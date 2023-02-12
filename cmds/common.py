import asyncio
import json
from log import logger
import os
import re
from random import randint

import discord
import requests
from discord.ext import commands

from core.classes import Cog_Extension, Hybirdcmd_Aliases
from localization import lang


lang = lang.langpref()['common']

with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

emoji = requests.get("http://gist.githubusercontent.com/Vexs/629488c4bb4126ad2a9909309ed6bd71/raw/416403f7080d1b353d8517dfef5acec9aafda6c3/emoji_map.json").text
emoji = json.loads(emoji)
emoji = {x: y for y, x in emoji.items()}

logger = logger.getLogger('common')


cmds = ['ping', 'sayd', 'poll']
hybirdAliases = Hybirdcmd_Aliases(lang, *cmds)


class common(Cog_Extension):

    @hybirdAliases.hyb_cmd
    async def ping(self, ctx):
        latency = round(self.bot.latency*1000)
        red = max(0, min(int(255*(latency-50)/1000), 255))
        green = 255-red
        color = discord.Colour.from_rgb(r=red, g=green, b=0)
        embed = discord.Embed(title=lang['ping.embed.title'], description=lang['ping.latency'].format(latency=latency), color=color)
        logger.info(f'[ping] {ctx.message.author} ping, latency:{latency}ms')
        await ctx.send(embed=embed)

    # @cog_ext.cog_slash(name="ping", description=lang['ping.description'])
    # async def slash_ping(self, ctx: SlashContext):
    #     await self.ping(ctx)

    @hybirdAliases.hyb_cmd
    async def sayd(self, ctx, *, msg):
        try:
            await ctx.message.delete()
            logger.info('[sayd] deleted source message')
        except Exception as e:
            logger.error(f'[sayd] cannot delete source message, cuz {e}')
        embed = discord.Embed(description=msg, color=0x3C879C)
        for items in ctx.message.attachments:
            logger.info(f'[sayd] attachment found: {items.url}')
            embed.set_image(url=items.url)
        message = await ctx.send(embed=embed)
        if ctx.channel.id == jdata['publish']:
            logger.info('[sayd] message published')
            await message.publish()

    @hybirdAliases.hyb_cmd
    async def poll(self, ctx, topic, option1, emoji1, option2, emoji2):
        try:
            await ctx.message.delete()
            logger.info('[poll] deleted source message')
        except Exception as e:
            logger.error(f'[poll] cannot delete source message, cuz {e}')
        match1 = re.match(r'<(a?):([a-zA-Z0-9\_]+):([0-9]+)>$', emoji1)
        match2 = re.match(r'<(a?):([a-zA-Z0-9\_]+):([0-9]+)>$', emoji2)
        if (emoji.get(emoji1, None) != None or match1) and (emoji.get(emoji2, None) != None or match2):
            if emoji1 == emoji2 or option1 == option2:
                await ctx.send(embed=discord.Embed(title=lang['poll.error.title'], description=lang['poll.error.description.same'], color=0xff0000))
                return
            embed = discord.Embed(description=topic, color=0x3C879C)
            embed.add_field(name=option1, value=emoji1)
            embed.add_field(name=option2, value=emoji2)
            message = await ctx.send(embed=embed)
            await message.add_reaction(emoji1)
            await message.add_reaction(emoji2)
        else:
            await ctx.send(embed=discord.Embed(title=lang['poll.error.title'], description=lang['poll.error.description.emoji']))


async def setup(bot):
    await bot.add_cog(common(bot))
