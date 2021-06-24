common.py
=====
common為機器人慣用功能統整的擴展。<br/>

## 指令列表
```
[ping|延遲|機器人延遲|delay]
```
顯示機器人當前延遲
```
[sayd|說|機器人說] <msg>
```
讓機器人代替你說出<msg>的內容
```
[poll|投票] <topic> <option1> <emoji1> <option2> <emoji2>
```
讓機器人發起一項投票

|鍵值|接受的數值|數據類別|
|----|----|----|
|`topic`|投票的主題|`str`|
|`option1`|選項1|`str`|
|`emoji1`|代表選項1的表情符號|`emoji`|
|`option2`|選項2|`str`|
|`emoji2`|代表選項2的表情符號|`emoji`|
