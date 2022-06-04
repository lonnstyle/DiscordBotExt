import json
import logging
import os

import requests

logger = logging.getLogger('language')
logger.setLevel(-1)
# display all logging messages
dirname = os.path.dirname(__file__)
handler = logging.FileHandler(filename=os.path.join(dirname, '../log/runtime.log'), encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(lineno)d: %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
logger.addHandler(handler)


class language():
    def init(self):
        try:
            self.zh_hant = json.loads(requests.get("https://raw.githubusercontent.com/lonnstyle/DiscordBotExt/v3.0/localization/locales/zh-hant.json").text)
            self.zh_hans = json.loads(requests.get("https://raw.githubusercontent.com/lonnstyle/DiscordBotExt/v3.0/localization/locales/zh-hans.json").text)
            self.en = json.loads(requests.get("https://raw.githubusercontent.com/lonnstyle/DiscordBotExt/v3.0/localization/locales/en.json").text)
            logger.debug("[init] successfully pulled loc file from github")
        except Exception as exc:
            logger.error(exc)
        self.pref = json.load(open(os.path.join(dirname, "../setting.json"), 'r', encoding='utf8'))
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
