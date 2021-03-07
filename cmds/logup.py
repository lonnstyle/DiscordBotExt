import discord
from discord.ext import commands
from core.classes import Cog_Extension
import os
import json
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
    if str(ctx.author.id) == jdata['owner']:
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
    if str(ctx.author.id) == jdata['owner']:
      global loglist,logindex
      loglist = []
      for logname in os.listdir('./log'):
        if logname.endswith('.txt'):
          loglist.append(logindex)
          loglist.append(logname)
          logindex += 1
      await ctx.send('已重新加載')
      logindex = 0

  @commands.command()
  async def downloadlog(self,ctx,index):
    if str(ctx.author.id) == jdata['owner']:
      for i in loglist:
        if i == int(index):
          a = 'log\\'+loglist[i+1]
          print(a)
          await ctx.send(file=discord.File(a))

def setup(bot):
    bot.add_cog(logup(bot))