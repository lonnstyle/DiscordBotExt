import discord
from discord.ext import commands
from core.classes import Cog_Extension
import os
import requests
import json
import asyncio
import chinese_converter

rawDict = requests.get("https://raw.githubusercontent.com/lonnstyle/riven-mirror/dev/src/i18n/lang/zh-Hant.json")
Dict = json.loads(rawDict.text)
Dict = Dict['messages']

class baro(Cog_Extension):
  tag = "Warframe"
  @commands.command(name='baro',aliases=['奸商' , 'Baro'],brief="虛空商人信息",description="查詢虛空商人Baro Ki'Teer目前狀態\t如已經抵達中繼站則會顯示所攜帶商品列表")
  async def baroManual(self,ctx):
    url = requests.get("https://api.warframestat.us/pc/tc/voidTrader",headers={'Accept-Language':'zh','Cache-Control': 'no-cache'})
    html = json.loads(url.text)
    if html['active'] == True:
      message = "```"
      location = html['location']
      location = chinese_converter.to_traditional(location)
      stay = html['endString']
      stay = stay.replace("d","天")
      stay = stay.replace("h","小時")
      stay = stay.replace("m","分鐘")
      stay = stay.replace("s","秒")
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
        message += f"物品:{name}\n杜卡德金幣:{ducats}\t現金:{credits}\n"
      message += "```"
      embed = discord.Embed(title=f"Baro Ki'Teer 已經到達{location},停留時間為{stay}\t帶來的商品如下:",description=message,color=0x429990)
      await ctx.send(embed=embed)
    if html['active'] == False:
      location = html['location']
      location = chinese_converter.to_traditional(location)
      arrive = html['startString']
      arrive = arrive.replace("d","天")
      arrive = arrive.replace("h","小時")
      arrive = arrive.replace("m","分鐘")
      arrive = arrive.replace("s","秒")
      embed = discord.Embed(description=f"Baro Ki' Teer會在{arrive}後抵達{location}",color=0x429990)
      await ctx.send(embed=embed) 


def setup(bot):
    bot.add_cog(baro(bot))