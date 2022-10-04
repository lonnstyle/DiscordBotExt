import json
import logging
import os
import time
from datetime import datetime
from operator import itemgetter

import discord
import requests
from discord.ext import commands

from core.classes import Cog_Extension, Hybirdcmd_Aliases
from localization import lang

# from discord_slash import SlashContext, cog_ext
# from discord_slash.utils.manage_commands import create_choice, create_option


lang = lang.langpref()['worldState']

dirname = os.path.dirname(__file__)

logger = logging.getLogger('worldState')
logger.setLevel(-1)
handler = logging.FileHandler(filename=os.path.join(dirname, '../log/runtime.log'), encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(lineno)d: %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
logger.addHandler(handler)


cmds = ['poe', 'earth', 'cambion', 'orb', 'arbitration', 'sortie', 'fissure']
H_A = Hybirdcmd_Aliases(lang, *cmds)


class worldState(Cog_Extension):
    def timeConv(self, expiry):
        return int(time.mktime(datetime.strptime(expiry, "%Y-%m-%dT%H:%M:%S.%fZ").timetuple()))

    @commands.hybrid_command(name=H_A.c_name(), aliases=H_A.c_aliases(), brief=lang['poe.brief'], description=lang['poe.description'])
    async def eidolontime(self, ctx):
        html = requests.get('https://api.warframestat.us/pc/cetusCycle').text
        data = json.loads(html)
        if (data["state"] == "day"):
            desc = lang['poe.embed.description.day'].format(expiry=self.timeConv(data['expiry'])) + f"<t:{self.timeConv(data['expiry'])}:R>"
            embed = discord.Embed(title=lang['poe.embed.title.day'], description=desc, color=0xbfdaf3)
            await ctx.send(embed=embed)
        elif (data["state"] == "night"):
            desc = lang['poe.embed.description.night'].format(expiry=self.timeConv(data['expiry'])) + f"<t:{self.timeConv(data['expiry'])}:R>"
            embed = discord.Embed(title=lang['poe.embed.title.night'], description=desc, color=0xaca9ca)
            await ctx.send(embed=embed)

    # @cog_ext.cog_slash(name='POE', description=lang['poe.description'])
    # async def slash_POE(self, ctx: SlashContext):
    #     await self.eidolontime(ctx)

    @commands.hybrid_command(name=H_A.c_name(), aliases=H_A.c_aliases(), brief=lang['earth.brief'], description=lang['earth.description'])
    async def earthtime(self, ctx):
        html = requests.get('https://api.warframestat.us/pc/tc/earthCycle').text
        data = json.loads(html)
        if (data["state"] == "day"):
            desc = lang['earth.embed.description.day'].format(expiry=self.timeConv(data['expiry'])) + f"<t:{self.timeConv(data['expiry'])}:R>"
            embed = discord.Embed(title=lang['earth.embed.title.day'], description=desc, color=0xbfdaf3)
            await ctx.send(embed=embed)
        elif (data["state"] == "night"):
            desc = lang['earth.embed.description.night'].format(expiry=self.timeConv(data['expiry'])) + f"<t:{self.timeConv(data['expiry'])}:R>"
            embed = discord.Embed(title=lang['earth.embed.title.night'], description=desc, color=0xaca9ca)
            await ctx.send(embed=embed)

    # @cog_ext.cog_slash(name="Earth", description=lang['earth.description'])
    # async def slash_Earth(self, ctx: SlashContext):
    #     await self.earthtime(ctx)

    @commands.hybrid_command(name=H_A.c_name(), aliases=H_A.c_aliases(), brief=lang['cambion.brief'], description=lang['cambion.description'])
    async def cambiontime(self, ctx):
        html = requests.get('https://api.warframestat.us/pc/cetusCycle').text
        data = json.loads(html)
        if (data["state"] == "day"):
            desc = lang["cambion.embed.description.fass"].format(expiry=self.timeConv(data['expiry'])) + f"<t:{self.timeConv(data['expiry'])}:R>"
            embed = discord.Embed(title=lang['cambion.embed.title.fass'], description=desc, color=0xda6d34)
            await ctx.send(embed=embed)
        elif (data["state"] == "night"):
            desc = lang['cambion.embed.description.vome'].format(expiry=self.timeConv(data['expiry'])) + f"<t:{self.timeConv(data['expiry'])}:R>"
            embed = discord.Embed(title=lang['cambion.embed.title.vome'], description=desc, color=0x458691)
            await ctx.send(embed=embed)

    # @cog_ext.cog_slash(name="Cambion", description=lang['cambion.description'])
    # async def slash_Cambion(self, ctx: SlashContext):
    #     await self.cambiontime(ctx)

    @commands.hybrid_command(name=H_A.c_name(), aliases=H_A.c_aliases(), brief=lang['orb.brief'], description=lang['orb.description'])
    async def orbtime(self, ctx):
        html = requests.get('https://api.warframestat.us/pc/vallisCycle', headers={'Accept-Language': 'tc', 'Cache-Control': 'no-cache'}).text
        data = json.loads(html)
        if (data['state'] == 'cold'):
            desc = lang["orb.embed.description.cold"].format(expiry=self.timeConv(data['expiry'])) + f"<t:{self.timeConv(data['expiry'])}:R>"
            embed = discord.Embed(title=lang["orb.embed.title.cold"], description=desc, color=0x6ea7cd)
            await ctx.send(embed=embed)
        elif (data['state'] == 'warm'):
            desc = lang["orb.embed.description.warm"].format(expiry=self.timeConv(data['expiry'])) + f"<t:{self.timeConv(data['expiry'])}:R>"
            embed = discord.Embed(title=lang["orb.embed.title.warm"], description=desc, color=0xd9b4a1)
            await ctx.send(embed=embed)

    # @cog_ext.cog_slash(name="Orb", description=lang['orb.description'])
    # async def slash_Orb(self, ctx: SlashContext):
    #     await self.orbtime(ctx)

    @commands.hybrid_command(name=H_A.c_name(), aliases=H_A.c_aliases(), brief=lang['arbitration.brief'], description=lang['arbitration.description'][:99])
    async def arbitration(self, ctx):
        raw = requests.get("https://api.warframestat.us/pc/tc/arbitration", headers={'Accept-Language': 'zh'})
        text = raw.text
        data = json.loads(text)
        expiry = self.timeConv(data['expiry'])
        embed = discord.Embed(title=lang["arbitration.embed.title"], description=lang['arbitration.embed.description'].format(type=data['type']), color=0x302f36)
        embed.add_field(name=lang['arbitration.embed.field.name'].format(node=data['node']), value=lang["arbitration.embed.field.value"].format(enemy=data['enemy'], expiry=expiry))
        await ctx.send(embed=embed)

    # @cog_ext.cog_slash(name="Arbitration", description=lang['arbitration.description'])
    # async def slash_Arbitration(self, ctx: SlashContext):
    #     await self.arbitration(ctx)

    @commands.hybrid_command(name=H_A.c_name(), aliases=H_A.c_aliases(), brief=lang['sortie.brief'], description=lang['sortie.description'])
    async def sortie(self, ctx):
        count = 1
        raw = requests.get('https://api.warframestat.us/pc/zh/sortie', headers={'Accept-Language': 'tc'})
        text = raw.text
        data = json.loads(text)
        embed = discord.Embed(title=lang["sortie.embed.title"].format(expiry=self.timeConv(data['expiry'])),
                              description=lang['sortie.embed.description'].format(boss=data['boss'], faction=data['faction']), color=0xff9500)
        for missions in data['variants']:
            node = missions['node']
            missionType = missions['missionType']
            modifier = missions['modifier']
            embed.add_field(name=lang['sortie.embed.field.name'].format(count=count, node=node, lower=35+15*count, upper=40+20*count),
                            value=lang['sortie.embed.field.value'].format(missionType=missionType, modifier=modifier), inline=False)
            count += 1
        await ctx.send(embed=embed)

    # @cog_ext.cog_slash(name="Sortie", description=lang['sortie.description'])
    # async def slash_Sortie(self, ctx: SlashContext):
    #     await self.sortie(ctx)

    @commands.hybrid_command(name=H_A.c_name(), aliases=H_A.c_aliases(), brief=lang['fissure.brief'], description=lang['fissure.description'])
    async def fissure(self, ctx, tier="all", is_storm="False"):

        payload = requests.get('https://api.warframestat.us/pc/fissures', headers={'Accept-Language': 'en', 'Cache-Control': 'no-cache'})
        payload = json.loads(payload.text)
        tierList = lang['fissure.tierList']
        planets = lang['fissure.planets']
        mission = lang['fissure.missionType']
        tierOption = lang['fissure.tierOption']
        fissures = sorted(payload, key=itemgetter('tierNum'))
        embed = discord.Embed(title=lang['fissure.embed.title'], description=lang['fissure.embed.description'], color=0x725D33)
        for fissure in fissures:
            if fissure['expired'] != True and (str(fissure['isStorm']) == is_storm or is_storm == 'all') and (fissure['tierNum'] == tierOption.get(tier, tier) or tier == 'all'):
                node = fissure['node']
                for planet, trans in planets.items():
                    if planet in node:
                        try:
                            if fissure['isStorm'] == True:
                                trans += lang['fissure.proxima']
                        except Exception as e:
                            logger.error(f'{e}')
                        node = node.replace(planet, trans)
                missionType = mission[fissure['missionType']]
                missionTier = tierList[str(fissure['tierNum'])]
                expiry = self.timeConv(fissure['expiry'])
                description = lang['fissure.embed.field'].format(tier=missionTier, missionType=missionType, expiry=expiry)
                print(fissure['expired'] != True and fissure['isStorm'] != True)
                embed.add_field(name=node, value=description, inline=False)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(worldState(bot))
    # await bot.tree.sync()
    # logger.debug('Command tree synced')
