
import discord
import random
import time
from Database.GameData.UserList import UserList
from Database.DiscordData.Channel import mafiaChannel
from Database.GameData.MafiaRole import mafiaRole
from Database.DiscordData.Role import mafiaDefaultRole
from MafiaUtil.Vote import Vote, DropdownView

class Mafia():

    def __init__(self, userListObj: UserList, playChannelObj: mafiaChannel, mafiaChannelObj: mafiaChannel, mafiaDefaultRoleObj: mafiaDefaultRole):
        self.userListObj = userListObj
        self.playChannelObj = playChannelObj
        self.mafiaChannelObj = mafiaChannelObj
        self.mafiaDefaultRoleObj = mafiaDefaultRoleObj

        self.deadList = []
        self.mafiaTeam = []
        self.citizenTeam = []

    async def giveMafiaRole(self):

        for user in self.userListObj.getUserList():
            await user.add_roles(self.mafiaDefaultRoleObj.getRole())
    

    async def removeMafiaRole(self):

        for user in self.userListObj.getUserList():
            await user.remove_roles(self.mafiaDefaultRoleObj.getRole())


    def splitTeam(self):

        userList = self.userListObj.getUserList().copy()

        mafiaSize = 0
        if (len(userList) in range(4, 5)):
            mafiaSize = 1
        elif (len(userList) in range(6, 7)):
            mafiaSize = 2
        elif (len(userList) in range(8, 10)):
            mafiaSize = 3
        else:
            mafiaSize = 4

        for i in range(mafiaSize):
            tempUser = random.choice(userList)
            self.mafiaTeam.append(tempUser)
            userList.remove(tempUser)

        for user in userList:

            if (user in self.mafiaTeam):
                continue
   
            self.citizenTeam.append(user)
            


    async def startMafia(self):

        channel = self.playChannelObj.getChannel()
        mafia_Channel = self.mafiaChannelObj.getChannel()
        userList = self.userListObj.getUserList()

        await self.giveMafiaRole()

        self.splitTeam()
        mafiarole = mafiaRole(self.mafiaTeam, self.citizenTeam)
        await mafiarole.autoSelect()

        for user in userList:
            await mafia_Channel.set_permissions(user, read_messages=False, send_messages=False)
            await channel.set_permissions(user, read_messages=True, send_messages=True)

        for mafiaUser in self.mafiaTeam:
            await mafia_Channel.set_permissions(mafiaUser, read_messages=True, send_messages=True)
            await channel.set_permissions(mafiaUser, read_messages=True, send_messages=True)

        await channel.send(embed=discord.Embed(title="마피아", description="마피아 게임이 시작되었습니다.", color=0x2ecc71))

        while (len(userList) > 0):
            time.sleep(50)
            await channel.send(embed=discord.Embed(title="마피아", description="투표까지 10초 남았습니다.", color=0x2ecc71))
            
            time.sleep(10)
            voteObj = Vote()

            for user in userList:
                await mafia_Channel.set_permissions(user, send_messages=False)
                await channel.set_permissions(user, send_messages=False)

            await channel.send(embed=discord.Embed(title="마피아", description="아래 메뉴에서 투표해주세요!", color=0x2ecc71), view=DropdownView(userList=userList, voteObj=voteObj, deadList=self.deadList))

            time.sleep(20)
            values = []
            for value in voteObj.getResult().values():
                values.append(value)
            values.sort()

            sameRanks = []
            first = values[0]
            for votedUser in voteObj.getResult().keys():
                if (voteObj.getResult()[votedUser] != first):
                    continue
                sameRanks.append(votedUser)
            
            if (sameRanks.count() > 1):
                voteResultEmbed = discord.Embed(title="마피아", description="투표가 종료되었습니다.", color=0x2ecc71)
                voteResultEmbed.add_field(name="아무도 처형되지 않았습니다.")
            else:
                voteResultEmbed = discord.Embed(title="마피아", description="투표가 종료되었습니다.", color=0x2ecc71)
                voteResultEmbed.add_field(name=f"{sameRanks[0].name}", value="님이 처형되었습니다.")
                self.deadList.append(sameRanks[0])


            await channel.send(embed=voteResultEmbed)

            for user in userList:
                await channel.set_permissions(user, send_messages=True)

            for mafiaUser in self.mafiaTeam:
                await mafia_Channel.set_permissions(mafiaUser, send_messages=True)

            await channel.send(embed=discord.Embed(title="마피아", description="밤이 되었습니다.", color=0x2ecc71))

