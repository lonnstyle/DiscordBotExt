import json
from log import logger
import os

import discord
from discord.ext import commands

from core.classes import Cog_Extension, Hybirdcmd_Aliases
from localization import lang

lang = lang.langpref()['admin']

dirname = os.path.dirname(__file__)

with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

logger = logger.getLogger('admin')

cmds = ['clear']
hybirdAliases = Hybirdcmd_Aliases(lang, *cmds)


class admin(Cog_Extension):

    @hybirdAliases.hyb_cmd
    async def clear(self, ctx, num: int):
        # if ctx.message.author.id == ctx.guild.owner_id:
        if ctx.message.channel.permissions_for(ctx.message.author).manage_messages:
            # if author have permission in corresponding channel
            await ctx.channel.purge(limit=num+1)
            logger.info(f"[clear]{str(ctx.message.author)} attempted to delete {num} messages in {ctx.channel.name}")
        else:
            embed = discord.embed(title=lang['clear.error.title'], description=lang['clear.error.description'].format(owner=ctx.guild.owner_id))
            await ctx.send(embed=embed)
            logger.info(f"[clear] {str(ctx.message.author)} do failed to delete {num} messages in {ctx.channel.name} cuz lack of permission")


async def setup(bot):
    await bot.add_cog(admin(bot))
