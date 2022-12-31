import asyncio
import json
import logging
import os
import re
from datetime import datetime, timedelta

import discord
import requests
from discord.ext import commands

from core.classes import Cog_Extension, Hybirdcmd_Aliases
from core.time import time_info
from localization import lang

lang = lang.langpref()['event']


with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

emojimap = requests.get("http://gist.githubusercontent.com/Vexs/629488c4bb4126ad2a9909309ed6bd71/raw/416403f7080d1b353d8517dfef5acec9aafda6c3/emoji_map.json").text
emojimap = json.loads(emojimap)
emojimap = {x: y for y, x in emojimap.items()}

logger = logging.getLogger('event')
logger.setLevel(-1)
handler = logging.FileHandler(filename='log/runtime.log', encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(lineno)d: %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
logger.addHandler(handler)

cmds = ['reactionrole', 'role']
hybirdAliases = Hybirdcmd_Aliases(lang, *cmds)


class event(Cog_Extension):
    # @commands.command(name="reactionRole", aliases=lang['reactionRole.aliases'], brief=lang['reactionRole.brief'], description=lang['reactionRole.description'])
    @hybirdAliases.hyb_cmd
    async def rr(self, ctx, message: int):
        with open("role/rr.txt", "a") as rr:
            rr.write(f"{message}\n")
            await ctx.message.add_reaction("✅")
            await ctx.message.delete(delay=5)

    # @commands.command(name='role', aliases=lang['role.aliases'], brief=lang['role.brief'], description=lang['role.description'])
    @hybirdAliases.hyb_cmd
    async def role(self, ctx, role: str, emoji):
        match = re.match(r'<(a?):([a-zA-Z0-9\_]+):([0-9]+)>$', emoji)
        if (emojimap.get(emoji, None) != None or match) and ctx.author.guild_permissions.administrator == True:
            with open("role/roles.txt", "a") as roles:
                roles.write(f"{emoji},{role}\n")
            await ctx.message.add_reaction("✅")
            await ctx.message.delete(delay=5)
        else:
            await ctx.message.delete()
            await ctx.send(embed=discord.Embed(title=lang['role.error.title'], description=lang['role.error.description']))

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        roles = {}
        message = []
        raw = open("role/roles.txt", "r")
        rr = open("role/rr.txt", "r")
        for line in raw.readlines():
            emoji, role = line.split(",")
            roles[emoji] = role.replace("\n", "")
        for line in rr.readlines():
            message.append(line.replace("\n", ""))
        for role in payload.member.guild.roles:
            if (role.name == roles.get(payload.emoji.name) or role.name == roles.get(f"<:{payload.emoji.name}:{payload.emoji.id}>")) and str(payload.message_id) in message:
                logger.info(f'[reactionRole] Add role {role.name} to user {payload.member.name}#{payload.member.discriminator}')
                await payload.member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        roles = {}
        message = []
        raw = open("role/roles.txt", "r")
        rr = open("role/rr.txt", "r")
        for line in raw.readlines():
            emoji, role = line.split(",")
            roles[emoji] = role.replace("\n", "")
        for line in rr.readlines():
            message.append(line.replace("\n", ""))
        guild = await self.bot.fetch_guild(payload.guild_id)
        member = await guild.fetch_member(payload.user_id)
        for role in member.roles:
            if (role.name == roles.get(payload.emoji.name) or role.name == roles.get(f"<:{payload.emoji.name}:{payload.emoji.id}>")) and str(payload.message_id) in message:
                logger.info(f'[reactionRole] Removed role {role.name} to user {payload.member.name}#{payload.member.discriminator}')
                await member.remove_roles(role)


async def setup(bot):
    if not os.path.exists("role"):
        os.makedirs("role")
    await bot.add_cog(event(bot))
