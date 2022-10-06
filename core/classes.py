
import logging
import os

import discord
from discord.ext import commands

logger = logging.getLogger('classes')
logger.setLevel(-1)
# display all logging messages
dirname = os.path.dirname(__file__)
handler = logging.FileHandler(filename=os.path.join(dirname, '../log/runtime.log'), encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(lineno)d: %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
logger.addHandler(handler)


class Cog_Extension(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


class Hybirdcmd_Aliases():
    def __init__(self, lang, *cmd_names: str):

        self.cmd_names = list(cmd_names)
        self.aliases = {}
        self.description = {}
        self.brief = {}

        for cmd_name in cmd_names:

            aliases = []
            for alias in lang.get(cmd_name+'.aliases', []):
                alias = alias.lower()
                if alias != cmd_name.lower():
                    aliases.append(alias)
            self.aliases[cmd_name] = aliases

            self.description[cmd_name] = lang.get(cmd_name + '.description', 'no_description')

            self.brief[cmd_name] = lang.get(cmd_name+'.brief', 'no_brief')

        self.count = len(self.cmd_names)
        self.point = 0

    def next(self):
        self.point = self.point+1
        if self.point == self.count:
            self.point = 0

    def get_cmd_name(self):
        return self.cmd_names[self.point].lower()

    def get_cmd_aliases(self):
        cmd_name = self.cmd_names[self.point]
        self.next()
        return self.aliases[cmd_name]

    def get_cmd_description(self):
        cmd_name = self.cmd_names[self.point]
        description = self.description[cmd_name][:99]
        if len(description) > 99:
            logging.debug(f"descripiton of command : [{cmd_name}] is too long ,its cropped to fit the size(1 - 100 charaters)")
        return description

    def get_cmd_brief(self):
        cmd_name = self.cmd_names[self.point]
        return self.brief[cmd_name]

    def hyb_cmd(self, func, index=-1):
        if index != -1:
            self.point = index

        name = self.get_cmd_name()
        brief = self.get_cmd_brief()
        description = self.get_cmd_description()
        aliases = self.get_cmd_aliases()

        with_app_command: bool = True
        # @commands.hybrid_command(name=name,  aliases=aliases, brief=brief, description=description)
        return commands.HybridCommand(func, name=name, with_app_command=with_app_command,  aliases=aliases, brief=brief, description=description)
