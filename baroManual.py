import discord
from discord.ext import commands
from core.classes import Cog_Extension
import os
import requests
import json
import asyncio

rawDict = requests.get("https://raw.githubusercontent.com/lonnstyle/riven-mirror/dev/src/i18n/lang/zh-Hant.json")
Dict = json.loads(rawDict.text)
Dict = Dict['messages']

class baroManual(Cog_Extension):
  @commands.command(name='baro',aliases=['奸商' , 'Baro'])
  async def baroManual(self,ctx):
    url = requests.get("https://api.warframestat.us/pc/tc/voidTrader",headers={'Accept-Language':'zh','Cache-Control': 'no-cache'})
    html = json.loads(url.text)
    if html['active'] == True:
      message = "```"
      location = html['location']
      await ctx.send(f"Baro Ki'Teer 已經到達{location},帶來的商品如下:")
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
        message += f"物品:{name}\t杜卡德金幣:{ducats}\t現金:{credits}\n"
      message += "```"
      await ctx.send(message)
    if html['active'] == False:
      timeLeft = html['endString']
      day,minute,second = timeLeft.split(" ")
      day = day.replace("d","天")
      minute = minute.replace("m","分")
      second = second.replace("s","秒")
      timeLeft = day+minute+second
      location = html['location']
      await ctx.send(f"Baro Ki' Teer會在{timeLeft}後抵達{location}") 


def setup(bot):
    bot.add_cog(baroManual(bot))
