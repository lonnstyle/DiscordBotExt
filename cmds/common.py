import discord
from discord.ext import commands
from core.classes import Cog_Extension
import random
import json
from random import randint
import requests
import re
import asyncio


with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

emoji = requests.get("http://gist.githubusercontent.com/Vexs/629488c4bb4126ad2a9909309ed6bd71/raw/416403f7080d1b353d8517dfef5acec9aafda6c3/emoji_map.json").text
emoji = json.loads(emoji)
emoji = {x: y for y, x in emoji.items()}

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
        #此功能為開發伺服器上公告自動廣播之用
        if ctx.channel.id == 820571680479903776:
          await message.publish()
    
    @commands.command(name= 'poll', aliases=['投票'],brief="發起投票",description="讓機器人發起一項投票")
    async def poll(self,ctx,topic,option1,emoji1,option2,emoji2):
        await ctx.message.delete()
        match1 = re.match(r'<(a?):([a-zA-Z0-9\_]+):([0-9]+)>$', emoji1)
        match2 = re.match(r'<(a?):([a-zA-Z0-9\_]+):([0-9]+)>$', emoji2)
        if (emoji.get(emoji1,None)!=None or match1) and (emoji.get(emoji2,None)!=None or match2):
          if emoji1 == emoji2 or option1 == option2:
            await ctx.send(embed=discord.Embed(title="錯誤信息",description='兩個一樣你要投什麼?',color=0xff0000))
            return
          embed=discord.Embed(description=topic,color=0x3C879C)
          embed.add_field(name=option1,value=emoji1)
          embed.add_field(name=option2,value=emoji2)
          message = await ctx.send(embed=embed)
          await message.add_reaction(emoji1)
          await message.add_reaction(emoji2)
        else:
          await ctx.send(embed=discord.Embed(title="錯誤信息",description='這真的是emoji嗎?'))

    @commands.command(name="role",brief="新增身份組",description="新增機器人可以分發的身份組")
    async def role(self,ctx,role):
      if ctx.message.author.id == ctx.guild.owner_id:
          for roles in ctx.guild.roles:
            if roles.name == role:
              embed = discord.Embed(title="已新增身份組",description=f"已新增<@&{roles.id}>")
              await ctx.send(embed=embed)
              with open("roles.txt","a",encoding="utf8") as role_id:
                role_id.write(roles.name+'\n')

    @commands.command(name="join",brief="加入身份組",description="使機器人分配身份組權限")
    async def join(self,ctx,role):
      await ctx.message.delete()
      with open("roles.txt","r",encoding="utf8") as roles:
        if (role+'\n') in roles.readlines():
          for roles in ctx.guild.roles:
            if roles.name == role:
              await ctx.author.add_roles(roles)
              message = await ctx.send(embed=discord.Embed(title="已加入身份組",description=f"<@&{roles.id}>",color=0x00ff00))
              await asyncio.sleep(10)
              message.delete()
        else:
          message = await ctx.send(embed=discord.Embed(title="加入身份組失敗",description="請確保身份組輸入無誤",color=0xff0000))
          await asyncio.sleep(10)
          message.delete()
    
def setup(bot):
    bot.add_cog(common(bot))
