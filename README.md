# DiscordBotMods
Warframe Discord 機器人<br/>
基於[MeowXiaoXiang](https://github.com/MeowXiaoXiang/Meow_Bot-Public_Version-/commits?author=MeowXiaoXiang)的[Meow_Bot-Public_Version-](https://github.com/MeowXiaoXiang/Meow_Bot-Public_Version-)開發的Mod<br/>
## Mod列表<br/>
* [worldState.py](worldState.py)查詢當前世界循環狀態<br/>
  * 使用[WFCD](https://github.com/WFCD/)的[API](https://docs.warframestat.us/)數據
* [rivenPrice.py](rivenPrice.py)查詢[wfm](https://warframe.market)上最低價格的五張該武器紫卡<br/>
  * 必須搭配[dict](dict)當中的[Weapons.json](Weapons.json)以及[attributes.json](attributes.json)使用
  * [Weapons.json]當中的武器名稱有機會不齊全，若有無法查詢的武器且你確保自己沒有輸入錯誤，請向我回報bug
* [baroManual.py](baroManual.py)查詢虛空商人Baro Ki'Teer的目前狀態<br/>
  * 感謝[pa001024](https://github.com/pa001024)允許使用[riven.im](https://riven.im)項目的繁體翻譯檔[zh-Hant.json](https://raw.githubusercontent.com/lonnstyle/riven-mirror/dev/src/i18n/lang/zh-Hant.json)作為Dict
  -pip install chinese-converter
* [wfm.py](wfm.py)查詢物品於[wfm](https://warframe.market)上最低價的五個賣家訂單<br/>
  需要翻譯Dict以支持功能運行
  * 官方翻譯：[GitLocalize](https://gitlocalize.com/repo/5556/zh/dict/items_en.json)
  * 自定義暱稱：[Google Sheet](https://docs.google.com/spreadsheets/d/1AMxTBp1_HdVbjdxnpTGqy_16OoP-CBeBc9117ZXGhEQ/edit?usp=sharing)

## 指令列表<br/>
**所有指令均需要搭配指令前綴使用，可在機器人框架中的setting.json中修改
* [worldState.py](worldState.py)當中的指令
  * POE/夜靈平原時間/poe  查詢夜靈平原目前日夜循環狀態和剩餘時間
  * Earth/地球時間  查詢地球目前日夜循環狀態和剩餘時間
  * Cambion/魔裔禁地時間  查詢魔裔禁地目前日夜循環狀態和剩餘時間
  * Orb/奧布山谷時間/orb  查詢奧布山谷目前日夜循環狀態和剩餘時間
  * Arbitration/仲裁  查詢目前仲裁任務和剩餘時間（此功能由於API不穩定，返回數據未必準確）
  * Sortie/突擊/sortie  查詢目前突擊任務和剩餘時間
* [rivenPrice.py](rivenPrice.py)當中的指令
  * riven/紫卡/紫卡查詢 [武器名稱]  查詢該武器最低價的三個在線賣家訂單
* [baroManual.py](baroManual.py)當中的指令
  * baro/奸商/Baro  查詢虛空商人Baro Ki'Teer目前狀態，如已經抵達中繼站則會顯示所攜帶商品列表
  * 此功能的自動版正在壓力測試中
* [wfm.py](wfm.py)當中的指令
  * wfm/wm/市場查詢 [物品名稱]  查詢該物品於wf.m上最低價的五名賣家訂單
  * 此功能所使用的Dict尚未編寫完成
  * 使用[GitLocalize](https://gitlocalize.com/repo/5556/zh/dict/items_en.json)協助完成官方翻譯的Dict編寫
  * 使用[Google Sheet](https://docs.google.com/spreadsheets/d/1AMxTBp1_HdVbjdxnpTGqy_16OoP-CBeBc9117ZXGhEQ/edit?usp=sharing)編寫自定義Dict
