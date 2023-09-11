import os
from dotenv import load_dotenv

import discord
from MafiaUtil.Message import MsgUtil
from Database.PlayData.UserList import UserList

bot = discord.Bot()

load_dotenv()
guild = os.getenv("GUILDID")
token = os.getenv("TOKEN")

msgObj = MsgUtil()
userListObj = UserList()

@bot.slash_command(name="마피아유저", description="마피아 유저관련명령어", guild_ids=[guild])
async def mafiaUser(
    ctx: discord.ApplicationContext,
    type: discord.Option(str, choices=["추가", "제거"]),
    user:  discord.User
    ):

    await ctx.defer(ephemeral=False)

    if (user == None):
        await ctx.respond(embed = msgObj.errorMsg("유저를 입력해주세요."))
        return
    
    if (type == "추가"):
        userListObj.addUserList(user)
        await ctx.respond(embed = discord.Embed(title="마피아", description=f"{user} 님을 추가하였습니다.", color=0x2ecc71))

    elif (type == "제거"):
        userListObj.removeUserList(user)
        await ctx.respond(embed = discord.Embed(title="마피아", description=f"{user} 님을 제거하였습니다.", color=0x2ecc71))
    


@bot.slash_command(name="마피아", description="마피아 관련명령어", guild_ids=[guild])
async def mafia(
    ctx: discord.ApplicationContext,
    type: discord.Option(str, choices=["도움말", "시작", "종료", "유저확인"]),
    ):

    await ctx.defer(ephemeral=False)
    if (type == "시작"):

        if (len(userListObj.getUserList()) < 4):
            await ctx.respond(embed = msgObj.errorMsg("4명 이하로는 플레이가 불가능합니다."))
            return
        
        await ctx.respond(embed = msgObj.startMsg())
    
    elif (type == "강제종료"):

        userListObj.clearUserList()
        await ctx.respond(embed = discord.Embed(title="마피아", description="관리자에의해 강제종료되었습니다.", color=0x2ecc71))
    
    elif (type == "유저확인"):
        
        embed = discord.Embed(title="마피아", description="마피아 게임에 추가된 인원목록", color=0x2ecc71)
        for user in userListObj.getUserList():
            embed.add_field(name=f"{user}", value="", inline=False)
        
        await ctx.respond(embed=embed)

    else:
        await ctx.respond(embed = msgObj.mafiaHelp())


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

bot.run(token)