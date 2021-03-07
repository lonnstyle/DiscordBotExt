import discord
from discord.ext import commands
from core.classes import Cog_Extension
import os
import json

with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)


class admin(Cog_Extension):
    tag = "admin"
    #清除訊息
    @commands.command(name='clear', aliases=['clean' , '清除'],brief="刪除聊天記錄",description="clear [指定數量]\n刪除指定數量的聊天記錄")
    async def clear(self,ctx,num:int):
        if ctx.message.author.id == ctx.guild.owner_id:
            await ctx.channel.purge(limit=num+1)
            print(str(ctx.message.author)+' ---ID '+str(ctx.message.author.id)+'在 << '+str(ctx.channel.name)+' >> 頻道使用了clear指令刪除了'+str(int(num))+'個對話')             
        else:
          embed = discord.embed(title="權限不足",description='本指令只提供給伺服器傭有者 \n本伺服器擁有者為 <@' + str(ctx.guild.owner_id) + '>')
          await ctx.send(embed=embed)
    
def setup(bot):
    bot.add_cog(admin(bot))