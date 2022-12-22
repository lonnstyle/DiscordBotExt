import json
import logging
import os

import discord
import requests
from core.classes import Cog_Extension,Hybirdcmd_Aliases
from discord.ext import commands
from discord_webhook import DiscordEmbed, DiscordWebhook
from localization import lang
from thefuzz import process

lang = lang.langpref()['rivenPrice']

dirname = os.path.dirname(__file__)

temp = {}
localWeapons = json.loads(requests.get("http://api.warframe.market/v1/riven/items", headers=lang['api.header']).text)
localWeapons = localWeapons['payload']['items']
for item in localWeapons:
    temp[item['item_name']] = item['url_name']
localWeapons = temp
temp = {}
Weapons = json.loads(requests.get("http://api.warframe.market/v1/riven/items").text)
Weapons = Weapons['payload']['items']
for item in Weapons:
    temp[item['item_name']] = item['url_name']
Weapons = temp
temp = {}
attrDict = json.loads(requests.get("http://api.warframe.market/v1/riven/attributes", headers=lang['api.header']).text)
attrDict = attrDict['payload']['attributes']
for attr in attrDict:
    temp[attr['url_name']] = attr['effect']
attrDict = temp

logger = logging.getLogger('rivenPrice')
logger.setLevel(-1)
handler = logging.FileHandler(filename=os.path.join(dirname, '../log/runtime.log'),  encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(lineno)d: %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
logger.addHandler(handler)

with open(os.path.join(dirname, '../setting.json'), 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

cmds = ['riven']
hybirdAliases = Hybirdcmd_Aliases(lang, *cmds)

class rivenPrice(Cog_Extension):
    @hybirdAliases.hyb_cmd
    async def rivenPrice(self, ctx, weapon):
        name = ' '.join(weapon)
        name = name.title()
        weapon, ratio = process.extractOne(name, localWeapons.keys())
        if ratio < 75:
            weapon, ratio = process.extractOne(name, Weapons.keys())
            if ratio < 75:
                embed = discord.Embed(title=lang['riven.error.title'], description=lang['riven.error.description'].format(self=jdata['self']), color=0xff0000)
                logger.warning(f'[riven] failed to search weapon: {name}')
                for match, score in process.extractBests(name, localWeapons.keys()):
                    if score > 50:
                        embed.add_field(name=match, value=score, inline=False)
                        logger.info(f'[riven] suggested weapon name: {match}')
                await ctx.send(embed=embed)
            else:
                name = weapon
                weapon = Weapons[weapon]
        else:
            name = weapon
            weapon = localWeapons[weapon]
        logger.info(f'[riven] searching weapon: {weapon}')
        url = 'https://api.warframe.market/v1/auctions/search?type=riven&weapon_url_name=' + weapon + '&sort_by=price_asc'
        html = requests.get(url)
        weapon = weapon.replace("_", " ")
        if html.status_code != 200:
            await ctx.send(embed=discord.Embed(title=lang['riven.error.title'],
                                               description=lang['riven.error.description'].format(self=jdata['self']),
                                               color=0xff0000))
            logger.error(f'[riven] failed to search {weapon}, status code: {html.status_code}, reason: {html.reason}')
            return ()
        else:
            rivenData = json.loads(html.text)
            rivenData = rivenData['payload']
            rivenData = rivenData['auctions']
            count = 0
            if str(ctx.channel.type) != 'private':
                channel_id = ctx.channel.id
            else:
                channel_id = None
            webhookID = jdata.get("webhook", "Blank")
            webhookID = requests.get(webhookID)
            webhookID = json.loads(webhookID.text)
            webhookID = webhookID['channel_id']
            message = lang['riven.message.title'].format(userInput=name)
            webhook = DiscordWebhook(url=jdata['webhook'], content=message)
            for items in rivenData:
                if count < 3:
                    owner = items['owner']
                    if owner['status'] != 'offline':
                        rivenItem = items['item']
                        rivenName = rivenItem['name']
                        message += lang['riven.message.rivenName'].format(userInput=name, rivenName=rivenName)
                        ownerName = owner['ingame_name']
                        avatar = owner['avatar']
                        if avatar == None:
                            avatar = "user/default-avatar.png"
                        message += lang['riven.message.owner'].format(ownerName=ownerName)
                        rank = rivenItem['mod_rank']
                        rerolls = rivenItem['re_rolls']
                        message += lang['riven.message.rank'].format(rank=rank)
                        message += lang['riven.message.reroll'].format(rerolls=rerolls)
                        embed = DiscordEmbed(
                            title=lang['riven.embed.title'].format(userInput=name, rivenName=rivenName),
                            description=lang['riven.embed.description'].format(rank=rank, rerolls=rerolls),
                            color=0xb59dd4)
                        embed.set_author(name=ownerName, icon_url="https://warframe.market/static/assets/" + avatar,
                                         url=f"https://warframe.market/{lang['riven.link.language']}/profile/" + ownerName)
                        if items['top_bid'] == 'None':
                            top_bid = items['top_bid']
                            message += lang['riven.message.topbid'].format(top_bid=top_bid)
                            embed.add_embed_field(name=lang['riven.embed.field.topbid'], value=top_bid)
                        else:
                            starting_price = items['starting_price']
                            buyout_price = items['buyout_price']
                            if starting_price == buyout_price:
                                message += lang['riven.message.price'].format(buyout_price=buyout_price)
                                embed.add_embed_field(name=lang['riven.embed.field.price'], value=buyout_price)
                            else:
                                message += lang['riven.message.starting'].format(starting_price=starting_price)
                                message += lang['riven.message.buyout'].format(buyout_price=buyout_price)
                                embed.add_embed_field(name=lang['riven.embed.field.starting'], value=starting_price,
                                                      inline=False)
                                embed.add_embed_field(name=lang['riven.embed.field.buyout'], value=buyout_price,
                                                      inline=False)
                        positive = ''
                        negative = ''
                        for attr in rivenItem['attributes']:
                            attribute = attr['url_name']
                            attribute = attrDict.get(attribute, attribute)
                            value = attr['value']
                            if attr['positive'] == True:
                                message += lang['riven.message.attr.pos'].format(attribute=attribute, value=value)
                                positive += f'{attribute} {value}\n'
                            elif attr['positive'] == False:
                                message += lang['riven.message.attr.neg'].format(attribute=attribute, value=value)
                                negative = f'{attribute} {value}'
                        embed.add_embed_field(name=lang['riven.embed.attr.pos'], value=positive[:-1])
                        if negative != '':
                            embed.add_embed_field(name=lang['riven.embed.attr.neg'], value=negative)
                        count += 1
                        message += '```'
                        webhook.add_embed(embed)
            if eval(webhookID) == channel_id:
                response = webhook.execute()
                logger.info(f"[rivenPrice] sent riven price data of {weapon} to channel {channel_id} as webhook")
            else:
                logger.info(f"[rivenPrice] sent riven price data of {weapon} to channel {channel_id}")
                await ctx.send(message)


async def setup(bot):
    await bot.add_cog(rivenPrice(bot))
