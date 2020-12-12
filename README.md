# DiscordBotMods
Warframe Discord 機器人<br/>
基於[MeowXiaoXiang](https://github.com/MeowXiaoXiang/Meow_Bot-Public_Version-/commits?author=MeowXiaoXiang)的[Meow_Bot-Public_Version-](https://github.com/MeowXiaoXiang/Meow_Bot-Public_Version-)開發的Mod<br/>
## Mod列表<br/>
* [worldState.py](worldState.py)查詢當前世界循環狀態<br/>
* [rivenPrice.py](rivenPrice.py)查詢[wfm](https://warframe.market)上最低價格的五張該武器紫卡<br/>
  * 必須搭配[dict](dict)當中的[Weapons.json](Weapons.json)以及[attributes.json](attributes.json)使用
* [baroManual.py](baroManual.py)查詢虛空商人Baro Ki'Teer的目前狀態<br/>
  * 感謝[pa001024](https://github.com/pa001024)允許使用[riven.im](https://riven.im)項目的繁體翻譯檔[zh-Hant.json](https://raw.githubusercontent.com/lonnstyle/riven-mirror/dev/src/i18n/lang/zh-Hant.json)作為Dict
* [wfm.py](wfm.py)查詢物品於[wfm](https://warframe.market)上最低價的五個賣家訂單<br/>
  需要翻譯Dict以支持功能運行
 * 官方翻譯：[GitLocalize](https://gitlocalize.com/repo/5556/zh/dict/items_en.json)
 * 自定義暱稱：[Google Sheet](https://docs.google.com/spreadsheets/d/1AMxTBp1_HdVbjdxnpTGqy_16OoP-CBeBc9117ZXGhEQ/edit?usp=sharing)
