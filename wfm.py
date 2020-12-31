from discord.ext import commands
from core.classes import Cog_Extension
import requests
import json
import discord
from discord_webhook import DiscordWebhook, DiscordEmbed

with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)


localDict = requests.get("https://raw.githubusercontent.com/lonnstyle/DiscordBotMods/main/dict/items_zh-hant.json")
localDict = json.loads(localDict.text)
localDict = {x: y for y, x in localDict.items()}
enDict = requests.get("https://raw.githubusercontent.com/lonnstyle/DiscordBotMods/main/dict/items_en.json")
enDict = json.loads(enDict.text)
enDict = {x: y for y, x in enDict.items()}


class wfm(Cog_Extension):
  @commands.command(name='wfm', aliases=['wm', '市場查詢'])
  async def market(self, ctx, *args):
    items = ' '.join(args)
    itemSet = False
    if "Set" in items:
      itemSet = True
    count = 5
    item = localDict.get(items, items)
    if item == items:
      item = enDict.get(items,items)
    if item == items:
      await ctx.send("Ordis不太清楚指揮官說的什麼呢") 
      return       
    url = "https://api.warframe.market/v1/items/" + item + "/orders"
    raw = requests.get(url)
    if raw.status_code != 200:
      await ctx.send("Ordis覺得...指揮官是不是搞錯了什麼")
      return
    else:
      raw = json.loads(raw.text.encode(encoding='UTF-8'))
      raw = raw['payload']
      raw = raw['orders']
      orderList = raw
      itemName = requests.get(url.replace("/orders","")).text.encode(encoding='UTF-8')
      itemName = json.loads(itemName)
      itemName = itemName['payload']
      itemName = itemName['item']
      itemName = itemName['items_in_set']
      for item in itemName:
        itemName = item
        itemName = itemName['en']
        itemName = itemName['item_name']
        if itemSet == True:
          if "Set" in itemName:
            break
      for x in range(len(orderList)):
        for y in range(0, len(orderList) - x - 1):
          if (orderList[y]['platinum'] >orderList[y + 1]['platinum']):
            orderList[y], orderList[y + 1] = orderList[y + 1], orderList[y]
      message = f"以下為{items}的五個最低價賣家資料:\n"
      webhook = DiscordWebhook(url=jdata['webhook'],content=message)
      for orders in raw:
        if count > 0:
          user = orders['user']
          if orders['order_type'] == 'sell' and user['status'] == 'ingame' and orders['platform'] == 'pc':
            rank = orders.get("mod_rank","")
            if rank != "":
              ChiRank = f"等級:{rank}"
              rank = f"(rank {rank})"
            else:
              ChiRank = ""
            embed = DiscordEmbed(title=f"物品:{itemName}\t數量:{orders['quantity']}\t{ChiRank}",description=f"價格:{int(orders['platinum'])}")
            embed.add_embed_field(name="複製信息", value =f"/w {user['ingame_name']} Hi! I want to Buy: {itemName} {rank} for {int(orders['platinum'])} platinum. (warframe.market)")
            avatar = user['avatar']
            if avatar == None:
              avatar = "user/default-avatar.png"
            embed.set_author(name=user['ingame_name'], icon_url="https://warframe.market/static/assets/"+avatar, url = "https://warframe.market/zh-hant/profile/"+user['ingame_name'])
            webhook.add_embed(embed)
            count -= 1
      response = webhook.execute()

def setup(bot):
    bot.add_cog(wfm(bot))
