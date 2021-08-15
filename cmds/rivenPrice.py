import discord
from discord.ext import commands
from core.classes import Cog_Extension
import os
import requests
import json
from discord_webhook import DiscordWebhook,DiscordEmbed
from language import language as lang

lang = lang()
lang = lang.langpref()['rivenPrice']

temp = {}
weapons = json.loads(requests.get("http://api.warframe.market/v1/riven/items",headers=lang['api.header']).text)
weapons = weapons['payload']['items']
for item in weapons:
  temp[item['item_name']]=item['url_name']
weapons = temp
temp = {}
attrDict = json.loads(requests.get("http://api.warframe.market/v1/riven/attributes",headers=lang['api.header']).text)
attrDict = attrDict['payload']['attributes']
for attr in attrDict:
  temp[attr['url_name']]=attr['effect']
attrDict=temp

with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)


class rivenPrice(Cog_Extension):
  tag = "Warframe"
  @commands.command(name='riven',aliases=lang['riven.aliases'],brief=lang['riven.brief'],description=lang['riven.description'])
  async def rivenPrice(self,ctx,*weapon):
    name = ' '.join(weapon)
    name = name.title()
    userInput= name
    weapon = weapons.get(name, "Empty")
    if weapon == "Empty":
      weapon = name
    weapon = weapon.lower().replace(" ","_")
    url = 'https://api.warframe.market/v1/auctions/search?type=riven&weapon_url_name=' + weapon + '&sort_by=price_asc'
    html = requests.get(url)
    weapon = weapon.replace("_"," ")
    if html.status_code != 200:
      await ctx.send(embed=discord.Embed(title=lang['riven.error.title'],description=lang['riven.error.description'].format(self=jdata['self']),color=0xff0000))
      return()
    else:
      rivenData = json.loads(html.text)
      rivenData = rivenData['payload']
      rivenData = rivenData['auctions']
      count = 0
      if str(ctx.channel.type) != 'private':
        channel_id = ctx.channel.id
      else:
        channel_id = None
      webhookID = jdata.get("webhook","Blank")
      webhookID = requests.get(webhookID)
      webhookID = json.loads(webhookID.text)
      webhookID = webhookID['channel_id']
      message = lang['riven.message.title'].format(userInput=userInput)
      webhook = DiscordWebhook(url=jdata['webhook'],content=message)
      for items in rivenData:
        if count < 3:
          owner = items['owner']
          if owner['status'] != 'offline':
            rivenItem = items['item']
            rivenName = rivenItem['name']
            message += lang['riven.message.rivenName'].format(userInput=userInput,rivenName=rivenName)
            ownerName = owner['ingame_name']
            avatar = owner['avatar']
            if avatar == None:
              avatar = "user/default-avatar.png"
            message += lang['riven.message.owner'].format(ownerName=ownerName)
            rank = rivenItem['mod_rank']
            rerolls = rivenItem['re_rolls']
            message += lang['riven.message.rank'].format(rank=rank)
            message += lang['riven.message.reroll'].format(rerolls=rerolls)
            embed = DiscordEmbed(title=lang['riven.embed.title'].format(userInput=userInput,rivenName=rivenName),description=lang['riven.embed.description'].format(rank=rank,rerolls=rerolls),color=0xb59dd4)
            embed.set_author(name=ownerName, icon_url="https://warframe.market/static/assets/"+avatar, url = f"https://warframe.market/{lang['riven.link.language']}/profile/"+ownerName)
            if items['top_bid'] == 'None':
              top_bid = items['top_bid']
              message += lang['riven.message.topbid'].format(top_bid=top_bid)
              embed.add_embed_field(name=lang['riven.embed.field.topbid'],value=top_bid)
            else:
              starting_price = items['starting_price']
              buyout_price = items['buyout_price']
              if starting_price == buyout_price:
                message += lang['riven.message.price'].format(buyout_price=buyout_price)
                embed.add_embed_field(name=lang['riven.embed.field.price'],value=buyout_price)
              else:
                message += lang['riven.message.starting'].format(starting_price=starting_price)
                message += lang['riven.message.buyout'].format(buyout_price=buyout_price)
                embed.add_embed_field(name=lang['riven.embed.field.starting'],value=starting_price,inline=False)
                embed.add_embed_field(name=lang['riven.embed.field.buyout'],value=buyout_price,inline=False)
            positive = ''
            negative = ''
            for attr in rivenItem['attributes']:
              attribute = attr['url_name']
              attribute = attrDict.get(attribute,attribute)
              value = attr['value']
              if attr['positive'] == True:
                message += lang['riven.message.attr.pos'].format(attribute=attribute,value=value)
                positive += f'{attribute} {value}\n'
              elif attr['positive'] == False:
                message += lang['riven.message.attr.neg'].format(attribute=attribute,value=value)
                negative = f'{attribute} {value}'
            embed.add_embed_field(name=lang['riven.embed.attr.pos'],value=positive[:-1])
            if negative != '':
              embed.add_embed_field(name=lang['riven.embed.attr.neg'],value=negative)
            count += 1
            message += '```'
            webhook.add_embed(embed)
      if eval(webhookID) == channel_id:
        response = webhook.execute()
      else:  
        await ctx.send(message)

def setup(bot):
    bot.add_cog(rivenPrice(bot))