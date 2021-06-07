Quick Install
=====
Assuming you had already installed [python 3](https://www.python.org/), you can install the Discord bot from the [GitHub Release](https://github.com/lonnstyle/DiscordBotExt/releases) .<br/>

## Required packages
```
-pip install discord
-pip install chinese_converter
-pip install discord-webhook
-pip install mwclient
-pip install fuzzywuzzy
-pip install flask
-pip install discord-py-slash-command
```

## Create bot account
Follow [discord.py](https://discordpy.readthedocs.io/en/stable/discord.html)'s tutorial to create and invite your bot.<br/>
The bot will need the following premissions:
```
WIP
```

## Configure [setting.json](https://github.com/lonnstyle/DiscordBotExt/blob/main/setting.json)
Blank template as follow:
```json
{
    "TOKEN": "",
    "command_prefix":"",
    "webhook":"",
    "user":"",
    "self":"",
    "watching":"",
    "publish":
}
```
|key|accepting value|type|
|----|----|----|
|TOKEN|bot's token|str|
|command_prefix|the prefix to raise bot command|str|
|webhook|webhook address for webhook embed responses|str|
|user|the nickname for the bot to call users|str|
|self|the nickname for the bot to call self|str|
|watching|the status of bot|str|
|publish|channel ID of self-publishing message sent by `sayd` command|int|