import json
import requests

class language():
  def __init__(self):
    self.zh_hant = json.loads(requests.get("https://raw.githubusercontent.com/lonnstyle/DiscordBotExt/main/zh-hant.json").text)
    self.pref = json.load(open("setting.json",'r',encoding='utf8'))
    self.pref = self.pref.get("language","zh-hant")
  def langpref(self):
    if self.pref == 'zh-hant':
      return self.zh_hant
    else:
      return json.load(open(self.pref,"r",encoding='utf8'))
      