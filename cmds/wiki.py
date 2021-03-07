from discord.ext import commands
from core.classes import Cog_Extension
import discord
from mwclient import Site
from fuzzywuzzy import process

zhURL = 'warframe.huijiwiki.com'
tcURL = 'warframe.fandom.com'
enURL = 'warframe.fandom.com'

zh = Site(zhURL,scheme='http')
tc = Site(tcURL, path='/zh-tw/', scheme='http')
en = Site(enURL, path='/', scheme='http')


class wiki(Cog_Extension):
  tag = "Warframe"
  @commands.command(name='update_wiki',brief="更新維基頁面列表",description="更新`wiki`語言維基的本地緩存頁面列表\n輸入`all`以更新所有維基")
  async def update_wiki(self,ctx,*wiki):
    name = " ".join(wiki)
    if name == "zh"or"all":
      allpages= zh.allpages()
      with open("dict/zh_pages.txt","w") as zh_pages:
        for page in allpages:
          print(page.name,file = zh_pages)
    elif name == "tc"or"all":
      allpages= tc.allpages()
      with open("dict/tc_pages.txt","w") as tc_pages:
        for page in allpages:
          print(page.name,file = tc_pages)
    elif name == "en"or"all":
      allpages= en.allpages()
      with open("dict/en_pages.txt","w") as en_pages:
        for page in allpages:
          print(page.name,file = en_pages)
  @commands.command(name='wiki',aliases=['維基'],brief="查詢維基頁面",description="查詢`page`的維基頁面")
  async def wiki(self,ctx,*page):
    name = " ".join(page)
    with open("dict/zh_pages.txt","r") as zh_pages:
      zhpage = []
      for page in zh_pages.readlines():
        zhpage.append(page)
    with open("dict/tc_pages.txt","r") as tc_pages:
      tcpage = []
      for page in tc_pages.readlines():
        tcpage.append(page)
    with open("dict/en_pages.txt","r") as en_pages:
      enpage = []
      for page in en_pages.readlines():
        enpage.append(page)
    title,ratio = process.extractOne(name,zhpage)
    if ratio>75:
      footer = "灰機"
      URL = f"https://{zhURL}/wiki/{title}"
    else:
      title,ratio = process.extractOne(name,tcpage)
      if ratio>75:
        footer = "繁體"
        URL = f"https://{tcURL}/zh-tw/wiki/{title}"
      else:
        title,ratio = process.extractOne(name,enpage)
        if ratio>75:
          footer = "英文"
          URL = f"https://{enURL}/wiki/{title}"
        else:
          await ctx.send("Ordis找不到指揮官想要的頁面呢")
          return
    embed = discord.Embed(title=title,url=URL)
    embed.set_footer(text=footer)
    await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(wiki(bot))