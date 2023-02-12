import asyncio
import json
from log import logger
import os
import time
from datetime import datetime

import discord
import requests
from discord.ext import commands

from core.classes import Cog_Extension, Hybirdcmd_Aliases
# import chinese_converter
from localization import lang

# from discord_slash import SlashContext, cog_ext


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
        logger.info(f'[baro] {ctx.message.author} requested for baro info')
        url = requests.get("https://api.warframestat.us/pc/tc/voidTrader", headers={'Accept-Language': 'zh', 'Cache-Control': 'no-cache'})
        if url.status_code != 200:
            logger.warning(f'[baro] failed to fetch baro info')
            logger.warning(f'[baro] html status: {url.status_code} {url.reason}')
            color = discord.Colour.from_rgb(r=255, g=0, b=0)
            embed = discord.Embed(title=f"Error {url.status_code}", description={url.reason}, color=color)
            # TODO: localize string
            await ctx.send(embed=embed)
        else:
            logger.info('[baro] fetched baro info')
        logger.info('[baro] parsing json...')
        html = json.loads(url.text)
        if html['active'] == True:
            message = "```"
            location = html['location']
            # location = chinese_converter.to_traditional(location)
            stay = html['expiry']
            logger.info(f"[baro] Baro arrived, leaving at {stay}")
            stay = int(time.mktime(datetime.strptime(stay, "%Y-%m-%dT%H:%M:%S.%fZ").timetuple()))
            # convert datetime string to UNIX timestamp
            for items in html['inventory']:
                item = items['item']
                item = item.lower()
                item = item.replace("\'", "")
                count = 0
                name = ''
                for words in item.split():
                    if count != 0:
                        word = words.capitalize()
                        name += word
                    elif count == 0:
                        name += words
                    count += 1
                name = Dict.get(name, name)
                ducats = items['ducats']
                credits = items['credits']
                message += lang['baro.item'].format(name=name, ducats=ducats, credits=credits)
            message += "```"
            embed = discord.Embed(title=lang['baro.arrived'].format(location=location, stay=stay), description=message, color=0x429990)
            logger.info(f'[baro] data parsed, arrived at {location}, stay until {stay}')
            await ctx.send(embed=embed)
        if html['active'] == False:
            location = html['location']
            # location = chinese_converter.to_traditional(location)
            arrive = html['activation']
            arrive = int(time.mktime(datetime.strptime(arrive, "%Y-%m-%dT%H:%M:%S.000Z").timetuple()))
            logger.info(f"[baro] Baro is arriving in {arrive}")
            embed = discord.Embed(description=lang['baro.arrival'].format(arrive=arrive, location=location), color=0x429990)
            logger.info(f'[baro] data parsed, will arrive {location} in {arrive}')
            await ctx.send(embed=embed)

    # @cog_ext.cog_slash(name="baro", description=lang['baro.description'])
    # async def slash_baro(self, ctx: SlashContext):
    #     await self.baro(ctx)


async def setup(bot):
    await bot.add_cog(baro(bot))
