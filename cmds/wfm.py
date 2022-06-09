import json
import logging
import os

import discord
import requests
from discord.ext import commands
from discord_webhook import DiscordEmbed, DiscordWebhook

from core.classes import Cog_Extension
# from discord_slash.utils.manage_commands import create_option, create_choice
# from discord_slash import SlashContext,cog_ext
from localization import lang

lang = lang.langpref()['wfm']

dirname = os.path.dirname(__file__)

with open(os.path.join(dirname, '../setting.json'), 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

logger = logging.getLogger('wfm')
logger.setLevel(-1)
handler = logging.FileHandler(filename=os.path.join(dirname, '../log/runtime.log'),  encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(lineno)d: %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
logger.addHandler(handler)

localDict = requests.get("http://api.warframe.market/v1/items", headers=lang['api.header'])
localDict = json.loads(localDict.text)
temp = {}
localDict = localDict['payload']['items']
for item in localDict:
    temp[item['item_name']] = item['url_name']
localDict = temp
enDict = requests.get("http://api.warframe.market/v1/items")
enDict = json.loads(enDict.text)
temp = {}
enDict = enDict['payload']['items']
for item in enDict:
    temp[item['item_name']] = item['url_name']
enDict = temp
localDictRev = localDict
enDictRev = enDict
localDictRev = {x: y for y, x in localDictRev.items()}
enDictRev = {x: y for y, x in enDictRev.items()}
local_order_type = lang['local_order_type']
price_order = lang['price_order']


class wfm(Cog_Extension):
    tag = "Warframe"

    @commands.command(name='translate', aliases=lang['translate.aliases'], brief=lang['translate.brief'], description=lang['translate.description'])
    async def translate(self, ctx, *item):
        item = ' '.join(word.capitalize() for word in (item))
        url_name = enDict.get(item, item)
        language = ''
        if url_name == item:
            url_name = localDict.get(item, item)
            if url_name == item:
                message = lang['translate.error.notFound'].format(self=jdata['self'], user=jdata['user'])
                await ctx.send(message)
                return
            else:
                translate = enDictRev[url_name]
                language = lang['translate.language.en']
        else:
            translate = localDictRev.get(url_name, item)
            if translate == item:
                message = lang['translate.error.noTrans'].format(self=jdata['self'])
                await ctx.send(message)
                logger.warning(f'[translate] failed to search translation for {item}')
                return
            else:
                language = lang['translate.language.local']
        message = lang['translate.translate.message'].format(item=item, language=language, translate=translate)
        await ctx.send(message)

    # @cog_ext.cog_slash(name="translate",description=lang['translate.description'],options=[create_option(name="item",description=lang["translate.options.item"],option_type=3,required=True)],guild_ids=[815462037840330762])
    # async def slash_translate(self,ctx,item):
    #   await self.translate(ctx,item)

    @commands.command(name='wfm', aliases=lang['wfm.aliases'], brief=lang['wfm.brief'], description=lang['wfm.description'])
    async def market(self, ctx, *args):
        if str(ctx.channel.type) != 'private':
            channel_id = ctx.channel.id
        else:
            channel_id = None
        action = 'buy'
        order_type = 'sell'
        itemrank = None
        args = ' '.join(args)
        if args.count(',') == 0:
            items = args
        elif args.count(',') == 1:
            if (lang['wfm.buy']+',') in args:
                args = args.replace((lang['wfm.buy']+','), '')
            elif (lang['wfm.sell']+',') in args:
                args = args.replace((lang['wfm.sell']+','), '')
                action = 'sell'
                order_type = 'buy'
            else:
                itemrank = args.split(',')[1]
                args = args.replace(f',{itemrank}', '')
            items = args
        elif args.count(',') == 2:
            order_type, items, itemrank = args.split(',')
            if order_type == lang['wfm.buy']:
                order_type = 'sell'
            elif order_type == lang['wfm.sell']:
                order_type = 'buy'
                action = 'sell'
            else:
                await ctx.send(lang['wfm.error.unknownOrder'].format(user=jdata['user']))
                logger.warning(f'[market] failed to search orders for {args}')
        else:
            await ctx.send(lang['wfm.error.tooManyArgs'].format(user=jdata['user'], self=jdata['self']))
            logger.warning(f'[market] too many arguments: {args}')
        count = 5
        items = ' '.join(word.capitalize() for word in (items.split()))
        item = localDict.get(items, items)
        if item == items:
            item = enDict.get(items, items)
        if item == items:
            item = item.replace(" ", "_").lower()
        try:
            itemsDetail = json.loads(requests.get("https://api.warframe.market/v1/items/" + item).text.encode(encoding="UTF-8"))["payload"]["item"]["items_in_set"]
        except:
            await ctx.send(lang["wfm.error.unknownItem"].format(self=jdata['self']))
            logger.warning(f'[market] failed to search orders for {args}')
            return
        max_rank = None
        for itemDetail in itemsDetail:
            if "mod_max_rank" in itemDetail:
                if itemrank is not None:
                    max_rank = int(itemDetail["mod_max_rank"])
                    itemrank = int(itemrank)
                    if itemrank > max_rank:
                        await ctx.send(lang["wfm.error.outOfRank"].format(user=jdata['user']))
                        logger.warning(f"[market] {item}'s maxrank is {max_rank} while attempting to search rank{itemrank}")
                        return
        url = "https://api.warframe.market/v1/items/" + item + "/orders"
        raw = requests.get(url)
        if raw.status_code != 200:
            await ctx.send(lang["wfm.error.API"].format(self=jdata['self'], user=jdata['user']))
            logger.warning(f'[market] failed to search item info, cuz {raw.status_code} {raw.reason}')
            return
        else:
            raw = json.loads(raw.text.encode(encoding='UTF-8'))
            raw = raw['payload']
            raw = raw['orders']
            orderList = raw
            itemName = requests.get(url.replace("/orders", "")).text.encode(encoding='UTF-8')
            itemName = json.loads(itemName)
            itemName = itemName['payload']
            itemName = itemName['item']
            itemName = itemName['items_in_set']
            for language in itemName:
                en = language['en']
                tc = language['zh-hant']
                tax = language['trading_tax']
                ducats = language.get("ducats", None)
                if ducats != None:
                    ducats = lang['wfm.ducats'].format(ducats=ducats)
                else:
                    ducats = ""
                if en["item_name"] == items or tc['item_name'] == items:
                    itemName = language['en']
                    itemName = itemName['item_name']
                    break
            for x in range(len(orderList)):
                for y in range(0, len(orderList) - x - 1):
                    if (orderList[y]['platinum'] > orderList[y + 1]['platinum']):
                        orderList[y], orderList[y + 1] = orderList[y + 1], orderList[y]
            if action == "sell":
                for x in range(1, round(len(orderList)/2)):
                    orderList[x], orderList[len(orderList)-x] = orderList[len(orderList)-x], orderList[x]
            message = lang["wfm.message.title"].format(items=items, order=price_order[action], order_type=local_order_type[order_type])
            webhookID = jdata.get("webhook", "Blank")
            if webhookID != "Blank":
                webhookID = requests.get(webhookID)
                webhookID = json.loads(webhookID.text)
                webhookID = webhookID['channel_id']
            if webhookID != "Blank" and eval(webhookID) == channel_id:
                webhook = DiscordWebhook(url=jdata['webhook'], content=message)
                for orders in raw:
                    if count > 0:
                        user = orders['user']
                        if max_rank is not None:
                            if orders['mod_rank'] != itemrank:
                                continue
                        if orders['order_type'] == order_type and user['status'] == 'ingame' and orders['platform'] == 'pc' and orders['visible']:
                            rank = orders.get("mod_rank", "")
                            if rank != "":
                                localRank = lang['wfm.rank'].format(rank=rank)
                                rank = f"(rank {rank})"
                            else:
                                localRank = ""
                            embed = DiscordEmbed(title=lang['wfm.embed.title'].format(itemName=items, quantity=orders['quantity'], localRank=localRank, tax=tax,
                                                 ducats=ducats), description=lang['wfm.embed.description'].format(platinum=int(orders['platinum'])), color=0x3b859a)
                            embed.add_embed_field(
                                name=lang["wfm.embed.field.cpMsg"],
                                value=f"\n/w {user['ingame_name']} Hi! I want to {action}: {itemName} {rank} for {int(orders['platinum'])} platinum. (warframe.market)\n")
                            avatar = user['avatar']
                            if avatar == None:
                                avatar = "user/default-avatar.png"
                            embed.set_author(name=user['ingame_name'], icon_url="https://warframe.market/static/assets/"+avatar,
                                             url=f"https://warframe.market/{lang['wfm.link.language']}/profile/"+user['ingame_name'])
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
                        if orders['order_type'] == order_type and user['status'] == 'ingame' and orders['platform'] == 'pc' and orders['visible']:
                            rank = orders.get("mod_rank", "")
                            if rank != "":
                                localRank = lang['wfm.rank'].format(rank=rank)
                                rank = f"(rank {rank}) "
                            else:
                                localRank = ""
                            message += lang['wfm.message.item'].format(user=user['ingame_name'], itemName=items, quantity=orders['quantity'],
                                                                       localRank=localRank, platinum=int(orders['platinum']), tax=tax, ducats=ducats)
                            message += lang['wfm.message.cpMsg']+f"/w {user['ingame_name']} Hi! I want to {action}: {itemName} {rank}for {int(orders['platinum'])} platinum. (warframe.market)```\n"
                            count -= 1
                await ctx.send(message)


def setup(bot):
    bot.add_cog(wfm(bot))
