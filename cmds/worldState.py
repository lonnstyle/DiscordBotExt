import json
import os
import time
from datetime import datetime, timedelta
from operator import itemgetter

import discord
import requests
from discord.ext import commands

from cmds.parsers.world_state import WorldStateParser
from core.classes import Cog_Extension, Hybirdcmd_Aliases
from localization import lang
from log import logger

# from discord_slash import SlashContext, cog_ext
# from discord_slash.utils.manage_commands import create_choice, create_option

parser = WorldStateParser()

lang = lang.langpref()['worldState']


logger = logger.getLogger('worldState')


cmds = ['poe', 'earth', 'cambion', 'orb', 'arbitration', 'sortie', 'archon', 'fissure']
hybirdAliases = Hybirdcmd_Aliases(lang, *cmds)


class worldState(Cog_Extension):
    def timeConv(self, expiry):
        if type(expiry) == datetime:
            return int(time.mktime(expiry.timetuple()))
        expiry = datetime.strptime(expiry, "%Y-%m-%dT%H:%M:%S.%fZ")
        return int(time.mktime(expiry.timetuple()))

    # @commands.hybrid_command(name=hybirdAliases.c_name(), aliases=hybirdAliases.c_aliases(), brief=lang['poe.brief'], description=lang['poe.description'])
    @hybirdAliases.hyb_cmd
    async def eidolontime(self, ctx):
        state, expiry = parser.get_poe_state()
        if (state == "day"):
            desc = lang['poe.embed.description.day'].format(expiry=self.timeConv(expiry)) + f"<t:{self.timeConv(expiry)}:R>"
            embed = discord.Embed(title=lang['poe.embed.title.day'], description=desc, color=0xbfdaf3)
            await ctx.send(embed=embed)
        elif (state == "night"):
            desc = lang['poe.embed.description.night'].format(expiry=self.timeConv(expiry)) + f"<t:{self.timeConv(expiry)}:R>"
            embed = discord.Embed(title=lang['poe.embed.title.night'], description=desc, color=0xaca9ca)
            await ctx.send(embed=embed)

    # @cog_ext.cog_slash(name='POE', description=lang['poe.description'])
    # async def slash_POE(self, ctx: SlashContext):
    #     await self.eidolontime(ctx)

    # @commands.hybrid_command(name=hybirdAliases.c_name(), aliases=hybirdAliases.c_aliases(), brief=lang['earth.brief'], description=lang['earth.description'])
    @hybirdAliases.hyb_cmd
    async def earthtime(self, ctx):
        state, expiry = parser.get_earth_state()
        if (state == "day"):
            desc = lang['earth.embed.description.day'].format(expiry=self.timeConv(expiry)) + f"<t:{self.timeConv(expiry)}:R>"
            embed = discord.Embed(title=lang['earth.embed.title.day'], description=desc, color=0xbfdaf3)
            await ctx.send(embed=embed)
        elif (state == "night"):
            desc = lang['earth.embed.description.night'].format(expiry=self.timeConv(expiry)) + f"<t:{self.timeConv(expiry)}:R>"
            embed = discord.Embed(title=lang['earth.embed.title.night'], description=desc, color=0xaca9ca)
            await ctx.send(embed=embed)

    # @cog_ext.cog_slash(name="Earth", description=lang['earth.description'])
    # async def slash_Earth(self, ctx: SlashContext):
    #     await self.earthtime(ctx)

    # @commands.hybrid_command(name=hybirdAliases.c_name(), aliases=hybirdAliases.c_aliases(), brief=lang['cambion.brief'], description=lang['cambion.description'])
    @hybirdAliases.hyb_cmd
    async def cambiontime(self, ctx):
        state, expiry = parser.get_cambion_state()
        if (state == "day"):
            desc = lang["cambion.embed.description.fass"].format(expiry=self.timeConv(expiry)) + f"<t:{self.timeConv(expiry)}:R>"
            embed = discord.Embed(title=lang['cambion.embed.title.fass'], description=desc, color=0xda6d34)
            await ctx.send(embed=embed)
        elif (state == "night"):
            desc = lang['cambion.embed.description.vome'].format(expiry=self.timeConv(expiry)) + f"<t:{self.timeConv(expiry)}:R>"
            embed = discord.Embed(title=lang['cambion.embed.title.vome'], description=desc, color=0x458691)
            await ctx.send(embed=embed)

    # @cog_ext.cog_slash(name="Cambion", description=lang['cambion.description'])
    # async def slash_Cambion(self, ctx: SlashContext):
    #     await self.cambiontime(ctx)

    # @commands.hybrid_command(name=hybirdAliases.c_name(), aliases=hybirdAliases.c_aliases(), brief=lang['orb.brief'], description=lang['orb.description'])
    @hybirdAliases.hyb_cmd
    async def orbtime(self, ctx):
        state, expiry = parser.get_orb_state()
        if (state == 'cold'):
            desc = lang["orb.embed.description.cold"].format(expiry=self.timeConv(expiry)) + f"<t:{self.timeConv(expiry)}:R>"
            embed = discord.Embed(title=lang["orb.embed.title.cold"], description=desc, color=0x6ea7cd)
            await ctx.send(embed=embed)
        elif (state == 'warm'):
            desc = lang["orb.embed.description.warm"].format(expiry=self.timeConv(expiry)) + f"<t:{self.timeConv(expiry)}:R>"
            embed = discord.Embed(title=lang["orb.embed.title.warm"], description=desc, color=0xd9b4a1)
            await ctx.send(embed=embed)

    # @cog_ext.cog_slash(name="Orb", description=lang['orb.description'])
    # async def slash_Orb(self, ctx: SlashContext):
    #     await self.orbtime(ctx)

    # @commands.hybrid_command(name=hybirdAliases.c_name(), aliases=hybirdAliases.c_aliases(), brief=lang['arbitration.brief'], description=lang['arbitration.description'][:99])
    @hybirdAliases.hyb_cmd
    async def arbitration(self, ctx):
        data = parser.get_arbitration()
        expiry = self.timeConv(data['expiry'])
        embed = discord.Embed(title=lang["arbitration.embed.title"], description=lang['arbitration.embed.description'].format(type=data['type']), color=0x302f36)
        embed.add_field(name=lang['arbitration.embed.field.name'].format(node=data['node']), value=lang["arbitration.embed.field.value"].format(enemy=data['enemy'], expiry=expiry))
        await ctx.send(embed=embed)

    # @cog_ext.cog_slash(name="Arbitration", description=lang['arbitration.description'])
    # async def slash_Arbitration(self, ctx: SlashContext):
    #     await self.arbitration(ctx)

    # @commands.hybrid_command(name=hybirdAliases.c_name(), aliases=hybirdAliases.c_aliases(), brief=lang['sortie.brief'], description=lang['sortie.description'])
    @hybirdAliases.hyb_cmd
    async def sortie(self, ctx):
        count = 1
        start, end, boss, missions = parser.get_sortie()
        for mission in missions:
            node = mission['node']
            missionType = mission['missionType']
            modifier = mission['modifierType']
            if count == 1:
                embed = discord.Embed(title=lang["sortie.embed.title"].format(expiry=int(end)),
                                      description=lang['sortie.embed.description'].format(boss=boss, faction=node), color=0xff9500)
            embed.add_field(name=lang['sortie.embed.field.name'].format(count=count, node=node, lower=35+15*count, upper=40+20*count),
                            value=lang['sortie.embed.field.value'].format(missionType=missionType, modifier=modifier), inline=False)
            count += 1
        await ctx.send(embed=embed)

    @hybirdAliases.hyb_cmd
    async def archon(self, ctx):
        count = 1
        start, end, boss, missions = parser.get_archon()
        for mission in missions:
            node = mission['node']
            missionType = mission['missionType']
            if count == 1:
                embed = discord.Embed(title=lang["archon.embed.title"].format(expiry=int(end)),
                                      description=lang['archon.embed.description'].format(boss=boss, faction=node), color=0xff9500)
            embed.add_field(name=lang['archon.embed.field.name'].format(count=count, node=node, lower=35+15*count, upper=40+20*count),
                            value=lang['archon.embed.field.value'].format(missionType=missionType), inline=False)
            count += 1
        await ctx.send(embed=embed)

    # @cog_ext.cog_slash(name="Sortie", description=lang['sortie.description'])
    # async def slash_Sortie(self, ctx: SlashContext):
    #     await self.sortie(ctx)

    @hybirdAliases.hyb_cmd
    async def fissure(self, ctx, Storm="True"):
        fissures = parser.get_fissure()
        voidstroms = parser.get_voidstorms()
        embed = discord.Embed(title=lang['fissure.embed.title'], description=lang['fissure.embed.description'], color=0x725D33)
        for fissure in fissures:
            node = fissure['Node'] + '(' + fissure['System'] + ')'
            missionType = fissure['MissionType']
            missionTier = fissure['Tier']
            expiry = int(fissure['Expiry'])
            description = lang['fissure.embed.field'].format(tier=missionTier, missionType=missionType, expiry=expiry)
            embed.add_field(name=node, value=description, inline=False)
        if Storm:
            for fissure in voidstroms:
                node = fissure['Node']
                missionType = fissure['MissionType'] + '(' + lang['fissure.proxima'] + ')'
                missionTier = fissure['Tier']
                expiry = int(fissure['Expiry'])
                description = lang['fissure.embed.field'].format(tier=missionTier, missionType=missionType, expiry=expiry)
                embed.add_field(name=node, value=description, inline=False)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(worldState(bot))
