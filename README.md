# DiscordBotExt
Warframe Discord 機器人<br/>
基於[MeowXiaoXiang](https://github.com/MeowXiaoXiang/Meow_Bot-Public_Version-/commits?author=MeowXiaoXiang)的[Meow_Bot-Public_Version-](https://github.com/MeowXiaoXiang/Meow_Bot-Public_Version-)開發的Mod<br/>
與[Meow_Bot-Public_Version-](https://github.com/MeowXiaoXiang/Meow_Bot-Public_Version-)兼容,但[main.py](main.py)為調整過後的優化版本,兼容性更佳

## 第三方庫列表<br/>
* -pip install discord
* -pip install chinese_converter
* -pip install discord-webhook
* -pip install mwclient
* -pip install fuzzywuzzy
* -pip install flask

## Mod列表<br/>
* [worldState.py](cmds/worldState.py)查詢當前世界循環狀態<br/>
  * 使用[WFCD](https://github.com/WFCD/)的[API](https://docs.warframestat.us/)數據
* [rivenPrice.py](cmds/rivenPrice.py)查詢[wfm](https://warframe.market)上最低價格的五張該武器紫卡<br/>
  * 必須搭配[dict](dict)當中的[Weapons.json](Weapons.json)以及[attributes.json](attributes.json)使用
  * [Weapons.json]當中的武器名稱有機會不齊全，若有無法查詢的武器且你確保自己沒有輸入錯誤，請向我回報bug
* [baro.py](cmds/baro.py)查詢虛空商人Baro Ki'Teer的目前狀態<br/>
  * 感謝[pa001024](https://github.com/pa001024)允許使用[riven.im](https://riven.im)項目的繁體翻譯檔[zh-Hant.json](https://raw.githubusercontent.com/lonnstyle/riven-mirror/dev/src/i18n/lang/zh-Hant.json)作為Dict
  -pip install chinese-converter
* [wfm.py](cmds/wfm.py)查詢物品於[wfm](https://warframe.market)上的訂單<br/>
  -pip install discord-webhook
  * 請在setting.json當中加入以下數據(可選)：
    "webhook": "<你的webhook URL>"
  * <s>自定義暱稱：[Google Sheet](https://docs.google.com/spreadsheets/d/1AMxTBp1_HdVbjdxnpTGqy_16OoP-CBeBc9117ZXGhEQ/edit?usp=sharing)</s>
* [wiki.py](cmds/wiki.py)生成wiki鏈接<br/>
  -pip install mwclient
  -pip install fuzzywuzzy
  * 查詢順序為[簡中](https://warframe.huijiwiki.com)→[繁中](https://warframe.fandom.com/zh-tw)→[英文](https://warframe.fandom.com)

## 指令列表<br/>
* 請於安裝機器人後使用**help**指令查看

## 安裝機器人<br/>
* 將本repo下載,刪去[dict](dict)文件夾(會自動下載本repo當中的最新版本)
* 填寫[setting.json](setting.json)當中留空的部分
  * [Token](https://discord.com/developers/applications)與[Webhook](https://support.discord.com/hc/zh-tw/articles/228383668-%E4%BD%BF%E7%94%A8%E7%B6%B2%E7%B5%A1%E9%89%A4%E6%89%8B-Webhooks-)請按照Discord官方的設置獲取
* 安裝前述的 **-pip install 第三方庫**
* 到你的[Discord開發者頁面](https://discord.com/developers/applications)邀請你的機器人進伺服器
* 執行[main.py](main.py),你就會看到你的機器人上線啦
<br/><br/>
<a href="https://www.patreon.com/bePatron?u=47066858" data-patreon-widget-type="贊助lonnstyle開發機器人">贊助lonnstyle開發機器人</a>
