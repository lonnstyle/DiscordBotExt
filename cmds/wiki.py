import json
from log import logger
import os

import discord
from discord.ext import commands
# from discord_slash import SlashContext, cog_ext
# from discord_slash.utils.manage_commands import create_choice, create_option
from mwclient import Site
from thefuzz import process

from core.classes import Cog_Extension, Hybirdcmd_Aliases
from localization import lang

lang = lang.langpref()['wiki']

dirname = os.path.dirname(__file__)

with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

logger = logger.getLogger('wiki')

zhURL = 'warframe.huijiwiki.com'
tcURL = 'warframe.fandom.com'
enURL = 'warframe.fandom.com'

zh = Site(zhURL, scheme='http')
tc = Site(tcURL, path='/zh-tw/', scheme='http')
en = Site(enURL, path='/', scheme='http')

cmds = ['update_wiki', 'wiki']
hybirdAliases = Hybirdcmd_Aliases(lang, *cmds)


class wiki(Cog_Extension):
    @hybirdAliases.hyb_cmd
    async def update_wiki(self, ctx, wiki):
        name = " ".join(wiki)
        if name == "zh" or "all":
            allpages = zh.allpages()
            with open("dict/zh_pages.txt", "w") as zh_pages:
                for page in allpages:
                    print(page.name, file=zh_pages)
                logger.info('[update_wiki] updated zh wiki links')
        if name == "tc" or "all":
            allpages = tc.allpages()
            with open("dict/tc_pages.txt", "w") as tc_pages:
                for page in allpages:
                    print(page.name, file=tc_pages)
                logger.info('[update_wiki] updated tc wiki links')
        if name == "en" or "all":
            allpages = en.allpages()
            with open("dict/en_pages.txt", "w") as en_pages:
                for page in allpages:
                    print(page.name, file=en_pages)
                logger.info('[update_wiki] updated en wiki links')

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

    @hybirdAliases.hyb_cmd
    async def wiki(self, ctx, page):
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
            logger.info(f'[wiki] found {name} as {title} from zh wiki')
        else:
            title, ratio = process.extractOne(name, tcpage)
            if ratio > 75:
                footer = lang['wiki.footer.tc']
                URL = f"https://{tcURL}/zh-tw/wiki/{title}"
                logger.info(f'[wiki] found {name} as {title} from tc wiki')
            else:
                title, ratio = process.extractOne(name, enpage)
                if ratio > 75:
                    footer = lang['wiki.footer.en']
                    URL = f"https://{enURL}/wiki/{title}"
                    logger.info(f'[wiki] found {name} as {title} from en wiki')
                else:
                    await ctx.send(lang['wiki.error.notFound'].format(self=jdata['self'], user=jdata['user']))
                    logger.warning(f'[wiki] failed to search {name}, most similar: {title}')
                    return
        embed = discord.Embed(title=title, url=URL.replace(" ", "_"))
        embed.set_footer(text=footer)
        await ctx.send(embed=embed)

    # @cog_ext.cog_slash(name="wiki", description=lang['wiki.description'], options=[create_option(name="page", description=lang["wiki.options.page"], option_type=3, required=True)])
    # async def slash_wiki(self, ctx, page):
    #     await ctx.defer()
    #     await self.wiki(ctx, page)


async def setup(bot):
    await bot.add_cog(wiki(bot))
