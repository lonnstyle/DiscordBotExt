import discord
from discord.ext import commands
from matplotlib.colors import cnames


class Cog_Extension(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

class Hybirdcmd_Aliases():
    def __init__(self, lang, *cmdName: str):
        self.cmdName = list(cmdName)
        self.aliases: str = {}
        for i in cmdName:
            self.aliases[i] = lang[i+'.aliases']
            if i in self.aliases[i]:
                self.aliases[i].remove(i)
        self.count = len(self.cmdName)
        self.point = 0

    def next(self):
        self.point = self.point+1
        if self.point == self.count:
            self.point = 0

    def c_name(self,index = -1):
        if index != -1:
            self.point = index
        return self.cmdName[self.point]

    def c_aliases(self,index = -1):
        if index != -1:
            self.point = index
        i = self.cmdName[self.point]
        self.next()
        return self.aliases[i]