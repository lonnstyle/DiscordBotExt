import discord
from discord.ext import commands
from core.classes import Cog_Extension
import random
import json
from random import randint
import requests
import re
import asyncio
from language import language as lang

lang = lang()
lang = lang.langpref()['common']

with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

emoji = requests.get("http://gist.githubusercontent.com/Vexs/629488c4bb4126ad2a9909309ed6bd71/raw/416403f7080d1b353d8517dfef5acec9aafda6c3/emoji_map.json").text
emoji = json.loads(emoji)
emoji = {x: y for y, x in emoji.items()}

class common(Cog_Extension):
    tag = "common"
    #ping
    @commands.command(name= 'ping', aliases=lang['ping.aliases'],brief=lang['ping.brief'],description=lang['ping.description'])
    async def ping(self, ctx):
      latency = round(self.bot.latency*1000)
      red = max(0,min(int(255*(latency-50)/1000),255))
      green = 255-red
      color = discord.Colour.from_rgb(r=red,g=green,b=0)
      embed = discord.Embed(title=lang['ping.embed.title'],description=lang['ping.latency'].format(latency=latency),color=color)
      await ctx.send(embed=embed)

    #說
    @commands.command(name= 'sayd', aliases=lang['sayd.aliases'],brief=lang['sayd.brief'],description=lang['sayd.description'])
    async def sayd(self,ctx,*,msg):
        await ctx.message.delete()
        embed=discord.Embed(description=msg,color=0x3C879C)
        message = await ctx.send(embed=embed)
        if ctx.channel.id == jdata['publish']:
          await message.publish()
    
    @commands.command(name= 'poll', aliases=lang['poll.aliases'],brief=lang['poll.brief'],description=lang['poll.description'])
    async def poll(self,ctx,topic,option1,emoji1,option2,emoji2):
        await ctx.message.delete()
        match1 = re.match(r'<(a?):([a-zA-Z0-9\_]+):([0-9]+)>$', emoji1)
        match2 = re.match(r'<(a?):([a-zA-Z0-9\_]+):([0-9]+)>$', emoji2)
        if (emoji.get(emoji1,None)!=None or match1) and (emoji.get(emoji2,None)!=None or match2):
          if emoji1 == emoji2 or option1 == option2:
            await ctx.send(embed=discord.Embed(title=lang['poll.error.title'],description=lang['poll.error.description.same'],color=0xff0000))
            return
          embed=discord.Embed(description=topic,color=0x3C879C)
          embed.add_field(name=option1,value=emoji1)
          embed.add_field(name=option2,value=emoji2)
          message = await ctx.send(embed=embed)
          await message.add_reaction(emoji1)
          await message.add_reaction(emoji2)
        else:
          await ctx.send(embed=discord.Embed(title=lang['poll.error.title'],description=lang['poll.error.description.emoji']))

    
def setup(bot):
    bot.add_cog(common(bot))