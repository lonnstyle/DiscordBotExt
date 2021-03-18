import discord
from discord.ext import commands
import os
import json
import keep_alive
from datetime import datetime,timedelta
import requests
import asyncio
import sys

intents = discord.Intents.all()
#載入設定檔
with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

bot = commands.Bot(command_prefix=commands.when_mentioned_or(jdata['command_prefix']),intents = intents)
start_time = datetime.now()

@bot.event
async def on_ready():
    print(">> 目前版本：v2.0.3 <<")
    print(">> OrdisBeta is online <<")
    activity = discord.Activity(type=discord.ActivityType.watching,name = "指揮官帥氣的臉龐")
    await bot.change_presence(activity=activity)
    while(1):
        await asyncio.sleep(60)
        requests.get("http://127.0.0.1:8080/")

#----------------------------------------------------------------------------
bot.remove_command('help')
#help指令
@bot.command(name="help" , aliases=['幫助' , '機器人功能' , 'HELP'] ,description="展示`command`的幫助信息", brief="展示幫助列表")
async def help(ctx, command:str="all", page:int=1):
  fields = 0
  embed = discord.Embed(title="幫助列表",color=0xccab2b)
  embed.set_author(name="Patreon", url="https://patreon.com/join/lonnstyle", icon_url="https://i.imgur.com/CCYuxwH.png")
  if command == "all":
    for command in bot.commands:
      if command.brief != None:
        if (page-1)*25<fields<=page*25-1:
          embed.add_field(name=f"{jdata['command_prefix']}{command.name}", value=command.brief, inline=True)
        fields += 1
    embed.set_footer(text=f"第{page}/{int((fields-fields%25)/25+1)}頁")
    await ctx.send(embed=embed)
  elif command in commands.values():
    for botcommand in bot.commands:
      if command == "common" and botcommand.cog_name == None:
        if (page-1)*25<fields<=page*25-1:
          embed.add_field(name=f"{jdata['command_prefix']}{botcommand.name}", value=botcommand.brief)
        fields += 1
      for ext,tag in commands.items():
        if tag == command and ext == botcommand.cog_name:
          if (page-1)*25<fields<=page*25-1:
            embed.add_field(name=f"{jdata['command_prefix']}{botcommand.name}", value=botcommand.brief)
          fields += 1
    embed.set_footer(text=f"第{page}/{int((fields-fields%25)/25+1)}頁")
    await ctx.send(embed=embed)
  else:
    for botcommand in bot.commands:
      if botcommand.name == command:
        aliases = botcommand.name
        params = ""
        for param in botcommand.clean_params:
          params += f"<{param}>"
        for alias in botcommand.aliases:
          aliases += f"|{alias}"
        embed.add_field(name=f"{jdata['command_prefix']}[{aliases}] {params}",value=botcommand.description)
        await ctx.send(embed=embed)
        return
    await ctx.send("找不到指揮官要問的呢")


#-----------------------------------------------------------------------------
f = '[%Y-%m-%d %H:%M:%S]'
time_delta = timedelta(hours=+8)
utc_8_date_str = (datetime.utcnow()+time_delta).strftime(f)
#-----------------------------------------------------------------------------

@bot.command(name= 'load', aliases=['載入' , '載入模組' , '啟用'],brief="載入擴展庫",description="載入`extension`擴展庫")
async def load(ctx, extension):
    if ctx.author.id == jdata['owner']:
        bot.load_extension(F'cmds.{extension}')
        await ctx.send(f'\n已加載：{extension}')
        print('\n---------------------------------\n' + utc_8_date_str + f'\n已加載 {extension}\n---------------------------------\n')


@bot.command(name= 'unload', aliases=['卸載' , '卸載模組' , '停用'],brief="卸載擴展庫",description="卸載`extension`擴展庫")
async def unload(ctx, extension):
    if ctx.author.id == jdata['owner']:
        bot.unload_extension(F'cmds.{extension}')
        await ctx.send(f'\n已卸載：{extension}')
        print('\n---------------------------------\n' + utc_8_date_str + f'\n已卸載 {extension}\n---------------------------------\n')

@bot.command(name= 'reload', aliases=['重載' , '重載模組' , '重新載入模組', '重新加載', '重啟'],brief="重載擴展庫",description="重新載入`extension`擴展庫")
async def reload(ctx, extension):
    if ctx.author.id == jdata['owner']:
        bot.reload_extension(F'cmds.{extension}')
        await ctx.send(f'\n已重新載入：{extension}')
        print('\n---------------------------------\n' + utc_8_date_str + f'\n已重新載入 {extension}\n---------------------------------\n')
#機器人關閉系統--------------------------------------------   

@bot.command(name= 'disconnect', aliases=['disable' , 'shutdown' , '關閉機器人' , '關機' , '關閉'],brief="關閉機器人",description=f"機器人關機\n僅供<@{jdata['owner']}>使用")
async def turn_off_bot(ctx):
  if ctx.message.author.id == jdata['owner']:
    print(utc_8_date_str + '機器人已關閉')
    await ctx.send(utc_8_date_str + '\n機器人已關閉') #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    await bot.close()
  else:
    owner = jdata['owner']
    await ctx.send(f'權限不足 本指令只提供給Ordis擁有者 \n擁有者為 <@{owner}>')
    
#--------------------------------


@bot.command(name='status', aliases=['debug'],brief="除錯信息",description="回報當前機器人狀態信息進行除錯")
async def status(ctx):
  if await bot.is_owner(ctx.message.author):
    embed = discord.Embed(title="目前狀態:")
    embed.add_field(name="目前延遲",value=f"{round(bot.latency*1000)}ms",inline=False)
    perms = ">>> "
    for name,value in ctx.channel.permissions_for(ctx.me):
      if value == True:
        perms += name + '\n'
    embed.add_field(name="本機權限",value=perms,inline=True)
    exts = ">>> "
    for ext in bot.extensions:
      exts += ext.replace("cmds.","")+'\n'
    embed.add_field(name="已加載擴展",value=exts,inline=True)
    uptime = datetime.now()-start_time
    embed.set_footer(text=f"在線時間:{uptime.days}天{int(uptime.seconds/3600)}:{int(uptime.seconds%3600/60)}:{uptime.seconds%3600%60}")
    await ctx.send(embed=embed)
  else:
    await ctx.send(embed=discord.Embed(title="權限不足",description='本指令只提供給伺服器傭有者 \n本伺服器擁有者為 <@' + str(ctx.guild.owner_id) + '>'))

for filename in os.listdir('./cmds'):
    if filename.endswith('.py'):
        bot.load_extension(f'cmds.{filename[:-3]}')
        
commands = {}
for extension in bot.extensions:
  package = extension
  name = extension[5:]
  tags = getattr(__import__(package, fromlist=[name]), name)      
  try:
    commands[name] = tags.tag
  except:
    pass


    
if __name__ == "__main__":
    keep_alive.keep_alive()
    bot.run(jdata['TOKEN'])
