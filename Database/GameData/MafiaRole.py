import discord
import random
from Database.MafiaDB import MafiaDB

class mafiaRole():

    def __init__(self, mafiaDB: MafiaDB):
        self.mafiaRole = dict()
        self.mafiaTeam = mafiaDB.mafiaTeam.copy()
        self.citizenTeam = mafiaDB.citizenTeam.copy()

        self.userSize = len(self.mafiaTeam + self.citizenTeam)
    
    async def autoSelect(self):
        await self.selectMafia()
        await self.selectSpy()
        await self.selectPolice()
        await self.selectDoctor()
        await self.selectSubJob()

    async def selectMafia(self):

        mafiaSize = 0
        if (self.userSize in range(4, 7)):
            mafiaSize = 1
        elif (self.userSize in range(8, 10)):
            mafiaSize = 2
        elif (self.userSize in range(11, 12)):
            mafiaSize = 3

        for i in range(mafiaSize):

            mafia = random.choice(self.mafiaTeam)
            self.mafiaRole[mafia] = "마피아"
            self.mafiaTeam.remove(mafia)

            await mafia.send(embed=discord.Embed(title="마피아", description="당신은 마피아 입니다.", color=0x2ecc71))
    
    async def selectSpy(self):

        if (self.userSize in range(4, 5)):
            return
        
        spy = random.choice(self.mafiaTeam)
        self.mafiaRole[spy] = "스파이"
        self.mafiaTeam.remove(spy)

        await spy.send(embed=discord.Embed(title="마피아", description="당신은 스파이 입니다.", color=0x2ecc71))
    
    async def selectPolice(self):

        police = random.choice(self.citizenTeam)
        self.mafiaRole[police] = "경찰"
        self.citizenTeam.remove(police)

        await police.send(embed=discord.Embed(title="마피아", description="당신은 경찰 입니다.", color=0x2ecc71))
    
    async def selectDoctor(self):
        
        doctor = random.choice(self.citizenTeam)
        self.mafiaRole[doctor] = "의사"
        self.citizenTeam.remove(doctor)

        await doctor.send(embed=discord.Embed(title="마피아", description="당신은 의사 입니다.", color=0x2ecc71))
    
    async def selectSubJob(self):
        
        if (len(self.citizenTeam) == 0):
            return

        subJobs = ["군인", "정치인", "시민", "기자", "건달", "테러리스트"]

        for user in self.citizenTeam:
            job = random.choice(subJobs)
            self.mafiaRole[user] = "job"
            self.citizenTeam.remove(user)
            subJobs.remove(job)

            await user.send(embed=discord.Embed(title="마피아", description=f"당신은 {job} 입니다.", color=0x2ecc71))

    async def getJobs(self) -> dict:
        return self.mafiaRole