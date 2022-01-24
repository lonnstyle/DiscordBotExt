import json

import discord
from discord.ext import commands
# from discord_slash import SlashContext, cog_ext
# from discord_slash.utils.manage_commands import create_choice, create_option
from mwclient import Site
from thefuzz import process

from core.classes import Cog_Extension
from localization import lang

lang = lang.langpref()['wiki']

with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

zhURL = 'warframe.huijiwiki.com'
tcURL = 'warframe.fandom.com'
enURL = 'warframe.fandom.com'

zh = Site(zhURL, scheme='http')
tc = Site(tcURL, path='/zh-tw/', scheme='http')
en = Site(enURL, path='/', scheme='http')


class wiki(Cog_Extension):
    tag = "Warframe"

    @commands.command(name='update_wiki', brief=lang['update_wiki.brief'], description=lang['update_wiki.description'])
    async def update_wiki(self, ctx, *wiki):
        name = " ".join(wiki)
        if name == "zh" or "all":
            allpages = zh.allpages()
            with open("dict/zh_pages.txt", "w") as zh_pages:
                for page in allpages:
                    print(page.name, file=zh_pages)
        if name == "tc" or "all":
            allpages = tc.allpages()
            with open("dict/tc_pages.txt", "w") as tc_pages:
                for page in allpages:
                    print(page.name, file=tc_pages)
        if name == "en" or "all":
            allpages = en.allpages()
            with open("dict/en_pages.txt", "w") as en_pages:
                for page in allpages:
                    print(page.name, file=en_pages)

    # @cog_ext.cog_slash(name="update_wiki", description=lang['update_wiki.description'],
    #                    options=[
    #     create_option(
    #         name="wiki", description=lang["update_wiki.options.wiki"],
    #         option_type=3, required=True,
    #         choices=[create_choice(name=lang["update_wiki.options.zh"],
    #                                value="zh"),
    #                  create_choice(name=lang["update_wiki.options.tc"],
    #                                value="tc"),
    #                  create_choice(name=lang["update_wiki.options.en"],
    #                                value="en"),
    #                  create_choice(name=lang["update_wiki.options.all"],
    #                                value="all")])])
    # async def slash_update_wiki(self, ctx: SlashContext, wiki):
    #     await ctx.defer()
    #     await self.update_wiki(ctx, wiki)

    @commands.command(name='wiki', aliases=lang['wiki.aliases'], brief=lang['wiki.brief'], description=lang['wiki.description'])
    async def wiki(self, ctx, *page):
        name = " ".join(page)
        with open("dict/zh_pages.txt", "r") as zh_pages:
            zhpage = list(zh_pages.readlines())
        with open("dict/tc_pages.txt", "r") as tc_pages:
            tcpage = list(tc_pages.readlines())
        with open("dict/en_pages.txt", "r") as en_pages:
            enpage = list(en_pages.readlines())
        title, ratio = process.extractOne(name, zhpage)
        if ratio > 75:
            footer = lang['wiki.footer.huiji']
            URL = f"https://{zhURL}/wiki/{title}"
        else:
            title, ratio = process.extractOne(name, tcpage)
            if ratio > 75:
                footer = lang['wiki.footer.tc']
                URL = f"https://{tcURL}/zh-tw/wiki/{title}"
            else:
                title, ratio = process.extractOne(name, enpage)
                if ratio > 75:
                    footer = lang['wiki.footer.en']
                    URL = f"https://{enURL}/wiki/{title}"
                else:
                    await ctx.send(lang['wiki.error.notFound'].format(self=jdata['self'], user=jdata['user']))
                    return
        embed = discord.Embed(title=title, url=URL.replace(" ", "_"))
        embed.set_footer(text=footer)
        await ctx.send(embed=embed)

    # @cog_ext.cog_slash(name="wiki", description=lang['wiki.description'], options=[create_option(name="page", description=lang["wiki.options.page"], option_type=3, required=True)])
    # async def slash_wiki(self, ctx, page):
    #     await ctx.defer()
    #     await self.wiki(ctx, page)


def setup(bot):
    bot.add_cog(wiki(bot))
