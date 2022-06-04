import asyncio
import json
import os
import re
from datetime import datetime, timedelta

import discord
import requests
from core.classes import Cog_Extension
from core.time import time_info
from discord.ext import commands
from localization import lang

lang = lang.langpref()['event']

dirname = os.path.dirname(__file__)

with open(os.path.join(dirname, '../setting.json'), 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

emojimap = requests.get("http://gist.githubusercontent.com/Vexs/629488c4bb4126ad2a9909309ed6bd71/raw/416403f7080d1b353d8517dfef5acec9aafda6c3/emoji_map.json").text
emojimap = json.loads(emojimap)
emojimap = {x: y for y, x in emojimap.items()}


class event(Cog_Extension):
    tag = "common"

    @commands.command(name="reactionRole", aliases=["rr"], brief="指定自動身份組訊息", description="指定可自動分發身份組的訊息")
    async def rr(self, ctx, message: int):
        with open("role/rr.txt", "a") as rr:
            rr.write(f"{message}\n")
            await ctx.message.add_reaction("✅")
            await ctx.message.delete(delay=5)

    @commands.command(name='role', aliases=lang['role.aliases'], brief=lang['role.brief'], description=lang['role.description'])
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
                await member.remove_roles(role)


def setup(bot):
    bot.add_cog(event(bot))
