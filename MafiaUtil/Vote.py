
import discord
import Vote

class Dropdown(discord.ui.Select):

    def __init__(self, userList: list, voteObj: Vote, deadList: list):
        
        self.voteObj = voteObj
        self.deadList = deadList

        options = []
        options.append(discord.SelectOption(label="스킵", description="스킵에 투표합니다.", emoji='🚫'))
        for user in userList:
            options.append(discord.SelectOption(label=f"{user.name} (ID: {user.id})", description="신중하게 선택해주세요 클릭시 투표가 완료 됩니다.", emoji='✅'))

        super().__init__(placeholder='투표할 사람을 선택해주세요...', min_values=1, max_values=1, options=options)
 
    async def callback(self, interaction: discord.Interaction):

        if (interaction.user in self.deadList):
            return

        userName = self.values[0].split("ID: ")
        userID = int(userName[1].replace(")", ""))
        votedUser = await discord.utils.get(interaction.guild.get_member(userID))
        
        self.voteObj.vote(votedUser)


class DropdownView(discord.ui.View):
    def __init__(self, userList: list, voteObj: Vote, deadList: list):
        super().__init__()

        self.add_item(Dropdown(userList, voteObj, deadList))


class Vote():

    def __init__(self):
        self.voteResult = dict()
    
    def vote(self, user: discord.user):
        self.voteResult[user] = self.voteResult[user] + 1
    
    def getResult(self) -> dict:
        return self.voteResult