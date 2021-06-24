快速安裝
=====
假設你已經安裝了[python 3](https://www.python.org/)，你可以直接從[GitHub Release](https://github.com/lonnstyle/DiscordBotExt/releases)下載機器人所需要的文件。<br/>

## 需要的模組
```
-pip install discord
-pip install chinese_converter
-pip install discord-webhook
-pip install mwclient
-pip install fuzzywuzzy
-pip install flask
-pip install discord-py-slash-command
```

## 創建機器人賬號
跟隨[discord.py的教學](https://discordpy.readthedocs.io/en/stable/discord.html)創建並邀請你的機器人。<br/>
機器人會需要以下權限：
```
add_reactions
read_messages
send_messages
manage_messages
embed_links
attach_files
read_message_history
mention_everyone
external_emojis
manage_roles
manage_webhooks
```

## 設置[setting.json](https://github.com/lonnstyle/DiscordBotExt/blob/main/setting.json)
以下為空白模板:
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
|鍵值|接受的數值|數據類別|
|----|----|----|
|`TOKEN`|機器人的token|`str`|
|`command_prefix`|機器人執行指令的前綴|`str`|
|`webhook`|機器人發webhook嵌入信息的鏈接|`str`|
|`user`|機器人對用戶的稱呼|`str`|
|`self`|機器人的自稱|`str`|
|`watching`|機器人的自訂狀態|`str`|
|`publish`|機器人自動發佈`sayd`信息的頻道ID|`int`|
|`language`|機器人顯示語言|`str`|

**註:`language`僅接受`zh-hant`(繁體)、`zh-hans`(簡體)與`en`(英文)，你也可以指定自定義翻譯的路徑**