import discord
from discord.ext import commands
from core.classes import Cog_Extension
import os
import requests
import json
from discord_webhook import DiscordWebhook,DiscordEmbed

weapons = json.loads(requests.get("https://raw.githubusercontent.com/lonnstyle/DiscordBotMods/main/dict/Weapons.json").text)
weapons = {x: y for y, x in weapons.items()}
attrDict = json.loads(requests.get("https://raw.githubusercontent.com/lonnstyle/DiscordBotMods/main/dict/attributes.json").text)

with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)


class rivenPrice(Cog_Extension):
  tag = "Warframe"
  @commands.command(name='riven',aliases=['紫卡','紫卡查詢'],brief="查詢裂罅價格",description="查詢`weapon`裂罅價格")
  async def rivenPrice(self,ctx,*weapon):
    name = ' '.join(weapon)
    Chinese= name
    weapon = weapons.get(name, "Empty")
    if weapon == "Empty":
      weapon = name
    weapon = weapon.lower().replace(" ","_")
    url = 'https://api.warframe.market/v1/auctions/search?type=riven&weapon_url_name=' + weapon + '&sort_by=price_asc'
    html = requests.get(url)
    weapon = weapon.replace("_"," ")
    if html.status_code != 200:
      return('查到...Ordis發生錯誤...API出錯！')
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
      message = f'以下為{Chinese}紫卡的查詢結果（按價格由低至高順序）\n'
      webhook = DiscordWebhook(url=jdata['webhook'],content=message)
      for items in rivenData:
        if count < 3:
          owner = items['owner']
          if owner['status'] != 'offline':
            rivenItem = items['item']
            rivenName = rivenItem['name']
            message += f'```\n紫卡名稱:{Chinese} {rivenName}\n'
            ownerName = owner['ingame_name']
            avatar = owner['avatar']
            if avatar == None:
              avatar = "user/default-avatar.png"
            message += f'賣家:{ownerName}\n'
            rank = rivenItem['mod_rank']
            rerolls = rivenItem['re_rolls']
            message += f'等級:{rank}\n'
            message += f'迴圈次數:{rerolls}\n'
            embed = DiscordEmbed(title=f"紫卡名稱:{Chinese} {rivenName}",description=f'等級:{rank}    迴圈次數:{rerolls}',color=0xb59dd4)
            embed.set_author(name=ownerName, icon_url="https://warframe.market/static/assets/"+avatar, url = "https://warframe.market/zh-hant/profile/"+ownerName)
            if items['top_bid'] == 'None':
              top_bid = items['top_bid']
              message += f'目前競標:{top_bid}\n'
              embed.add_embed_field(name="目前競標:",value=top_bid)
            else:
              starting_price = items['starting_price']
              buyout_price = items['buyout_price']
              if starting_price == buyout_price:
                message += f'價格:{buyout_price}\n'
                embed.add_embed_field(name="價格:",value=buyout_price)
              else:
                message += f'起標價格:{starting_price}\n'
                message += f'買斷價格:{buyout_price}\n'
                embed.add_embed_field(name="價格:",value=buyout_price,inline=False)
            positive = ''
            negative = ''
            for attr in rivenItem['attributes']:
              attribute = attr['url_name']
              attribute = attrDict.get(attribute,attribute)
              value = attr['value']
              if attr['positive'] == True:
                message += f'正面詞條:{attribute} {value}\n'
                positive += f'{attribute} {value}\n'
              elif attr['positive'] == False:
                message += f'負面詞條:{attribute} {value}\n'
                negative = f'{attribute} {value}'
            embed.add_embed_field(name="正面詞條:",value=positive[:-1])
            if negative != '':
              embed.add_embed_field(name="負面詞條:",value=negative)
            count += 1
            message += '```'
            webhook.add_embed(embed)
      if eval(webhookID) == channel_id:
        response = webhook.execute()
      else:  
        await ctx.send(message)

      
def setup(bot):
    bot.add_cog(rivenPrice(bot))