from discord.ext import commands
from core.classes import Cog_Extension
import discord
from mwclient import Site

zh = Site('warframe.huijiwiki.com', scheme='https')
tc = Site('warframe.fandom.com', path='/zh-tw/', scheme='https')
en = Site('warframe.fandom.com', path='/', scheme='https')

subpage = {"Main":"概述","Prime":"Prime","Abilities":"技能","Equip":"可替換裝備","Patch_History":"更新歷史","Media":"影音資料"}

class wiki(Cog_Extension):
  @commands.command(name='wiki',aliases=['維基'])
  async def wiki(self,ctx,*args):
    name = " ".join(args)
    page = zh.pages[name]
    if page.exists == False:
      page = tc.pages[name]
      if page.exists == False:
        page = en.pages[name]
        if page.exists == False:
          await ctx.send("頁面不存在，Ordis在等待指揮官為Wiki作出貢獻呢")
          return
        else: 
          page = page.resolve_redirect()
          name = page.name
          url = "https://warframe.fandom.com/wiki/"+name
          footer="英文Fandom"
          host = en
      else:
        page = page.resolve_redirect()
        name = page.name
        url = "https://warframe.fandom.com/zh-tw/wiki/"+name
        footer="繁中Fandom"
        host = tc
    else:
      page = page.resolve_redirect()
      name = page.name
      url = "https://warframe.huijiwiki.com/wiki/"+name
      footer="灰機Wiki"
      host = zh
    url = url.replace(" ","_")
    found = 0
    desc = "以下為嵌入頁面鏈接:\n"
    for items in subpage:
      sub = host.pages[f"{name}/{items}"]
      if sub.exists == True:
        linkURL = url.replace(name,"")+items
        desc += f"[{subpage[items]}]({linkURL})\n"
    if desc == "以下為嵌入頁面鏈接:\n":
      desc = ""
    desc += "以下為相關頁面鏈接:\n"
    for link in page.links():
      if name in link.name:
        linkURL = url.replace(name,"")+link.name.replace(" ","_")
        if found <=5:
          desc += f"[{link.name}]({linkURL})\n"
        found += 1
    if found == 0:
      desc = ""
    embed = discord.Embed(title=name,url=url,description=desc)
    embed.set_footer(text=footer)
    await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(wiki(bot))
