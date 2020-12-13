from discord.ext import commands
from core.classes import Cog_Extension
import requests
import json

localDict = requests.get(
    "https://raw.githubusercontent.com/lonnstyle/DiscordBotMods/main/dict/items_zh-hant.json"
)
localDict = json.loads(localDict.text)
localDict = {x: y for y, x in localDict.items()}
enDict = requests.get("https://raw.githubusercontent.com/lonnstyle/DiscordBotMods/main/dict/items_en.json")
enDict = json.loads(enDict.text)
enDict = {x: y for y, x in enDict.items()}


class wfm(Cog_Extension):
    @commands.command(name='wfm', aliases=['wm', '市場查詢'])
    async def market(self, ctx, *args):
        msg = self.item(' '.join(args))
        await ctx.send(msg)

    def item(self, items):
        count = 5
        item = localDict.get(items, items)
        if item == items:
          item = enDict.get(items,items)
        if item == items:
          return("Ordis不太清楚指揮官說的什麼呢")        
        url = "https://api.warframe.market/v1/items/" + item + "/orders"
        raw = requests.get(url)
        if raw.status_code != 200:
            print(item)
            return ("Ordis覺得...指揮官是不是搞錯了什麼")
        else:
            raw = json.loads(raw.text)
            raw = raw['payload']
            raw = raw['orders']
            orderList = raw
            for x in range(len(orderList)):
                for y in range(0, len(orderList) - x - 1):
                    if (orderList[y]['platinum'] >
                            orderList[y + 1]['platinum']):
                        orderList[y], orderList[y + 1] = orderList[
                            y + 1], orderList[y]
            message = f"以下為{items}的五個最低價賣家資料:\n```"
            for orders in raw:
                if count > 0:
                    user = orders['user']
                    if orders['order_type'] == 'sell' and user[
                            'status'] == 'ingame' and orders[
                                'platform'] == 'pc':
                        message += f"價格:{int(orders['platinum'])}\t賣家:{user['ingame_name']}\n"
                        count -= 1
            message += '```'
        return (message)

    @commands.command(name='reloadDict')
    async def reload(self, ctx):
        msg = self.load()
        await ctx.send(msg)

    def load():
      localDict = requests.get("https://raw.githubusercontent.com/lonnstyle/DiscordBotMods/main/dict/items_zh-hant.json")
      localDict = json.loads(localDict.text)
      localDict = {x: y for y, x in localDict.items()}
      return ("已重新載入Dict")


def setup(bot):
    bot.add_cog(wfm(bot))
