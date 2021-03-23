import discord
from discord.ext import commands
from core.classes import Cog_Extension
import os
import json
from language import language as lang

lang = lang()
lang = lang.langpref()['event']

with open('setting.json','r',encoding='utf8') as jset:
    jdata = json.load(jset)

loglist = []
logindex = 0
for logname in os.listdir('./log'):
    if logname.endswith('.txt'):
        loglist.append(logindex)
        loglist.append(logname)
        logindex += 1
logindex = 0

class logup(Cog_Extension):
  tag = "common"
  @commands.command()
  async def loglist(self,ctx):
    if await self.bot.is_owner(ctx.message.author):
      msg = ''
      dou = 0
      for i in loglist:
        if dou == 0:
          msg = msg + str(i)+' , '
          dou+=1
        else:
          msg = msg + str(i)[:-4] +'\n'
          dou = 0
      print(msg)
      await ctx.send(msg)
    
  @commands.command()
  async def reloadlog(self,ctx):
    if await self.bot.is_owner(ctx.message.author):
      global loglist,logindex
      loglist = []
      for logname in os.listdir('./log'):
        if logname.endswith('.txt'):
          loglist.append(logindex)
          loglist.append(logname)
          logindex += 1
      await ctx.send(lang['reloadlog.reloaded'])
      logindex = 0

  @commands.command()
  async def downloadlog(self,ctx,index):
    if await self.bot.is_owner(ctx.message.author):
      for i in loglist:
        if i == int(index):
          a = 'log\\'+loglist[i+1]
          print(a)
          await ctx.send(file=discord.File(a))

def setup(bot):
    bot.add_cog(logup(bot))