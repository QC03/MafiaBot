import discord

class mafiaDefaultRole():

    def __init__(self) -> None:
        self.role = None

    def setRole(self, role: discord.Role):
        self.role = role
    
    def getRole(self) -> discord.Role:
        return self.role
    
    def clearRole(self):
        self.role = None
    
    def isSet(self) -> bool:
        return (self.role != None)