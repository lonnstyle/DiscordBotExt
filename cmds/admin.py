import json
import logging
import os

import discord
from core.classes import Cog_Extension
from discord.ext import commands
from localization import lang

lang = lang.langpref()['admin']

dirname = os.path.dirname(__file__)

with open(os.path.join(dirname, '../setting.json'), 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

logger = logging.getLogger('admin')
logger.setLevel(-1)
handler = logging.FileHandler(filename=os.path.join(dirname, '../log/runtime.log'), encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


class admin(Cog_Extension):
    tag = "admin"
    # 清除訊息

    @commands.command(name='clear', aliases=lang['clear.aliases'], brief=lang['clear.brief'], description=lang['clear.description'])
    async def clear(self, ctx, num: int):
        if ctx.message.author.id == ctx.guild.owner_id:
            await ctx.channel.purge(limit=num+1)
            logger.info(f"[clear]{str(ctx.message.author)} attempted to delete {num} messages in {ctx.channel.name}")
        else:
            embed = discord.embed(title=lang['clear.error.title'], description=lang['clear.error.description'].format(owner=ctx.guild.owner_id))
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(admin(bot))
