from discord.ext import commands
from core.classes import Cog_Extension
from core.time import time_info
from datetime import datetime,timedelta
import json
import os
import requests
import re
import discord
import asyncio
from language import language as lang

lang = lang()
lang = lang.langpref()['event']

with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

emojimap = requests.get("http://gist.githubusercontent.com/Vexs/629488c4bb4126ad2a9909309ed6bd71/raw/416403f7080d1b353d8517dfef5acec9aafda6c3/emoji_map.json").text
emojimap = json.loads(emojimap)
emojimap = {x: y for y, x in emojimap.items()}

class event(Cog_Extension):
  tag = "common"
  @commands.command(name="reactionRole", aliases=["rr"],brief="指定自動身份組訊息",description="指定可自動分發身份組的訊息")
  async def rr(self,ctx,message:int):
    with open("role/rr.txt","a") as rr:
      rr.write(f"{message}\n")
      await ctx.message.add_reaction("✅")
      await ctx.message.delete(delay=5)
   

  @commands.command(name='role', aliases=lang['role.aliases'],brief=lang['role.brief'],description=lang['role.description'])
  async def role(self,ctx,role:str,emoji):
    match = re.match(r'<(a?):([a-zA-Z0-9\_]+):([0-9]+)>$', emoji)
    if (emojimap.get(emoji,None)!=None or match) and ctx.author.guild_permissions.administrator == True:
      with open("role/roles.txt","a") as roles:
        roles.write(f"{emoji},{role}\n")
      await ctx.message.add_reaction("✅")
      await ctx.message.delete(delay=5)
    else:
      await ctx.message.delete()
      await ctx.send(embed=discord.Embed(title=lang['role.error.title'],description=lang['role.error.description']))

  @commands.Cog.listener()
  async def on_raw_reaction_add(self,payload): 
    roles = {}
    message = []
    raw = open("role/roles.txt","r")
    rr = open("role/rr.txt","r")
    for line in raw.readlines():
      emoji,role = line.split(",")
      roles[emoji] = role.replace("\n","")
    for line in rr.readlines():
      message.append(line.replace("\n",""))
    for role in payload.member.guild.roles:
      if (role.name == roles.get(payload.emoji.name) or role.name == roles.get(f"<:{payload.emoji.name}:{payload.emoji.id}>")) and str(payload.message_id) in message:
        await payload.member.add_roles(role)
  
  @commands.Cog.listener()
  async def on_raw_reaction_remove(self,payload):
    roles = {}
    message = []
    raw = open("role/roles.txt","r")
    rr = open("role/rr.txt","r")
    for line in raw.readlines():
      emoji,role = line.split(",")
      roles[emoji] = role.replace("\n","")
    for line in rr.readlines():
      message.append(line.replace("\n",""))
    guild = await self.bot.fetch_guild(payload.guild_id)
    member = await guild.fetch_member(payload.user_id)
    for role in member.roles:
      if (role.name == roles.get(payload.emoji.name) or role.name == roles.get(f"<:{payload.emoji.name}:{payload.emoji.id}>")) and str(payload.message_id) in message:
        await member.remove_roles(role)

  @commands.Cog.listener()
  async def on_ready(self):
    print("working")
    bot = self.bot
    vc1 = bot.get_channel(822681456437362712)
    vc2 = bot.get_channel(823548462896644166)
    vc3 = bot.get_channel(823548483797385256)
    while True:
      if vc1.members == [] and vc2.members == [] and vc3.members == []:
        text = bot.get_channel(824462815900205097)
        async for message in text.history(limit=1):
          if message != None:
            lonns = bot.get_user(535295352115560488)
            await lonns.send(message)
            await text.purge(limit=100, bulk=True)
      await asyncio.sleep(300)
   

def setup(bot):
  if not os.path.exists('log'):
    os.mkdir('log')
  bot.add_cog(event(bot))