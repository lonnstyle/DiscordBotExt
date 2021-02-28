from discord.ext import commands
from core.classes import Cog_Extension
import requests
import json
import discord
from discord_webhook import DiscordWebhook, DiscordEmbed

with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)


zhDict = requests.get("https://raw.githubusercontent.com/lonnstyle/DiscordBotMods/main/dict/items_zh-hant.json")
zhDict = json.loads(zhDict.text)
zhDictRev = zhDict
zhDict = {x: y for y, x in zhDict.items()}
enDict = requests.get("https://raw.githubusercontent.com/lonnstyle/DiscordBotMods/main/dict/items_en.json")
enDict = json.loads(enDict.text)
enDictRev = enDict
enDict = {x: y for y, x in enDict.items()}
Chinese_order_type = {'buy':'買','sell':'賣'}


class wfm(Cog_Extension):
  @commands.command(name='translate',aliases=['trans','翻譯'])
  async def translate(self,ctx,*args):
    item = ' '.join(args)
    url_name = enDict.get(item,item)
    language = ''
    if url_name == item:
      url_name = zhDict.get(item,item)
      if url_name == item:
        message = "Ordis沒找到指揮官說的物品呢"
        await ctx.send(message)
        return
      else:
        translate = enDictRev[url_name]
        language = "英文"
        print(translate+url_name)
    else:
      translate = zhDictRev.get(url_name,item)
      if translate == item:
        message = "Ordis也不太清楚翻譯是什麼呢"
        await ctx.send(message)
        return
      else:
        language = "中文"
    message = f"`{item}`  的{language}翻譯為  `{translate}`"
    await ctx.send(message)
  @commands.command(name='wfm', aliases=['wm', '市場查詢'])
  async def market(self, ctx, *args):
    if str(ctx.channel.type) != 'private':
      channel_id = ctx.channel.id
    else:
      channel_id = None
    action = 'buy'
    order_type = 'sell'
    itemrank = None
    args = ' '.join(args)
    if args.count(',')==0:
        items = args
    elif args.count(',')==1:
        if '買,'in args:
            args = args.replace('買,','')
        elif '賣,' in args:
            args = args.replace('賣,','')
            action = 'sell'
            order_type = 'buy'
        else:
            itemrank = args.split(',')[1]
            args = args.replace(f',{itemrank}','')
        items = args
    elif args.count(',')==2:
        order_type,items,itemrank = args.split(',')
        if order_type == '買':
            order_type = 'sell'
        elif order_type == '賣':
            order_type = 'buy'
            action = 'sell'
        else:
            await ctx.send('指揮官是要買還是賣呢？')
    else:
        await ctx.send("指揮官說的太多了,Ordis不是很懂呢")
    count = 5
    item = zhDict.get(items, items)
    if item == items:
      item = enDict.get(items,items)
    if item == items:
       item=item.replace(" ","_").lower()
    try: itemsDetail = json.loads(requests.get("https://api.warframe.market/v1/items/" + item).text.encode(encoding="UTF-8"))["payload"]["item"]["items_in_set"]
    except:
      await ctx.send("Ordis不太清楚指揮官說的什麼呢")
      return
    max_rank = None
    for itemDetail in itemsDetail:
      if "mod_max_rank" in itemDetail:
        if itemrank is not None:
          max_rank = int(itemDetail["mod_max_rank"])
          itemrank = int(itemrank)
          if itemrank > max_rank:
            await ctx.send("指揮官所輸入的等級超出物品最高等級呢 0.0") 
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
      for language in itemName:
        en = language['en']
        tc = language['zh-hant']
        if en["item_name"] == items or tc['item_name'] == items:
          itemName = language['en']
          itemName = itemName['item_name']
          break
      for x in range(len(orderList)):
        for y in range(0, len(orderList) - x - 1):
          if (orderList[y]['platinum'] >orderList[y + 1]['platinum']):
            orderList[y], orderList[y + 1] = orderList[y + 1], orderList[y]
      message = f"以下為{items}的五個最低價{Chinese_order_type[order_type]}家資料:\n"
      webhookID = jdata.get("webhook","Blank")
      webhookID = requests.get(webhookID)
      webhookID = json.loads(webhookID.text)
      webhookID = webhookID['channel_id']
      if eval(webhookID) == channel_id:
        print("true")
        webhook = DiscordWebhook(url=jdata['webhook'],content=message)
        for orders in raw:
          if count > 0:
            user = orders['user']
            if max_rank is not None:
              if orders['mod_rank'] != itemrank:
                continue
            if orders['order_type'] == order_type and user['status'] == 'ingame' and orders['platform'] == 'pc':
              rank = orders.get("mod_rank","")
              if rank != "":
                ChiRank = f"等級:{rank}"
                rank = f"(rank {rank})"
              else:
                ChiRank = ""
              embed = DiscordEmbed(title=f"物品:{itemName}\t數量:{orders['quantity']}\t{ChiRank}",description=f"價格:{int(orders['platinum'])}")
              embed.add_embed_field(name="複製信息", value = f"\n/w {user['ingame_name']} Hi! I want to {action}: {itemName} {rank} for {int(orders['platinum'])} platinum. (warframe.market)\n")
              avatar = user['avatar']
              if avatar == None:
                avatar = "user/default-avatar.png"
              embed.set_author(name=user['ingame_name'], icon_url="https://warframe.market/static/assets/"+avatar, url = "https://warframe.market/zh-hant/profile/"+user['ingame_name'])
              webhook.add_embed(embed)
              count -= 1
        response = webhook.execute()
      else:
        for orders in raw:
          if count > 0:
            user = orders['user']
            if max_rank is not None:
              if orders['mod_rank'] != itemrank:
                continue
            if orders['order_type'] == order_type and user['status'] == 'ingame' and orders['platform'] == 'pc':
              rank = orders.get("mod_rank","")
              if rank != "":
                ChiRank = f"等級:{rank}"
                rank = f"(rank {rank})"
              else:
                ChiRank = ""
              message+=f"```{Chinese_order_type[order_type]}\n玩家:{user['ingame_name']}\n物品:{itemName}\t數量:{orders['quantity']}\t{ChiRank}\n價格:{int(orders['platinum'])}\n"
              message+=f"複製信息\n/w {user['ingame_name']} Hi! I want to {action}: {itemName} {rank} for {int(orders['platinum'])} platinum. (warframe.market)```\n"
              count -= 1
        await ctx.send(message)
      

def setup(bot):
    bot.add_cog(wfm(bot))
