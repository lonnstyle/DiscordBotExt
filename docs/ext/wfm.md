wfm.py
=====
wfm為與[wf.m](https://warframe.market)相關功能統整的擴展。

##指令列表
```
[translate|trans|翻譯] <item>
```
查詢`item`的翻譯名

```
[wfm|wm|市場查詢] <args>
```
根據`args`查詢[wf.m](https://warframe.market)上的訂單
`args`接受以下參數:

|鍵值|接受的數值|數據類別|必須|
|----|----|----|----|
|`type`|買賣類別|`str`|`False`|
|`item`|物品|`str`|`True`|
|`rank`|等級|`str`|`False`|
