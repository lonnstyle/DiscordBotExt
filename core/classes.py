from logging import Logger

import discord
from discord.ext import commands


class Cog_Extension(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


class Hybirdcmd_Aliases():
    def __init__(self, lang, *cmdName: str):

        self.cmdName = list(cmdName)
        self.aliases = {}
        self.description = {}
        self.brief = {}

        for i in cmdName:

            try:
                aliases = []
                for alias in lang[i+'.aliases']:
                    alias = alias.lower()
                    if alias != i.lower():
                        aliases.append(alias)
                self.aliases[i] = aliases

            except:
                self.aliases[i] = []

            try:
                self.description[i] = lang[i+'.description']
                # baro's descripiton is always too long for somereason
                if i == 'baro':
                    self.description[i] = 'no_description'
            except:
                self.description[i] = 'no_description'

            try:
                self.brief[i] = lang[i+'.brief']
            except:
                self.brief[i] = 'no_brief'

        self.count = len(self.cmdName)
        self.point = 0

    def next(self):
        self.point = self.point+1
        if self.point == self.count:
            self.point = 0

    def c_name(self, index=-1):
        if index != -1:
            self.point = index
        return self.cmdName[self.point].lower()

    def c_aliases(self, index=-1):
        if index != -1:
            self.point = index
        i = self.cmdName[self.point]
        self.next()
        return self.aliases[i]

    def c_description(self, index=-1):
        if index != -1:
            self.point = index
        i = self.cmdName[self.point]
        return str(self.description[i])[:99]

    def c_brief(self, index=-1):
        if index != -1:
            self.point = index
        i = self.cmdName[self.point]
        return self.brief[i]

    def hyb_cmd(self, func, index=-1):
        if index != -1:
            self.point = index

        name = self.c_name()
        brief = self.c_brief()
        description = self.c_description()
        aliases = self.c_aliases()

        with_app_command: bool = True
        # @commands.hybrid_command(name=name,  aliases=aliases, brief=brief, description=description)
        return commands.HybridCommand(func, name=name, with_app_command=with_app_command,  aliases=aliases, brief=brief, description=description)
