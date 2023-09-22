import discord

class UserList:
    
    def __init__(self):
        self.mafiaUserList = []

    def getUserList(self):
        return self.mafiaUserList

    def containUserList(self, user: discord.user):

        for loop_user in self.getUserList():

            if (loop_user != user):
                continue
            return True
        
        return False

    def addUserList(self, user: discord.user):
        if (self.containUserList(user) == True):
            return
        self.mafiaUserList.append(user)

    def removeUserList(self, user: discord.user):
        if (self.containUserList(user) == False):
            return
        self.mafiaUserList.remove(user)

    def clearUserList(self):
        self.mafiaUserList.clear()