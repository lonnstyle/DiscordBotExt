import discord
from discord.ext import commands
from core.classes import Cog_Extension
import os
import requests
import json

Chi = ["玩家","幽靈氏族","暗影氏族","風暴氏族","山脈氏族","月亮氏族"]

class OrphixRank(Cog_Extension):
  tag = "Warframe"
  @commands.command(name='orphix', aliases=['奧菲斯'])
  async def orphix(self, ctx, *args):
    count = 0
    name = " ".join(args)
    raw = requests.get("http://content.warframe.com/dynamic/orphixVenomJS.php")
    if raw.status_code != 200:
      await ctx.send("API異常！Ordis建議指揮官晚點再次查詢。")
    else:
      leaderBoard = json.loads(raw.text)
      players = leaderBoard['Players']
      ghostClans = leaderBoard['GhostClans']
      shadowClans = leaderBoard['ShadowClans']
      stormClans = leaderBoard['StormClans']
      mountainClans = leaderBoard['MountainClans']
      moonClans = leaderBoard['MoonClans']
      for types in [players,ghostClans,shadowClans,stormClans,mountainClans,moonClans]:
        for id in types:
          if name == id['n']:
            await ctx.send(f"{Chi[count]}{name}的排行為{id['r']},分數{id['s']}")
            return
        count += 1
      await ctx.send("指揮官所查詢的氏族/玩家不在榜上,請繼續加油！")

def setup(bot):
    bot.add_cog(OrphixRank(bot))
