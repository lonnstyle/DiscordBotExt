from discord.ext import commands
from core.classes import Cog_Extension
import requests
import json
import chinese_converter
from datetime import datetime
import discord


class worldState(Cog_Extension):
  tag = "Warframe"

  def timeConv(self,expiry):
    h = int(expiry[11:13]) + 8
    m = expiry[14:16]
    m = ("0" if len(m) == 1 else "") + m
    s = expiry[17:19]
    s = ("0" if len(s) == 1 else "") + s
    return(str(h)+":"+m)
  
  @commands.command(name='POE',aliases=['夜靈平原時間' , 'poe'],brief="查詢夜靈平原時間",description="查詢夜靈平原目前日夜循環狀態和剩餘時間")
  async def eidolontime(self,ctx):
    html = requests.get('https://api.warframestat.us/pc/cetusCycle').text
    data = json.loads(html)
    if (data["state"]=="day"):
      desc = f"夜靈平原晚上將於{self.timeConv(data['expiry'])}開始\n距離夜靈平原晚上還有：" + data["timeLeft"]
      embed = discord.Embed(title="夜靈平原-早上☀️",description=desc,color=0xbfdaf3)
      await ctx.send(embed=embed)
    elif (data["state"]=="night"):
      desc = f"夜靈平原早上將於{self.timeConv(data['expiry'])}開始\n距離夜靈平原早上還有：" + data["timeLeft"]
      embed = discord.Embed(title="夜靈平原-晚上️🌙",description=desc,color=0xaca9ca)
      await ctx.send(embed=embed)

  @commands.command(name='Earth',aliases=['地球時間'],brief="查詢地球時間",description="查詢地球目前日夜循環狀態和剩餘時間")
  async def earthtime(self,ctx):
    html = requests.get('https://api.warframestat.us/pc/tc/earthCycle').text
    data = json.loads(html)
    if (data["state"]=="day"):
      desc = f"地球晚上將於{self.timeConv(data['expiry'])}開始\n距離地球晚上還有：" + data["timeLeft"]
      embed = discord.Embed(title="地球-早上☀️",description=desc,color=0xbfdaf3)
      await ctx.send(embed=embed)
    elif (data["state"]=="night"):
      desc = f"地球早上將於{self.timeConv(data['expiry'])}開始\n距離地球早上還有：" + data["timeLeft"]
      embed = discord.Embed(title="地球-晚上️🌙",description=desc,color=0xaca9ca)

  @commands.command(name='Cambion',aliases=['魔裔禁地時間'],brief="查詢魔裔禁地時間",description="查詢魔裔禁地目前日夜循環狀態和剩餘時間")
  async def cambiontime(self,ctx):
    html = requests.get('https://api.warframestat.us/pc/cetusCycle').text
    data = json.loads(html)
    if (data["state"]=="day"):
      desc = f"魔裔禁地Vome將於{self.timeConv(data['expiry'])}開始\n距離魔裔禁地Vome還有：" + data["timeLeft"]
      embed = discord.Embed(title="魔裔禁地Fass",description=desc,color=0xda6d34)
      await ctx.send(embed=embed)
    elif (data["state"]=="night"):
      desc = f"魔裔禁地Fass將於{self.timeConv(data['expiry'])}開始\n距離魔裔禁地Fass還有：" + data["timeLeft"]
      embed = discord.Embed(title="魔裔禁地Vome",description=desc,color=0x458691)
      await ctx.send(embed=embed)

  @commands.command(name='Orb',aliases=['奧布山谷時間' , 'orb'],brief="查詢奧布山谷時間",description="查詢奧布山谷目前日夜循環狀態和剩餘時間")
  async def orbtime(self,ctx):
    html = requests.get('https://api.warframestat.us/pc/vallisCycle',headers={'Accept-Language':'tc','Cache-Control': 'no-cache'}).text
    data = json.loads(html)
    if(data['state']=='cold'):
      desc = f"奧布山谷溫暖將於{self.timeConv(data['expiry'])}開始\n距離奧布山谷溫暖還有：" + data["timeLeft"]
      embed = discord.Embed(title="奧布山谷寒冷",description=desc,color=0x6ea7cd)
      await ctx.send(embed=embed)
    elif(data['state']=='warm'):
      desc = f"奧布山谷寒冷將於{self.timeConv(data['expiry'])}開始\n距離奧布山谷寒冷還有：" + data["timeLeft"]
      embed = discord.Embed(title="奧布山谷溫暖",description=desc,color=0xd9b4a1)
      await ctx.send(embed=embed)

  @commands.command(name="Arbitration",aliases=['仲裁'],brief="查詢仲裁任務",description="查詢當前仲裁任務與剩餘時間\n**此功能由於API不穩定，返回數據未必準確**")
  async def arbitration(self,ctx):
    raw = requests.get("https://api.warframestat.us/pc/tc/arbitration",headers={'Accept-Language':'zh'})
    text = raw.text
    text = chinese_converter.to_traditional(text)
    data = json.loads(text)
    expiry = data['expiry']
    timeLeft = datetime.strptime(expiry,'%Y-%m-%dT%X.000Z')
    now = datetime.now()
    timeLeft = timeLeft-now
    minutes = int((timeLeft.seconds - timeLeft.seconds%60)/60)
    seconds = timeLeft.seconds%60
    embed = discord.Embed(title="仲裁",description=f"任務:{data['type']}",color=0x302f36)
    embed.add_field(name=f"節點:{data['node']}",value=f"敵人:{data['enemy']}\n剩餘時間:{minutes}分鐘{seconds}秒")
    await ctx.send(embed=embed)

  @commands.command(name='Sortie',aliases=['突擊' , 'sortie'],brief="查詢突擊任務",description="查詢目前突擊任務和剩餘時間")
  async def sortie(self,ctx):
    count = 1
    raw = requests.get('https://api.warframestat.us/pc/zh/sortie',headers={'Accept-Language':'tc'})
    text = raw.text
    text = chinese_converter.to_traditional(text)
    data = json.loads(text)
    embed = discord.Embed(title=f"突擊剩餘時間：{data['eta']}",description=f"{data['boss']}的部隊，{data['faction']}陣營",color=0xff9500)
    for missions in data['variants']:
      node = missions['node']
      missionType= missions['missionType']
      modifier = missions['modifier']
      embed.add_field(name=f"突擊{count}:\n節點:{node} 等級{35+15*count}-{40+20*count}",value=f"任務:{missionType}\n狀態:{modifier}",inline=False)
      count += 1
    await ctx.send(embed=embed)
    
    

def setup(bot):
  bot.add_cog(worldState(bot))