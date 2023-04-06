import asyncio
import json
import os
import time
from datetime import datetime

import discord
import requests
from discord.ext import commands

from cmds.parsers.world_state import WorldStateParser
from core.classes import Cog_Extension, Hybirdcmd_Aliases
# import chinese_converter
from localization import lang
from log import logger

# from discord_slash import SlashContext, cog_ext

parser = WorldStateParser()
lang = lang.langpref()['baro']


rawDict = requests.get(lang['rawDict.URL'])
Dict = json.loads(rawDict.text)
Dict = Dict['messages']

logger = logger.getLogger('baro')


cmds = ['baro']
hybirdAliases = Hybirdcmd_Aliases(lang, *cmds)


class baro(Cog_Extension):
    @hybirdAliases.hyb_cmd
    async def baro(self, ctx):
        arrive, expiry, node_name, system, items = parser.get_baro()
        now = datetime.utcnow().timestamp()
        location = node_name + '(' + system + ')'
        arrived = now > arrive
        arrive = int(arrive)
        expiry = int(expiry)
        if arrived:
            message = "```"
            # location = chinese_converter.to_traditional(location)
            stay = expiry
            logger.info(f"[baro] Baro arrived, leaving at {stay}")
            stay = int(time.mktime(datetime.strptime(stay, "%Y-%m-%dT%H:%M:%S.%fZ").timetuple()))
            # convert datetime string to UNIX timestamp
            for item in items:
                name = item
                ducats = items['PrimePrice']
                credits = items['RegularPrice']
                message += lang['baro.item'].format(name=name, ducats=ducats, credits=credits)
            message += "```"
            embed = discord.Embed(title=lang['baro.arrived'].format(location=location, stay=stay), description=message, color=0x429990)
            logger.info(f'[baro] data parsed, arrived at {location}, stay until {stay}')
            await ctx.send(embed=embed)
        else:
            # location = chinese_converter.to_traditional(location)
            logger.info(f"[baro] Baro is arriving in {arrive}")
            embed = discord.Embed(description=lang['baro.arrival'].format(arrive=arrive, location=location), color=0x429990)
            logger.info(f'[baro] data parsed, will arrive {location} in {arrive}')
            await ctx.send(embed=embed)

    # @cog_ext.cog_slash(name="baro", description=lang['baro.description'])
    # async def slash_baro(self, ctx: SlashContext):
    #     await self.baro(ctx)


async def setup(bot):
    await bot.add_cog(baro(bot))
