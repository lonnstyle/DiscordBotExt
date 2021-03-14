import discord
from discord.ext import commands
from core.classes import Cog_Extension
import random
import json
from random import randint


with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

class common(Cog_Extension):
    tag = "common"
    #ping
    @commands.command(name= 'ping', aliases=['延遲' , '機器人延遲' , 'delay'],brief="測試延遲",description="顯示當前機器人處理信息的延遲值")
    async def ping(self, ctx):
      latency = round(self.bot.latency*1000)
      red = max(0,min(int(255*(latency-50)/1000),255))
      green = 255-red
      color = discord.Colour.from_rgb(r=red,g=green,b=0)
      embed = discord.Embed(title="當前本機延遲為",description=f'{latency} 毫秒 (ms)',color=color)
      await ctx.send(embed=embed)

    #說
    @commands.command(name= 'sayd', aliases=['說' , '機器人說'],brief="復讀",description="讓機器人代替你說出`msg`的內容")
    async def sayd(self,ctx,*,msg):
        await ctx.message.delete()
        embed=discord.Embed(description=msg,color=0x3C879C)
        message = await ctx.send(embed=embed)
    
    @commands.command(name= 'poll', aliases=['投票'],brief="發起投票",description="讓機器人發起一項投票")
    async def poll(self,ctx,topic,option1,emoji1,option2,emoji2):
        await ctx.message.delete()
        embed=discord.Embed(description=topic,color=0x3C879C)
        embed.add_field(name=option1,value=emoji1)
        embed.add_field(name=option2,value=emoji2)
        message = await ctx.send(embed=embed)
        await message.add_reaction(emoji1)
        await message.add_reaction(emoji2)

    
def setup(bot):
    bot.add_cog(common(bot))