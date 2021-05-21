import discord
from discord.ext import commands
from core.classes import Cog_Extension
import os
import requests
import json
import asyncio
from discord_slash import SlashContext,cog_ext
# import chinese_converter
from language import language as lang

lang = lang()
lang = lang.langpref()['baro']

rawDict = requests.get(lang['rawDict.URL'])
Dict = json.loads(rawDict.text)
Dict = Dict['messages']

class baro(Cog_Extension):
  tag = "Warframe"
  @commands.command(name='baro',aliases=lang['baro.aliases'],brief=lang['baro.brief'],description=lang['baro.description'])
  async def baro(self,ctx):
    url = requests.get("https://api.warframestat.us/pc/tc/voidTrader",headers={'Accept-Language':'zh','Cache-Control': 'no-cache'})
    html = json.loads(url.text)
    if html['active'] == True:
      message = "```"
      location = html['location']
      # location = chinese_converter.to_traditional(location)
      stay = html['endString']
      stay = stay.replace("d",lang['baro.time.day'])
      stay = stay.replace("h",lang['baro.time.hour'])
      stay = stay.replace("m",lang['baro.time.minute'])
      stay = stay.replace("s",lang['baro.time.second'])
      for items in html['inventory']:
        item = items['item']
        item = item.lower()
        item = item.replace("\'","")
        count = 0
        name = ''
        for words in item.split():
          if count != 0:
            word = words.capitalize()
            name += word
          elif count == 0:
            name += words
          count += 1
        name = Dict.get(name,name)
        ducats = items['ducats']
        credits = items['credits']
        message += lang['baro.item'].format(name=name,ducats=ducats,credits=credits)
      message += "```"
      embed = discord.Embed(title=lang['baro.arrived'].format(location=location,stay=stay),description=message,color=0x429990)
      await ctx.send(embed=embed)
    if html['active'] == False:
      location = html['location']
      # location = chinese_converter.to_traditional(location)
      arrive = html['startString']
      arrive = arrive.replace("d",lang['baro.time.day'])
      arrive = arrive.replace("h",lang['baro.time.hour'])
      arrive = arrive.replace("m",lang['baro.time.minute'])
      arrive = arrive.replace("s",lang['baro.time.second'])
      embed = discord.Embed(description=lang['baro.arrival'].format(arrive=arrive,location=location),color=0x429990)
      await ctx.send(embed=embed) 

  @cog_ext.cog_slash(name="baro",description=lang['baro.description'])
  async def slash_baro(self, ctx:SlashContext):
    await self.baro(ctx)

def setup(bot):
    bot.add_cog(baro(bot))