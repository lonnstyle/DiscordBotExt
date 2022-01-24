import json
import os

import discord
from discord.ext import commands

from core.classes import Cog_Extension
from localization import lang

lang = lang.langpref()['admin']

with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)


class admin(Cog_Extension):
    tag = "admin"
    # 清除訊息

    @commands.command(name='clear', aliases=lang['clear.aliases'], brief=lang['clear.brief'], description=lang['clear.description'])
    async def clear(self, ctx, num: int):
        if ctx.message.author.id == ctx.guild.owner_id:
            await ctx.channel.purge(limit=num+1)
            print(str(ctx.message.author)+' ---ID '+str(ctx.message.author.id)+lang['clear.cleared'].format(channel=str(ctx.channel.name), num=str(int(num))))
        else:
            embed = discord.embed(title=lang['clear.error.title'], description=lang['clear.error.description'].format(owner=self.bot.owner_id))
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(admin(bot))
