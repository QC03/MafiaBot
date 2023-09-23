
import discord
from Database.GameData.UserList import UserList

class MsgUtil:

    def __init__(self) -> None:
        pass

    def errorMsg(self, msg: str):
        embed = discord.Embed(title="ERROR", description=f"{msg}", color=0x2ecc71)
        return embed
    
    def startMsg(self, userlist: list):
        embed = discord.Embed(title="마피아", description="마피아 시작", color=0x2ecc71)
        for user in userlist:
            embed.add_field(name=f"{user}", value="", inline=False)
        return embed


    def mafiaHelp(self):
        embed = discord.Embed(title="마피아", description="마피아 명령어", color=0x2ecc71)
        embed.add_field(name="/마피아 시작", value="마피아를 시작합니다.", inline=True)
        embed.add_field(name="/마피아 강제종료", value="마피아를 강제로 종료합니다.", inline=True)
        embed.add_field(name="/마피아 유저확인", value="마피아 게임에 추가된 인원목록을 나열합니다.", inline=True)
        embed.add_field(name="", value="", inline=False)
        embed.add_field(name="/마피아유저 추가 @유저", value="마피아를 플레이할 유저를 목록에 추가합니다.", inline=True)
        embed.add_field(name="/마피아유저 제거 @유저", value="마피아를 플레이하지 않는 유저를 목록에서 제거합니다.", inline=True)
        return embed