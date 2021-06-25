event.py
=====
event為機器人監視活動更新的擴展。<br/>

## 指令列表
```
[reactionRole|rr] <message>
```
指定可自動分發身份組的訊息

--------
`message`<br/>
類別:`int`<br/>
自動分發身份組訊息ID
--------
```
[role|身份組] <role> <emoji>
```
新增可自動分發的身份組

------
`role`<br/>
類別:`str`<br/>
可自動分發的身份組名稱
------
`emoji`<br/>
類別:`emoji`<br/>
用於獲取身份組的emoji

-------
## 監聽事件
```
on_message()
```
當有用戶發送信息時會自動記錄於`log`文件夾中，並輸出到控制台中。

------
```
on_raw_reaction_add()
```
用於檢測上述對應的`role`和`reactionRole`更新，並發放身份組
