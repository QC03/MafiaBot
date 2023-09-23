import discord

class UserList:
    
    def __init__(self):
        self.mafiaUserList = []

    def getUserList(self):
        return self.mafiaUserList

    def addUserList(self, user: discord.user):
        if (user in self.mafiaUserList == True):
            return
        self.mafiaUserList.append(user)

    def removeUserList(self, user: discord.user):
        if (user in self.mafiaUserList == False):
            return
        self.mafiaUserList.remove(user)

    def clearUserList(self):
        self.mafiaUserList.clear()