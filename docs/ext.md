指令擴展
==========
於[cmds](https://github.com/lonnstyle/DiscordBotExt/tree/main/cmds)文件中均為機器人的指令擴展，其他放置於此文件夾內的`.py`文件亦會被視為指令擴展自動加載。<br/>

## 空白的指令擴展模板
```py
from discord.ext import commands
from core.classes import Cog_Extension
import discord

class 自訂名稱(Cog_Extension):
	
	@commands.command(name=指令名稱,aliases=[指令別稱],brief=指令簡介,description=指令詳情)
	async def 指令功能(self,ctx):
		...
		
	def setup(bot):
		bot.add_cog(自訂名稱(bot))
```
## 現成的指令擴展
```{toctree}
:maxdepth: 1

ext/admin
ext/baro
ext/common
ext/event
ext/logup
ext/OrphixRank
ext/rivenPrice
ext/wfm
ext/wiki
ext/worldState
```