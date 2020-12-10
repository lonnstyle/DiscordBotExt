from discord.ext import commands
from core.classes import Cog_Extension
import requests
import json
from mwclient import Site #請自行安裝mwclient


site = Site('warframe.fandom.com', path='/zh-tw/', scheme='https')
page = site.pages['UserDict']
raw = page.text()
raw = json.loads(raw)
localDict = raw['Text']
localDict = {x: y for y, x in localDict.items()}
nicks = json.load(open("dict/localDict.json",'r'))#需要自行創建localDict


with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

userList = []
userList.append(str(jdata['owner']))

class wfm(Cog_Extension):
  @commands.command(name='wfm',aliases=['wm','市場查詢'])
  async def market(self,ctx,*args):
    msg = self.item(' '.join(args))
    await ctx.send(msg)

  def item(self,items):
    count = 5
    item = localDict.get(items,items)
    if item == items:
      item = nicks.get(items,items)
    item = item.lower()
    item = item.replace(' ','_')
    if item.find("primed") == -1:
      item = item.replace("prime","prime_set")
    url = "https://api.warframe.market/v1/items/" + item + "/orders"
    raw = requests.get(url)
    if raw.status_code != 200:
      print(item)
      return("Ordis覺得...指揮官是不是搞錯了什麼")
    else:
      raw = json.loads(raw.text)
      raw = raw['payload']
      raw = raw['orders']
      orderList = raw
      for x in range(len(orderList)):
        for y in range(0,len(orderList)-x-1):
          if(orderList[y]['platinum'] > orderList[y+1]['platinum']):
            orderList[y],orderList[y+1] = orderList[y+1],orderList[y]
      message = f"以下為{items}的五個最低價賣家資料:\n```"
      for orders in raw:
        if count>0:
          user = orders['user']
          if orders['order_type'] == 'sell' and user['status'] == 'ingame' and orders['platform'] == 'pc':
            message += f"價格:{int(orders['platinum'])}\t賣家:{user['ingame_name']}\n"
            count -= 1
      message += '```'
    return(message)
  
  @commands.command(name='dictUser')
  async def dictUser(self,ctx,*args):
    if ctx.message.author.id == jdata['owner']:
      msg = self.user(' '.join(args))
      await ctx.send(msg)
    else:
      await ctx.send("權限不足")

  def user(self,users):
    user = users.replace("@","")
    user = user.replace("!","")
    if user not in userList:
      userList.append(user)
      return("已加入")
    return("已在內")
    


  @commands.command(name='dict')
  async def dictionary(self,ctx,*args):
    with open("dictUser.txt",'r') as file:
      for lines in file:
        userList.append(file)
    if ctx.message.author.id in userList or ctx.message.author.id == jdata['owner']:
      msg = self.addDict(' '.join(args))
      await ctx.send("已加入")
    else:
      await ctx.send("權限不足")

  def addDict(self,items):
    nick, original = items.split(' ')
    url = "https://api.warframe.market/v1/items/" + original
    if requests.get(url).status_code == 200:
      with open("dict/localDict.json",'r') as nickDict:
        jsonDict = json.load(nickDict)
        wrote = jsonDict.get(nick,"Empty")
        nickDict.close()
        if wrote == "Empty":
          nickDict = open("dict/localDict.json",'a+')
          nickDict.write(f"\b\b,\n\"{nick}\": \"{original}\"\n"+"}")
          nickDict.close()
          return(f"{nick}已加入")
        else:
          return(f"{nick}已在內")


  @commands.command(name='reloadDict')
  async def reload(self,ctx):
    msg = self.load()
    await ctx.send(msg)
  
  def load():
    global nicks
    site = Site('warframe.fandom.com', path='/zh-tw/', scheme='https')
    page = site.pages['UserDict']
    raw = page.text()
    raw = json.loads(raw)
    localDict = raw['Text']
    localDict = {x: y for y, x in localDict.items()}
    nicks = json.load(open("dict/localDict.json",'r'))
    return("已重新載入Dict")


def setup(bot):
  bot.add_cog(wfm(bot))
