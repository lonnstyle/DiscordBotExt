import json
from datetime import datetime
from operator import itemgetter

import discord
import requests
from discord.ext import commands

from core.classes import Cog_Extension
from localization import lang

# from discord_slash import SlashContext, cog_ext
# from discord_slash.utils.manage_commands import create_choice, create_option


lang = lang.langpref()['worldState']


class worldState(Cog_Extension):
    tag = "Warframe"

    def timeConv(self, expiry):
        h = int(expiry[11:13]) + 8
        if h >= 24:
            h -= 24
        m = expiry[14:16]
        m = ("0" if len(m) == 1 else "") + m
        s = expiry[17:19]
        s = ("0" if len(s) == 1 else "") + s
        return(str(h)+":"+m)

    @commands.command(name='POE', aliases=lang['poe.aliases'], brief=lang['poe.brief'], description=lang['poe.description'])
    async def eidolontime(self, ctx):
        html = requests.get('https://api.warframestat.us/pc/cetusCycle').text
        data = json.loads(html)
        if (data["state"] == "day"):
            desc = lang['poe.embed.description.day'].format(expiry=self.timeConv(data['expiry'])) + data["timeLeft"]
            embed = discord.Embed(title=lang['poe.embed.title.day'], description=desc, color=0xbfdaf3)
            await ctx.send(embed=embed)
        elif (data["state"] == "night"):
            desc = lang['poe.embed.description.night'].format(expiry=self.timeConv(data['expiry'])) + data["timeLeft"]
            embed = discord.Embed(title=lang['poe.embed.title.night'], description=desc, color=0xaca9ca)
            await ctx.send(embed=embed)

    # @cog_ext.cog_slash(name='POE', description=lang['poe.description'])
    # async def slash_POE(self, ctx: SlashContext):
    #     await self.eidolontime(ctx)

    @commands.command(name='Earth', aliases=lang['earth.aliases'], brief=lang['earth.brief'], description=lang['earth.description'])
    async def earthtime(self, ctx):
        html = requests.get('https://api.warframestat.us/pc/tc/earthCycle').text
        data = json.loads(html)
        if (data["state"] == "day"):
            desc = lang['earth.embed.description.day'].format(expiry=self.timeConv(data['expiry'])) + data["timeLeft"]
            embed = discord.Embed(title=lang['earth.embed.title.day'], description=desc, color=0xbfdaf3)
            await ctx.send(embed=embed)
        elif (data["state"] == "night"):
            desc = lang['earth.embed.description.night'].format(expiry=self.timeConv(data['expiry'])) + data["timeLeft"]
            embed = discord.Embed(title=lang['earth.embed.title.night'], description=desc, color=0xaca9ca)
            await ctx.send(embed=embed)

    # @cog_ext.cog_slash(name="Earth", description=lang['earth.description'])
    # async def slash_Earth(self, ctx: SlashContext):
    #     await self.earthtime(ctx)

    @commands.command(name='Cambion', aliases=lang['cambion.aliases'], brief=lang['cambion.brief'], description=lang['cambion.description'])
    async def cambiontime(self, ctx):
        html = requests.get('https://api.warframestat.us/pc/cetusCycle').text
        data = json.loads(html)
        if (data["state"] == "day"):
            desc = lang["cambion.embed.description.fass"].format(expiry=self.timeConv(data['expiry'])) + data["timeLeft"]
            embed = discord.Embed(title=lang['cambion.embed.title.fass'], description=desc, color=0xda6d34)
            await ctx.send(embed=embed)
        elif (data["state"] == "night"):
            desc = lang['cambion.embed.description.vome'].format(expiry=self.timeConv(data['expiry'])) + data["timeLeft"]
            embed = discord.Embed(title=lang['cambion.embed.title.vome'], description=desc, color=0x458691)
            await ctx.send(embed=embed)

    # @cog_ext.cog_slash(name="Cambion", description=lang['cambion.description'])
    # async def slash_Cambion(self, ctx: SlashContext):
    #     await self.cambiontime(ctx)

    @commands.command(name='Orb', aliases=lang["orb.aliases"], brief=lang['orb.brief'], description=lang['orb.description'])
    async def orbtime(self, ctx):
        html = requests.get('https://api.warframestat.us/pc/vallisCycle', headers={'Accept-Language': 'tc', 'Cache-Control': 'no-cache'}).text
        data = json.loads(html)
        if(data['state'] == 'cold'):
            desc = lang["orb.embed.description.cold"].format(expiry=self.timeConv(data['expiry'])) + data["timeLeft"]
            embed = discord.Embed(title=lang["orb.embed.title.cold"], description=desc, color=0x6ea7cd)
            await ctx.send(embed=embed)
        elif(data['state'] == 'warm'):
            desc = lang["orb.embed.description.warm"].format(expiry=self.timeConv(data['expiry'])) + data["timeLeft"]
            embed = discord.Embed(title=lang["orb.embed.title.warm"], description=desc, color=0xd9b4a1)
            await ctx.send(embed=embed)

    # @cog_ext.cog_slash(name="Orb", description=lang['orb.description'])
    # async def slash_Orb(self, ctx: SlashContext):
    #     await self.orbtime(ctx)

    @commands.command(name="Arbitration", aliases=lang["arbitration.aliases"], brief=lang['arbitration.brief'], description=lang['arbitration.description'])
    async def arbitration(self, ctx):
        raw = requests.get("https://api.warframestat.us/pc/tc/arbitration", headers={'Accept-Language': 'zh'})
        text = raw.text
        data = json.loads(text)
        expiry = data['expiry']
        timeLeft = datetime.strptime(expiry, '%Y-%m-%dT%X.000Z')
        now = datetime.now()
        timeLeft = timeLeft-now
        minutes = int((timeLeft.seconds - timeLeft.seconds % 60)/60)
        seconds = timeLeft.seconds % 60
        embed = discord.Embed(title=lang["arbitration.embed.title"], description=lang['arbitration.embed.description'].format(type=data['type']), color=0x302f36)
        embed.add_field(name=lang['arbitration.embed.field.name'].format(node=data['node']), value=lang["arbitration.embed.field.value"].format(enemy=data['enemy'], minutes=minutes, seconds=seconds))
        await ctx.send(embed=embed)

    # @cog_ext.cog_slash(name="Arbitration", description=lang['arbitration.description'])
    # async def slash_Arbitration(self, ctx: SlashContext):
    #     await self.arbitration(ctx)

    @commands.command(name='Sortie', aliases=lang['sortie.aliases'], brief=lang['sortie.brief'], description=lang['sortie.description'])
    async def sortie(self, ctx):
        count = 1
        raw = requests.get('https://api.warframestat.us/pc/zh/sortie', headers={'Accept-Language': 'tc'})
        text = raw.text
        data = json.loads(text)
        embed = discord.Embed(title=lang["sortie.embed.title"].format(eta=data['eta']), description=lang['sortie.embed.description'].format(boss=data['boss'], faction=data['faction']), color=0xff9500)
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

    @commands.command(name="Fissure", aliases=lang['fissure.aliases'], brief=lang['fissure.brief'], description=lang['fissure.description'])
    async def fissure(self, ctx, tier="all", isStorm="False"):
        payload = requests.get('https://api.warframestat.us/pc/fissures', headers={'Accept-Language': 'en', 'Cache-Control': 'no-cache'})
        payload = json.loads(payload.text)
        tierList = lang['fissure.tierList']
        planets = lang['fissure.planets']
        mission = lang['fissure.missionType']
        tierOption = lang['fissure.tierOption']
        fissures = sorted(payload, key=itemgetter('tierNum'))
        embed = discord.Embed(title=lang['fissure.embed.title'], description=lang['fissure.embed.description'], color=0x725D33)
        for fissure in fissures:
            if fissure['expired'] != True and (str(fissure['isStorm']) == isStorm or isStorm == 'all') and (fissure['tierNum'] == tierOption.get(tier, tier) or tier == 'all'):
                node = fissure['node']
                for planet, trans in planets.items():
                    if planet in node:
                        if fissure['isStorm'] == True:
                            trans += lang['fissure.proxima']
                        node = node.replace(planet, trans)
                missionType = mission[fissure['missionType']]
                missionTier = tierList[str(fissure['tierNum'])]
                eta = fissure['eta']
                description = lang['fissure.embed.field'].format(tier=missionTier, missionType=missionType, eta=eta)
                print(fissure['expired'] != True and fissure['isStorm'] != True)
                embed.add_field(name=node, value=description, inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(worldState(bot))
