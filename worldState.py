import discord
from discord.ext import commands
from core.classes import Cog_Extension
import os
import requests
import json


class worldState(Cog_Extension):
  @commands.command(name='POE',aliases=['夜靈平原時間'])
  async def eidolontime(self,ctx):
    html = requests.get('https://api.warframestat.us/pc/cetusCycle').text
    data = json.loads(html)
    if (data["state"]=="day"):
      await ctx.send("距離夜靈平原晚上還有：" + data["timeLeft"])
    elif (data["state"]=="night"):
      await ctx.send("距離夜靈平原早上還有：" + data["timeLeft"])

  @commands.command(name='Earth',aliases=['地球時間'])
  async def earthtime(self,ctx):
    html = requests.get('https://api.warframestat.us/pc/tc/earthCycle').text
    data = json.loads(html)
    if (data["state"]=="day"):
      await ctx.send("距離晚上還有：" + data["timeLeft"])
    elif (data["state"]=="night"):
      await ctx.send("距離早上還有：" + data["timeLeft"])

  @commands.command(name='Cambion',aliases=['魔裔禁地時間'])
  async def cambiontime(self,ctx):
    html = requests.get('https://api.warframestat.us/pc/cetusCycle').text
    data = json.loads(html)
    if (data["state"]=="day"):
      await ctx.send("距離魔裔禁地Vome還有：" + data["timeLeft"])
    elif (data["state"]=="night"):
      await ctx.send("距離魔裔禁地Fass還有：" + data["timeLeft"])

  @commands.command(name='Orb',aliases=['奧布山谷時間'])
  async def orbtime(self,ctx):
    html = requests.get('https://api.warframestat.us/pc/vallisCycle',headers={'Accept-Language':'tc','Cache-Control': 'no-cache'}).text
    data = json.loads(html)
    if(data['state']=='cold'):
      await ctx.send("距离溫暖還有："+data['timeLeft'])
    elif(data['state']=='warm'):
      await ctx.send("距离寒冷還有："+data['timeLeft'])

  @commands.command(name='Sortie',aliases=['突擊'])
  async def sortie(self,ctx):
    count = 1
    raw = requests.get('https://api.warframestat.us/pc/zh/sortie',headers={'Accept-Language':'tc'})
    data = json.loads(raw.text)
    await ctx.send(f"```\n突擊剩餘時間：{data['eta']}\n{data['boss']}的部隊，{data['faction']}陣營```")
    for missions in data['variants']:
      node = missions['node']
      missionType= missions['missionType']
      modifier = missions['modifier']
      await ctx.send(f'```突擊{count}:\n節點:{node} 等級{35+15*count}-{40+20*count}\n任務:{missionType}\n狀態:{modifier}```')
      count += 1

def setup(bot):
    bot.add_cog(worldState(bot))
