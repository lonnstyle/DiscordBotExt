import json
import logging
import os
from datetime import datetime
from pprint import pprint

import requests
from const import AVAILABLE_LANGUAGES
from mobile_export import MobileExportParser

# from localization.language import language

dirname = os.path.dirname(__file__)

logger = logging.getLogger("worldState")
logger.setLevel(-1)
handler = logging.FileHandler(
    filename=os.path.join(dirname, "../../log/runtime.log"), encoding="utf-8", mode="a"
)
handler.setFormatter(
    logging.Formatter(
        "%(asctime)s:%(levelname)s:%(name)s:%(lineno)d: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
)
logger.addHandler(handler)


class Sortie:
    start = 1
    end = 1
    boss = None
    missions = []
    data = {}


class Archon(Sortie):
    def __init__(self):
        super().__init__()


class Baro():
    data = {}
    start = 1
    end = 1
    node = {"name": "", "system": ""}
    items = {}


class Varzia(Baro):
    def __init__(self) -> None:
        super().__init__()
        # delattr(self,'node')


class Nightwave():
    data = {}
    start = 1
    end = 1


class WorldStateParser:
    url = "https://content.warframe.com/dynamic/worldState.php"
    data = {}
    manifests = MobileExportParser()
    manifests_dir = MobileExportParser.manifests_dir
    sortie = Sortie()
    archon = Archon()
    baro = Baro()
    last_update = 1
    varzia = Varzia()
    nightwave = Nightwave()

    def __init__(self, language=None):
        if language:
            self.language = language
        else:
            with open("setting.json", "r") as _jfile:
                jdata = json.load(_jfile)
            self.language = jdata["language"]
    

    def __get_timestamp(self, timestamp):
        """
        __get_timestamp get timestamp from worldState

        :param timestamp: timestamp from worldState in ms
        :type timestamp: dict
        :return: parsed timestamp
        :rtype: int
        """
        return int(timestamp["$date"]["$numberLong"]) // 1000
        # return timestamp in second. DE provided them as ms

    def __get_data(self, force=False):
        if force or self.last_update + 300 <= datetime.now().timestamp():
            # timeout
            resp = requests.get(self.url)
            resp.raise_for_status()
            self.data = json.loads(resp.text)
            self.last_update = self.__now()

    def __now(self):
        return int(datetime.now().timestamp())
    
    def __dump(self, obj, lang=None):
        if lang is None:
            lang = self.language
        for attr in obj[lang]:
            obj[attr] = obj[lang][attr]
        for _lang in AVAILABLE_LANGUAGES:
            del obj[_lang]
        return obj


    def __expired(self, obj):
        return self.__now() >= obj.end if hasattr(obj, 'end') else True

    def get_baro(self):
        if self.data == {} or self.__expired(self.baro):
            self.__get_data()
            self.baro.data = self.data["VoidTraders"][0]
            node = self.baro.data["Node"]
            node = self.manifests.nodes.get(node, node)
            if type(node) is not str:
                self.baro.node['name'] = node[self.language]["name"]
                self.baro.node['system'] = node[self.language]["system"]
            else:
                self.baro.node['name'] = node
                self.baro.node['system'] = "Unknown"
            self.baro.start = self.__get_timestamp(self.baro.data["Activation"])
            self.baro.end = self.__get_timestamp(self.baro.data["Expiry"])
            self.baro.items = {}
            for item in self.baro.data.get("Manifest", {}):
                _item = self.manifests.manifest_data.get(item["ItemType"], item["ItemType"])
                self.baro.items[_item] = {
                    "PrimePrice": item.get("PrimePrice", 0),
                    "RegularPrice": item.get("RegularPrice", 0),
                }
        return self.baro.start, self.baro.end, self.baro.node['name'], self.baro.node['system'], self.baro.items

    def get_varzia(self):
        """
        get offering list of PrimeVaultTraders
        :returns start: timestamp of current Prime Resurgence start
        :returns end: timestamp of current Prime Resurgence end
        :returns item: list of offering items, with item name and Price
        """
        if self.data == {} or self.__expired(self.varzia):
            self.__get_data()
            self.varzia.data = self.data["PrimeVaultTraders"][0]
            self.varzia.start = self.__get_timestamp(self.varzia.data["Activation"])
            self.varzia.end = self.__get_timestamp(self.varzia.data["Expiry"])
            _items = self.varzia.data["Manifest"]
            self.varzia.items = {}
            for item in _items:
                game_ref = item["ItemType"].replace("/StoreItems/", "/")
                _item = self.manifests.manifest_data.get(game_ref, None)
                if _item is None:
                    continue
                self.varzia.items[_item[self.language]["item_name"]] = {
                    "PrimePrice": item.get("PrimePrice", 0),
                    "RegularPrice": item.get("RegularPrice", 0),
                }
        return self.varzia.start, self.varzia.end, self.varzia.items

    def get_sortie(self):
        if self.data == {} or self.__expired(self.sortie):
            self.__get_data()
            self.sortie.data = self.data["Sorties"][0]
            self.sortie.start = self.__get_timestamp(self.sortie.data["Activation"])
            self.sortie.end = self.__get_timestamp(self.sortie.data["Expiry"])
            self.sortie.boss = self.sortie.data["Boss"]
            self.sortie.missions = self.sortie.data["Variants"]
            for mission in self.sortie.missions:
                mission["node"] = self.manifests.nodes.get(mission["node"], mission["node"])
                if type(mission['node']) is not str:
                    mission['node'] = self.__dump(mission['node'])
        return self.sortie.start, self.sortie.end, self.sortie.boss, self.sortie.missions

    def get_archon(self):
        if self.data == {} or self.__expired(self.archon):
            self.__get_data()
            self.archon.data = self.data["LiteSorties"][0]
            self.archon.start = self.__get_timestamp(self.archon.data["Activation"])
            self.archon.end = self.__get_timestamp(self.archon.data["Expiry"])
            self.archon.boss = self.archon.data["Boss"]
            self.archon.missions = self.archon.data["Missions"]
            for mission in self.archon.missions:
                mission["node"] = self.manifests.nodes.get(mission["node"], mission["node"])
        return self.archon.start, self.archon.end, self.archon.boss, self.archon.missions

    def get_fissure(self):
        self.__get_data()
        # always ask for new data cuz fissures are dynamically updated
        self.fissure = self.data["ActiveMissions"]
        for mission in self.fissure:
            mission["Activation"] = self.__get_timestamp(mission["Activation"])
            mission["Expiry"] = self.__get_timestamp(mission["Expiry"])
            mission["Node"] = self.manifests.nodes.get(mission["Node"], mission["Node"])
            del mission["_id"]
            del mission["Region"]
            del mission["Seed"]
        return self.fissure

    def get_voidstorms(self):
        self.__get_data()
        # always ask for new data cuz voidstorms are dynamically updated
        self.voidstorm = self.data["VoidStorms"]
        for mission in self.voidstorm:
            mission["Activation"] = self.__get_timestamp(mission["Activation"])
            mission["Expiry"] = self.__get_timestamp(mission["Expiry"])
            mission["Node"] = self.manifests.nodes.get(mission["Node"], mission["Node"])
            del mission["_id"]
            del mission["Region"]
            del mission["Seed"]
        return self.voidstorm

    def get_daily_deals(self):
        self.__get_data()
        # always ask for new data cuz amountSold is dynamically updated
        self.daily_deals = self.data["DailyDeals"]
        self.daily_deals["Activation"] = self.__get_timestamp(
            self.daily_deals["Activation"]
        )
        self.daily_deals["Expiry"] = self.__get_timestamp(self.daily_deals["Expiry"])
        return self.daily_deals

    def get_nightwave(self):
        if self.data == {}:
            self.__get_data()
        self.nightwave.data = self.data["SeasonInfo"]
        self.nightwave.start = self.__get_timestamp(
            self.nightwave.data["Activation"]
        )
        self.nightwave.end = self.__get_timestamp(self.nightwave.data["Expiry"])
        if (
            "affiliationTag" not in self.manifests.nightwave
            or self.manifests.nightwave["affiliationTag"]
            != self.nightwave.data["AffiliationTag"]
        ):
            self.manifests.update()
        for challenge in self.nightwave.data["ActiveChallenges"]:
            del challenge["_id"]
            challenge["Activation"] = self.__get_timestamp(challenge["Activation"])
            challenge["Expiry"] = self.__get_timestamp(challenge["Expiry"])
            challenge_info = self.manifests.nightwave["challenges"].get(
                challenge["Challenge"]
            )
            del challenge['Challenge']
            if challenge_info is None:
                challenge["name"] = "Unknown"
                challenge["standing"] = "Unknown"
            else:
                challenge["name"] = challenge_info[self.language]["name"]
                challenge["standing"] = challenge_info["standing"]
        del self.nightwave.data["Params"]
        del self.nightwave.data["Phase"]
        del self.nightwave.data["Season"]
        if "SeasonInfo" not in self.data:
            return None
        return self.nightwave.data


if __name__ == "__main__":
    parser = WorldStateParser('en')
    parser.manifests.update()
    pprint(parser.get_sortie())
