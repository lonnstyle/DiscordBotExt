from flask import Flask, request
from threading import Thread
import json
import logging
from http.server import BaseHTTPRequestHandler
import zlib
from discord_webhook import DiscordWebhook, DiscordEmbed

app = Flask('')

with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

@app.route('/post',methods=['POST'])
def post():
  raw = request.get_data()
  try:
    raw = zlib.decompress(raw)
    raw = json.loads(raw.decode('utf-8'))
  except:
    raw = json.loads(raw)
  challenge = raw['d'].get("challenge",None)
  if challenge != None:
    challenge = {"challenge": challenge}
    print(json.dumps(challenge))
    return json.dumps(challenge)
  else:
    author = raw['d']['extra']['author']
    if author['bot'] == False:
      nickname = author['nickname']
      if nickname == '':
        nickname = author['username']
      avatar = author['avatar']
      content = raw['d']['content']
      webhook = DiscordWebhook(url=jdata['forward_webhook'])
      embed = DiscordEmbed(title=content)
      embed.set_author(name=nickname, icon_url=avatar)
      webhook.add_embed(embed)
      response = webhook.execute()
      print(response)
    return "200"
  
@app.route('/',methods=['GET','POST','HEAD'])
def main():
  if request.method == 'GET':
    return '機器人在綫!'
  elif request.method == 'POST':
    raw = request.get_data()
    print("raw=",raw)
    try:
      raw = zlib.decompress(raw)
      print(raw)
      raw = json.loads(raw.decode('utf-8'))
    except:
      print(raw)
      raw = json.loads(raw)
    challenge = raw['d'].get("challenge",None)
    if challenge != None:
      challenge = {"challenge": challenge}
      print(json.dumps(challenge))
      return json.dumps(challenge)
    else:
      author = raw['d']['extra']['author']
      if author['bot'] == False:
        nickname = author['nickname']
        if nickname == '':
          nickname = author['username']
        avatar = author['avatar']
        content = raw['d']['content']
        webhook = DiscordWebhook(url=jdata['forward_webhook'])
        embed = DiscordEmbed(title=content)
        embed.set_author(name=nickname, icon_url=avatar)
        webhook.add_embed(embed)
        response = webhook.execute()
      return "200"
  else:
    print(request.get_data)
    return"200"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()

