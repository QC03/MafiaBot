
from Database.GameData.UserList import UserList
from Database.DiscordData.Channel import mafiaChannel
from Database.GameData.MafiaRole import mafiaRole
from Database.DiscordData.Role import mafiaDefaultRole

class MafiaDB():

    def __init__(self,
                userListObj: UserList,
                playChannelObj: mafiaChannel,
                mafiaChannelObj: mafiaChannel,
                mafiaDefaultRoleObj: mafiaDefaultRole,
                deadList: list,
                mafiaTeam: list,
                citizenTeam: list
                ):
        
        self.userListObj = userListObj
        self.playChannelObj = playChannelObj
        self.mafiaChannelObj = mafiaChannelObj
        self.mafiaDefaultRoleObj = mafiaDefaultRoleObj

        self.deadList = deadList
        self.mafiaTeam = mafiaTeam
        self.citizenTeam = citizenTeam
    
    def getUserListObj(self) -> UserList:
        return self.userListObj

    def setUserListObj(self, userListObj: UserList):
        self.userListObj = userListObj
    

    def getPlayChannelObj(self) -> mafiaChannel:
        return self.playChannelObj

    def setPlayChannelObj(self, playChannelObj: mafiaChannel):
        self.playChannelObj = playChannelObj
    

    def getMafiaChannelObj(self) -> mafiaChannel:
        return self.mafiaChannelObj

    def setMafiaChannelObj(self, mafiaChannelObj: mafiaChannel):
        self.mafiaChannelObj = mafiaChannelObj
    

    def getDefaultRoleObj(self) -> mafiaDefaultRole:
        return self.mafiaDefaultRoleObj

    def setDefaultRoleObj(self, mafiaDefaultRoleObj: mafiaDefaultRole):
        self.mafiaDefaultRoleObj = mafiaDefaultRoleObj  


    def getDeadList(self) -> list:
        return self.deadList

    def setDeadList(self, deadList: list):
        self.deadList = deadList


    def getMafiaTeam(self) -> list:
        return self.mafiaTeam

    def setMafiaTeam(self, mafiaTeam: list):
        self.mafiaTeam = mafiaTeam


    def getCitizenTeam(self) -> list:
        return self.mafiaTeam

    def setCitizenTeam(self, citizenTeam: list):
        self.citizenTeam = citizenTeam