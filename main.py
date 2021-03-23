import discord
from discord.ext import commands
import os
import json
import keep_alive
from datetime import datetime,timedelta
import requests
import asyncio
import sys
from language import language as lang


lang = lang()
lang = lang.langpref()['main']
intents = discord.Intents.all()
#載入設定檔
with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)
bot = commands.Bot(command_prefix=commands.when_mentioned_or(jdata['command_prefix']),intents = intents)
start_time = datetime.now()
version = "v2.1.0"

@bot.event
async def on_ready():
  print(lang['startup.version'].format(version=version))
  print(">> OrdisBeta is online <<")
  activity = discord.Activity(type=discord.ActivityType.watching,name = jdata['watching'])
  await bot.change_presence(activity=activity)
  while(1):
    await asyncio.sleep(60)
    requests.get("http://127.0.0.1:8080/")

#----------------------------------------------------------------------------
bot.remove_command('help')
#help指令
@bot.command(name="help" , aliases=lang['help.aliases'] ,description=lang['help.description'], brief=lang['help.brief'])
async def help(ctx, command:str="all", page:int=1):
  fields = 0
  embed = discord.Embed(title=lang['help.embed.title'],color=0xccab2b)
  embed.set_author(name="Patreon", url="https://patreon.com/join/lonnstyle", icon_url="https://i.imgur.com/CCYuxwH.png")
  if command == "all":
    for command in bot.commands:
      if command.brief != None:
        if (page-1)*25<fields<=page*25-1:
          embed.add_field(name=f"{jdata['command_prefix']}{command.name}", value=command.brief, inline=True)
        fields += 1
    embed.set_footer(text=lang['help.embed.footer'].format(command_prefix=jdata['command_prefix'],page=page,total=int((fields-fields%25)/25+1)))
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
    embed.set_footer(text=lang['help.embed.footer'].format(command_prefix=jdata['command_prefix'],page=page,total=int((fields-fields%25)/25+1)))
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
    await ctx.send(lang['help.not_found'].format(user=jdata['user']))


#-----------------------------------------------------------------------------
f = '[%Y-%m-%d %H:%M:%S]'
time_delta = timedelta(hours=+8)
utc_8_date_str = (datetime.utcnow()+time_delta).strftime(f)
#-----------------------------------------------------------------------------

@bot.command(name= 'load', aliases=lang['load.aliases'],brief=lang['load.brief'],description=lang['load.description'])
async def load(ctx, extension):
    if await bot.is_owner(ctx.author):
        bot.load_extension(F'cmds.{extension}')
        await ctx.send(lang['load.loaded'].format(extension=extension))
        print('\n---------------------------------\n' + utc_8_date_str + lang['load.loaded'].format(extension=extension)+'\n---------------------------------\n')
    else:
      await ctx.send(embed=discord.Embed(title=lang['load.error.title'],description=lang['load.error.description'].format(owner=bot.owner_id),color=0xff0000))


@bot.command(name= 'unload', aliases=lang['unload.aliases'],brief=lang['unload.brief'],description=lang['unload.description'])
async def unload(ctx, extension):
    if await bot.is_owner(ctx.author):
        bot.unload_extension(F'cmds.{extension}')
        await ctx.send(lang['unload.unloaded'].format(extension=extension))
        print('\n---------------------------------\n' + utc_8_date_str + lang['unload.unloaded'].format(extension=extension)+'\n---------------------------------\n')
    else:
      await ctx.send(embed=discord.Embed(title=lang['unload.error.title'],description=lang['unload.error.description'].format(owner=bot.owner_id),color=0xff0000))


@bot.command(name= 'reload', aliases=lang['reload.aliases'],brief=lang['reload.brief'],description=lang['reload.description'])
async def reload(ctx, extension):
    if await bot.is_owner(ctx.author):
        bot.reload_extension(F'cmds.{extension}')
        await ctx.send(lang['reload.reloaded'].format(extension=extension))
        print('\n---------------------------------\n' + utc_8_date_str + lang['reload.reloaded'].format(extension=extension)+'\n---------------------------------\n')
    else:
      await ctx.send(embed=discord.Embed(title=lang['reload.error.title'],description=lang['reload.error.description'].format(owner=bot.owner_id),color=0xff0000))
#機器人關閉系統--------------------------------------------   

@bot.command(name= 'disconnect', aliases=lang['disconnect.aliases'],brief=lang['disconnect.brief'],description=lang['disconnect.description'].format(owner=bot.owner_id))
async def turn_off_bot(ctx):
  if await bot.is_owner(ctx.author):
    await ctx.send(utc_8_date_str + '\n'+lang['disconnect.disconnected']) #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    await bot.close()
  else:
    await ctx.send(embed=discord.Embed(title=lang['disconnect.error.title'],description=lang['disconnect.error.description'].format(owner=bot.owner_id),color=0xff0000))
    
#--------------------------------


@bot.command(name='status', aliases=['debug'],brief=lang['status.brief'],description=lang['status.description'].format(owner=bot.owner_id))
async def status(ctx):
  if await bot.is_owner(ctx.message.author):
    embed = discord.Embed(title=lang['status.embed.title'])
    embed.add_field(name=lang['status.embed.field.ping'],value=f"{round(bot.latency*1000)}ms",inline=False)
    perms = ">>> "
    for name,value in ctx.channel.permissions_for(ctx.me):
      if value == True:
        perms += name + '\n'
    embed.add_field(name=lang['status.embed.field.perms'],value=perms,inline=True)
    exts = ">>> "
    for ext in bot.extensions:
      exts += ext.replace("cmds.","")+'\n'
    embed.add_field(name=lang['status.embed.field.exts'],value=exts,inline=True)
    uptime = datetime.now()-start_time
    embed.set_footer(text=lang['status.embed.footer.time'].format(days=uptime.days,hours=int(uptime.seconds/3600),minutes=int(uptime.seconds%3600/60),seconds=uptime.seconds%3600%60)+version)
    await ctx.send(embed=embed)
  else:
    await ctx.send(embed=discord.Embed(title=lang['status.error.title'],description=lang['status.error.description'].format(owner=bot.owner_id)))


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