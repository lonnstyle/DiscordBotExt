import asyncio
import json
import logging
import os

import discord
import requests
from core.classes import Cog_Extension
from discord.ext import commands
# import chinese_converter
from localization import lang

# from discord_slash import SlashContext, cog_ext


lang = lang.langpref()['baro']

dirname = os.path.dirname(__file__)

rawDict = requests.get(lang['rawDict.URL'])
Dict = json.loads(rawDict.text)
Dict = Dict['messages']

logger = logging.getLogger('baro')
logger.setLevel(-1)
handler = logging.FileHandler(filename=os.path.join(dirname, '../log/runtime.log'),  encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(lineno)d: %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
logger.addHandler(handler)


class baro(Cog_Extension):
    @commands.command(name='baro', aliases=lang['baro.aliases'], brief=lang['baro.brief'], description=lang['baro.description'])
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
            stay = html['endString']
            # TODO: replace with UNIX timestamp
            logger.info(f"[baro] Baro arrived, leaving in {stay}")
            stay = stay.replace("d", lang['baro.time.day'])
            stay = stay.replace("h", lang['baro.time.hour'])
            stay = stay.replace("m", lang['baro.time.minute'])
            stay = stay.replace("s", lang['baro.time.second'])
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
            arrive = html['startString']
            logger.info(f"[baro] Baro is arriving in {arrive}")
            arrive = arrive.replace("d", lang['baro.time.day'])
            arrive = arrive.replace("h", lang['baro.time.hour'])
            arrive = arrive.replace("m", lang['baro.time.minute'])
            arrive = arrive.replace("s", lang['baro.time.second'])
            embed = discord.Embed(description=lang['baro.arrival'].format(arrive=arrive, location=location), color=0x429990)
            logger.info(f'[baro] data parsed, will arrive {location} in {arrive}')
            await ctx.send(embed=embed)

    # @cog_ext.cog_slash(name="baro", description=lang['baro.description'])
    # async def slash_baro(self, ctx: SlashContext):
    #     await self.baro(ctx)


async def setup(bot):
    await bot.add_cog(baro(bot))
