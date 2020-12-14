from discord.ext import commands
from core.classes import Cog_Extension
import requests
import json
import chinese_converter
import asyncio
from datetime import datetime

with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)


class worldStateAuto(Cog_Extension):

  
  @commands.command(name="ArbitrationAuto")
  async def arbitration(self,ctx,*args):
    if ctx.message.author.id == jdata['owner']:
      args = str(args).replace(",","")
      args = args.replace("\'","")
      args = args.replace("(","")
      args = args.replace(")","")
      offset = int(args)
      if offset > 0:
        while(True):
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
          await asyncio.sleep(timeLeft.seconds+offset)
    else:
      await ctx.send("權限不足")
  
  @commands.command(name="SortieAuto")
  async def Sortie(self,ctx,*args):
    if ctx.message.author.id == jdata['owner']:
      args = str(args).replace(",","")
      args = args.replace("\'","")
      args = args.replace("(","")
      args = args.replace(")","")
      offset = int(args)
      if offset > 0:
        while(True):
          count = 1
          raw = requests.get('https://api.warframestat.us/pc/zh/sortie',headers={'Accept-Language':'tc'})
          text = raw.text
          text = chinese_converter.to_traditional(text)
          data = json.loads(text)
          msg = f"```\n突擊剩餘時間：{data['eta']}\n{data['boss']}的部隊，{data['faction']}陣營```"
          for missions in data['variants']:
            node = missions['node']
            missionType= missions['missionType']
            modifier = missions['modifier']
            msg += f'```突擊{count}:\n節點:{node} 等級{35+15*count}-{40+20*count}\n任務:{missionType}\n狀態:{modifier}```'
            count += 1
          await ctx.send(msg)
          expiry = data['expiry']
          timeLeft = datetime.strptime(expiry,'%Y-%m-%dT%X.000Z')
          now = datetime.now()
          timeLeft = timeLeft-now
          await asyncio.sleep(timeLeft.seconds+offset)
    else:
      await ctx.send("權限不足")
    


def setup(bot):
  bot.add_cog(worldStateAuto(bot))
  worldStateAuto.arbitration(100)
