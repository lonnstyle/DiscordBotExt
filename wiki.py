from discord.ext import commands
from core.classes import Cog_Extension
import discord
from mwclient import Site

zh = Site('warframe.huijiwiki.com', scheme='https')
tc = Site('warframe.fandom.com', path='/zh-tw/', scheme='https')
en = Site('warframe.fandom.com', path='/', scheme='https')

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
      else:
        page = page.resolve_redirect()
        name = page.name
        url = "https://warframe.fandom.com/zh-tw/wiki/"+name
    else:
      page = page.resolve_redirect()
      name = page.name
      url = "https://warframe.huijiwiki.com/wiki/"+name
    text = page.text()
    url = url.replace(" ","_")
    embed = discord.Embed(title=name,url=url,description=text[:500]) 
    await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(wiki(bot))
