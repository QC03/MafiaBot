import discord

class mafiaChannel():

    def __init__(self) -> None:
        self.channel = None

    def setChannel(self, channel: discord.TextChannel):
        self.channel = channel
    
    def getChannel(self) -> discord.TextChannel:
        return self.channel
    
    def clearChanel(self):
        self.channel = None
    
    def isSet(self):
        return (self.channel != None)