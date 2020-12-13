from discord.ext import commands
from core.classes import Cog_Extension
import requests
import json
import chinese_converter
from datetime import datetime


class worldState(Cog_Extension):
  @commands.command(name='POE',aliases=['夜靈平原時間' , 'poe'])
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

  @commands.command(name='Orb',aliases=['奧布山谷時間' , 'orb'])
  async def orbtime(self,ctx):
    html = requests.get('https://api.warframestat.us/pc/vallisCycle',headers={'Accept-Language':'tc','Cache-Control': 'no-cache'}).text
    data = json.loads(html)
    if(data['state']=='cold'):
      await ctx.send("距離溫暖還有："+data['timeLeft'])
    elif(data['state']=='warm'):
      await ctx.send("距離寒冷還有："+data['timeLeft'])

  @commands.command(name="Arbitration",aliases=['仲裁'])
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
    await ctx.send(f"```\n當前仲裁任務(API並不穩定，僅供參考):\n任務:{data['type']}\n節點:{data['node']}\n敵人:{data['enemy']}\n剩餘時間:{minutes}分鐘{seconds}秒```")

  @commands.command(name='Sortie',aliases=['突擊' , 'sortie'])
  async def sortie(self,ctx):
    count = 1
    raw = requests.get('https://api.warframestat.us/pc/zh/sortie',headers={'Accept-Language':'tc'})
    text = raw.text
    text = chinese_converter.to_traditional(text)
    data = json.loads(text)
    await ctx.send(f"```\n突擊剩餘時間：{data['eta']}\n{data['boss']}的部隊，{data['faction']}陣營```")
    for missions in data['variants']:
      node = missions['node']
      missionType= missions['missionType']
      modifier = missions['modifier']
      await ctx.send(f'```突擊{count}:\n節點:{node} 等級{35+15*count}-{40+20*count}\n任務:{missionType}\n狀態:{modifier}```')
      count += 1
    
    

def setup(bot):
  bot.add_cog(worldState(bot))
