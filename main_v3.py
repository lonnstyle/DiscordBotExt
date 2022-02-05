import asyncio
import json
import logging
import os
from datetime import datetime, timedelta

import discord
import interactions
import requests
from discord import activity
from discord.ext import commands
from interactions.api.models.gw import Presence
from interactions.api.models.message import Embed, EmbedAuthor, EmbedField
from interactions.api.models.presence import PresenceActivity

import keep_alive
from localization import lang

# from platformdirs import importlib


# clear log records
with open("log/runtime.log", "w") as log:
    pass
# setup logger
logger = logging.getLogger('main')
logger.setLevel(-1)
# display all logging messages
handler = logging.FileHandler(filename='log/runtime.log', encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
logger.info('[init] Bot startup')

logger.debug("[language] requesting language")
# lang = importlib.import_module("language").lang
# import with importlib, to prevent sort imports
lang.init()
lang = lang.langpref()['main']
intents = discord.Intents.all()

# load settings and init
with open('setting.json', 'r') as _jfile:
    jdata = json.load(_jfile)
bot = commands.Bot(command_prefix=commands.when_mentioned_or(jdata['command_prefix']), intents=intents)
start_time = datetime.now()
version = "v3.0.0alpha"
logger.info(f"[init] Bot is now starting...")


@bot.event
async def on_ready():
    logger.info(f'[init] current version: {version}')
    logger.info('[init] Bot is now started')
    activity = discord.Activity(type=discord.ActivityType.watching, name=jdata['watching'])
    logger.info("[init] Bot activity set.")
    await bot.change_presence(activity=activity)
    while(1):
        await asyncio.sleep(60)
        requests.get("http://127.0.0.1:8080/")

bot.remove_command('help')
logger.debug('[init] removed default help')


@bot.command(name="help", aliases=lang['help.aliases'], description=lang['help.description'], brief=lang['help.brief'])
async def help(ctx, command: str = "all", page: int = 1):
    fields = 0
    embed = discord.Embed(title=lang['help.embed.title'], color=0xccab2b)
    embed.set_author(name="Patreon", url="https://patreon.com/join/lonnstyle", icon_url="https://i.imgur.com/CCYuxwH.png")
    if command == "all":
        # send all commands help
        for command in bot.commands:
            if command.brief != None:
                if (page-1)*25 <= fields <= page*25-1:
                    embed.add_field(name=f"{jdata['command_prefix']}{command.name}", value=command.brief, inline=True)
                fields += 1
        embed.set_footer(text=lang['help.embed.footer'].format(command_prefix=jdata['command_prefix'], page=page, total=int((fields-fields % 25)/25+1)))
        await ctx.send(embed=embed)
    elif command in commands.values():
        # send specific command help
        for botcommand in bot.commands:
            if command == "common" and botcommand.cog_name == None:
                # commands in common cog (None)
                if (page-1)*25 < fields <= page*25-1:
                    # every page can only contain 25 fields
                    embed.add_field(name=f"{jdata['command_prefix']}{botcommand.name}", value=botcommand.brief)
                fields += 1
            for ext, tag in commands.items():
                if botcommand.name == 'clear':
                    logger.debug(f"tag = {tag},ext = {ext},cog_name = {botcommand.cog_name}")
                if tag == command and ext == botcommand.cog_name:
                    if (page-1)*25 < fields <= page*25-1:
                        embed.add_field(name=f"{jdata['command_prefix']}{botcommand.name}", value=botcommand.brief)
                    fields += 1
        embed.set_footer(text=lang['help.embed.footer'].format(command_prefix=jdata['command_prefix'], page=page, total=int((fields-fields % 25)/25+1)))
        await ctx.send(embed=embed)
    else:
        for botcommand in bot.commands:
            if botcommand.name == command:
                aliases = botcommand.name
                params = ""
                for param in botcommand.clean_params:
                    params += f" <{param}>"
                for alias in botcommand.aliases:
                    aliases += f"|{alias}"
                embed.add_field(name=f"{jdata['command_prefix']}[{aliases}]{params}", value=botcommand.description)
                embed.add_field(name="cog", value=botcommand.cog_name)
                await ctx.send(embed=embed)
                return
        await ctx.send(lang['help.not_found'].format(user=jdata['user']))


@bot.command(name='load', aliases=lang['load.aliases'], brief=lang['load.brief'], description=lang['load.description'])
async def load(ctx, extension):
    if await bot.is_owner(ctx.author):
        bot.load_extension(F'cmds.{extension}')
        await ctx.send(lang['load.loaded'].format(extension=extension))
        logger.debug(f'[load] loaded extension: {extension}')
    else:
        await ctx.send(embed=discord.Embed(title=lang['load.error.title'], description=lang['load.error.description'].format(owner=bot.owner_id), color=0xff0000))


@bot.command(name='unload', aliases=lang['unload.aliases'], brief=lang['unload.brief'], description=lang['unload.description'])
async def unload(ctx, extension):
    if await bot.is_owner(ctx.author):
        bot.unload_extension(F'cmds.{extension}')
        await ctx.send(lang['unload.unloaded'].format(extension=extension))
        logger.debug(f'[unload] unloaded extension: {extension}')
    else:
        await ctx.send(embed=discord.Embed(title=lang['unload.error.title'], description=lang['unload.error.description'].format(owner=bot.owner_id), color=0xff0000))


@bot.command(name='reload', aliases=lang['reload.aliases'], brief=lang['reload.brief'], description=lang['reload.description'])
async def reload(ctx, extension):
    if await bot.is_owner(ctx.author):
        bot.reload_extension(F'cmds.{extension}')
        await ctx.send(lang['reload.reloaded'].format(extension=extension))
        logger.debug(f'[reload] reloaded extension: {extension}')
    else:
        await ctx.send(embed=discord.Embed(title=lang['reload.error.title'], description=lang['reload.error.description'].format(owner=bot.owner_id), color=0xff0000))
# 機器人關閉系統--------------------------------------------


@bot.command(name='disconnect', aliases=lang['disconnect.aliases'], brief=lang['disconnect.brief'], description=lang['disconnect.description'].format(owner=bot.owner_id))
async def turn_off_bot(ctx):
    if await bot.is_owner(ctx.author):
        await ctx.send(lang['disconnect.disconnected'])
        logger.info('[disconnect] bot is now closing')
        await bot.close()
    else:
        await ctx.send(embed=discord.Embed(title=lang['disconnect.error.title'], description=lang['disconnect.error.description'].format(owner=bot.owner_id), color=0xff0000))


@bot.command(name='status', aliases=lang['status.aliases'], brief=lang['status.brief'], description=lang['status.description'].format(owner=bot.owner_id))
async def status(ctx):
    if await bot.is_owner(ctx.message.author):
        embed = discord.Embed(title=lang['status.embed.title'])
        embed.add_field(name=lang['status.embed.field.ping'], value=f"{round(bot.latency*1000)}ms", inline=False)
        perms = ">>> "
        for name, value in ctx.channel.permissions_for(ctx.me):
            if value == True:
                perms += name + '\n'
        embed.add_field(name=lang['status.embed.field.perms'], value=perms, inline=True)
        exts = ">>> "
        for ext in bot.extensions:
            exts += ext.replace("cmds.", "")+'\n'
        embed.add_field(name=lang['status.embed.field.exts'], value=exts, inline=True)
        embed.add_field(name=lang['status.embed.uptime'], value=f">>> <t:{int(start_time.timestamp())}:R>\n{version}", inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send(embed=discord.Embed(title=lang['status.error.title'], description=lang['status.error.description'].format(owner=bot.owner_id)))


@bot.command(name='sponsor', aliases=lang['sponsor.aliases'], description=lang['sponsor.description'])
async def sponsor(ctx):
    embed = discord.Embed(title=lang['sponsor.embed.title'], description=lang['sponsor.embed.description'], color=0xff424d, url="https://patreon.com/join/lonnstyle")
    embed.set_thumbnail(url="https://i.imgur.com/CCYuxwH.png")
    await ctx.send(embed=embed)


@bot.command(name='documentation', aliases=lang['documentation.aliases'], description=lang['documentation.description'])
async def documentation(ctx):
    embed = discord.Embed(title=lang['documentation.embed.title'], description=lang['documentation.embed.description'], color=0x2980b9, url=lang['documentation.embed.url'])
    await ctx.send(embed=embed)

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


@bot.listen()
async def on_command_error(ctx, error):
    owner = await bot.application_info()
    owner = owner.owner
    embed = discord.Embed(title="Error", description=str(error))
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    embed.add_field(name="Context", value=ctx.message.content)
    if type(ctx.channel) == discord.channel.TextChannel:
        embed.add_field(name="Channel", value=ctx.guild.name+'/'+ctx.channel.name)
    if ctx.command in bot.commands:
        await owner.send(embed=embed)
        logger.info(f"[command_error]message: {ctx.message.content}")
        logger.info(f"[command_error]error: {error}")


logger.info('[init] loading extensions')
for filename in os.listdir('./cmds'):
    if filename.endswith('.py'):
        try:
            bot.load_extension(f'cmds.{filename[:-3]}')
            logger.debug(f'[init] loaded extension: {filename[:-3]}')
        except Exception as exc:
            logger.error(f'[init] {exc}')

commands = {}
for extension in bot.extensions:
    package = extension
    name = extension[5:]
    tags = getattr(__import__(package, fromlist=[name]), name)
    try:
        commands[name] = tags.tag
    except Exception as exc:
        logger.warning(exc)


if __name__ == "__main__":
    keep_alive.keep_alive()
    try:
        bot.run(jdata['TOKEN'])
    except Exception as exc:
        logger.critical(exc)
