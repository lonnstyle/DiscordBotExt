import json
import logging
from asyncio.log import logger

import requests

logging.getLogger('language')
logger.setLevel(-1)
# display all logging messages
handler = logging.FileHandler(filename='log/runtime.log', encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


class language():
    def init(self):
        #     pass

        # def init(self):
        self.zh_hant = json.loads(requests.get("https://raw.githubusercontent.com/lonnstyle/DiscordBotExt/main/localization/zh-hant.json").text)
        self.zh_hans = json.loads(requests.get("https://raw.githubusercontent.com/lonnstyle/DiscordBotExt/main/localization/zh-hans.json").text)
        self.en = json.loads(requests.get("https://raw.githubusercontent.com/lonnstyle/DiscordBotExt/main/localization/en.json").text)
        logger.debug("[init] successfully pulled loc file from github")
        self.pref = json.load(open("setting.json", 'r', encoding='utf8'))
        self.pref = self.pref.get("language", "zh-hant")
        logger.debug(f'[init] language preference set: {self.pref}')

    def langpref(self):
        if self.pref == 'zh-hant':
            return self.zh_hant
        elif self.pref == 'zh-hans':
            return self.zh_hans
        elif self.pref == 'en':
            return self.en
        else:
            try:
                return json.load(open(self.pref, "r", encoding='utf8'))
            except Exception as exc:
                logging.critical(exc)


# lang = language()
