import os
from dotenv import load_dotenv

import discord
from MafiaUtil.Message import MsgUtil
from Database.GameData.UserList import UserList
from Database.DiscordData.Channel import mafiaChannel
from Database.DiscordData.Role import mafiaDefaultRole
from Database.MafiaDB import MafiaDB
from GamePlay.Game import Mafia

bot = discord.Bot()

load_dotenv()
guild = os.getenv("GUILDID")
token = os.getenv("TOKEN")

msgObj = MsgUtil()
mafiaDB = MafiaDB(
    userListObj= UserList(),
    playChannelObj= mafiaChannel(),
    mafiaChannelObj= mafiaChannel(),
    mafiaDefaultRoleObj= mafiaDefaultRole(),

    deadList= [],
    mafiaTeam= [],
    citizenTeam= []
)
mafia = Mafia(mafiaDB)

@bot.slash_command(name="마피아유저", description="마피아 유저관련 명령어", guild_ids=[guild])
async def mafiaUserCmd(
    ctx: discord.ApplicationContext,
    type: discord.Option(str, choices=["추가", "제거"]),
    user:  discord.User
    ):

    await ctx.defer(ephemeral=False)

    if (user == None) or (user.bot):
        await ctx.respond(embed = msgObj.errorMsg("유저를 입력해주세요."))
        return
    
    if (type == "추가"):
        mafiaDB.getUserListObj().addUserList(user)
        await ctx.respond(embed = discord.Embed(title="마피아", description=f"{user.name} 님을 추가하였습니다.", color=0x2ecc71))

    elif (type == "제거"):
        mafiaDB.getUserListObj().removeUserList(user)
        await ctx.respond(embed = discord.Embed(title="마피아", description=f"{user.name} 님을 제거하였습니다.", color=0x2ecc71))



@bot.slash_command(name="마피아", description="마피아 관련명령어", guild_ids=[guild])
async def mafiaCmd(
    ctx: discord.ApplicationContext,
    type: discord.Option(str, choices=["도움말", "시작", "종료", "유저확인"]),
    ):

    await ctx.defer(ephemeral=False)
    if (type == "시작"):

        if (len(mafiaDB.getUserListObj().getUserList()) < 4):
            await ctx.respond(embed = msgObj.errorMsg("4명 이하로는 플레이가 불가능합니다."))
            return

        if (len(mafiaDB.getUserListObj().getUserList()) >= 8):
            await ctx.respond(embed = msgObj.errorMsg("8명 이상으로는 플레이가 불가능합니다."))
            return
        
        await mafia.startMafia()

        await ctx.respond(embed = msgObj.startMsg(mafiaDB.getUserListObj().getUserList()))
    
    elif (type == "강제종료"):

        mafiaDB.getUserListObj().clearUserList()
        await mafia.removeMafiaRole()
        await ctx.respond(embed = discord.Embed(title="마피아", description="관리자에의해 강제종료되었습니다.", color=0x2ecc71))
    
    elif (type == "유저확인"):
        
        embed = discord.Embed(title="마피아", description="마피아 게임에 추가된 인원목록", color=0x2ecc71)
        for user in mafiaDB.getUserListObj().getUserList():
            embed.add_field(name=f"{user}", value="", inline=False)
        
        await ctx.respond(embed=embed)

    else:
        await ctx.respond(embed = msgObj.mafiaHelp())


@bot.slash_command(name="마피아역할", description="마피아 참여역할을 지정합니다.", guild_ids=[guild])
async def mafiaRoleCmd(
    ctx: discord.ApplicationContext,
    role: discord.Role,
    ):

    await ctx.defer(ephemeral=False)

    mafiaDefaultRoleObj.setRole(role)

    if (playChannelObj.isSet() == True):
        await playChannelObj.getChannel().set_permissions(mafiaDefaultRoleObj.getRole(), read_messages=True, send_messages=True)

    await ctx.respond(embed=discord.Embed(title="마피아", description=f"마피아 참여역할을 {role.name}(으)로 지정하였습니다.", color=0x2ecc71))


@bot.slash_command(name="마피아채널", description="마피아를 플레이할 채널을 지정합니다.", guild_ids=[guild])
async def mafiaChannelCmd(
    ctx: discord.ApplicationContext,
    type: discord.Option(str, choices=["마피아", "일반"]),
    channel: discord.TextChannel,
    ):

    await ctx.defer(ephemeral=False)

    if (mafiaDB.getDefaultRoleObj().isSet() == False):
        await ctx.respond(embed = msgObj.errorMsg("마피아 참여역할을 먼저 지정해주세요."))
        return

    if (type == "마피아"):
        mafiaDB.getMafiaChannelObj().setChannel(channel=channel)
    elif (type == "일반"):
        mafiaDB.getPlayChannelObj().setChannel(channel=channel)
    else:
        return

    await channel.set_permissions(ctx.guild.default_role, read_messages=False, send_messages=False)
    await channel.set_permissions(mafiaDB.getDefaultRoleObj().getRole(), read_messages=True, send_messages=True)

    await ctx.respond(embed=discord.Embed(title="마피아", description=f"{type} 채널을 {channel}(으)로 지정하였습니다.", color=0x2ecc71))



@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


bot.run(token)