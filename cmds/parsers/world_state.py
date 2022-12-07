import json
import logging
import os
from pprint import pprint

import requests
from mobile_export import MobileExportParser

# from localization.language import language

dirname = os.path.dirname(__file__)

logger = logging.getLogger('worldState')
logger.setLevel(-1)
handler = logging.FileHandler(filename=os.path.join(dirname, '../../log/runtime.log'), encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(lineno)d: %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
logger.addHandler(handler)


class WorldStateParser():
    def __init__(self):
        self.url = "https://content.warframe.com/dynamic/worldState.php"
        self.data = {}
        # with open(os.path.join(dirname, '../../setting.json'), 'r') as _jfile:
        #     jdata = json.load(_jfile)
        # self.language = jdata['language']
        self.language = 'en'
        self.manifests = MobileExportParser()
        self.manifests_dir = MobileExportParser.manifests_dir

    def __get_timestamp(self, timestamp):
        return int(timestamp['$date']['$numberLong'])/1000
        # return timestamp in second. DE provided them as ms

    def __get_data(self):
        resp = requests.get(self.url)
        resp.raise_for_status()
        self.data = json.loads(resp.text)

    def get_baro(self):
        if self.data == {}:
            self.__get_data()
        self.baro = self.data['VoidTraders'][0]
        node = self.baro['Node']
        node = self.manifests.nodes.get(node, node)
        if type(node) is not str:
            node_name = node[self.language]['name']
            system = node[self.language]['system']
        else:
            node_name = node
            system = 'Unknown'
        arrive = self.__get_timestamp(self.baro['Activation'])
        expiry = self.__get_timestamp(self.baro['Expiry'])
        items = {}
        for item in self.baro.get('Manifest', {}):
            _item = self.manifests.manifest_data.get(item['ItemType'], item['ItemType'])
            items[_item] = {
                'PrimePrice': item.get('PrimePrice', 0),
                'RegularPrice': item.get('RegularPrice', 0)
            }
        return arrive, expiry, node_name, system, items

    def get_varzia(self):
        '''
        get offering list of PrimeVaultTraders
        :returns start: timestamp of current Prime Resurgence start
        :returns end: timestamp of current Prime Resurgence end
        :returns item: list of offering items, with item name and Price
        '''
        if self.data == {}:
            self.__get_data()
        self.varzia = self.data['PrimeVaultTraders'][0]
        start = self.__get_timestamp(self.varzia['Activation'])
        end = self.__get_timestamp(self.varzia['Expiry'])
        _items = self.varzia['Manifest']
        items = {}
        for item in _items:
            game_ref = item['ItemType'].replace("/StoreItems/", "/")
            _item = self.manifests.manifest_data.get(game_ref, None)
            if _item is None:
                continue
            items[_item[self.language]['item_name']] = {
                'PrimePrice': item.get('PrimePrice', 0),
                'RegularPrice': item.get('RegularPrice', 0)
            }
        return start, end, items

    def get_sortie(self):
        if self.data == {}:
            self.__get_data()
        self.sortie = self.data['Sorties'][0]
        start = self.__get_timestamp(self.sortie['Activation'])
        end = self.__get_timestamp(self.sortie['Expiry'])
        boss = self.sortie['Boss']
        missions = self.sortie['Variants']
        for mission in missions:
            mission['node'] = self.manifests.nodes.get(mission['node'], mission['node'])
        return start, end, boss, missions

    def get_archon(self):
        if self.data == {}:
            self.__get_data()
        self.archon = self.data['LiteSorties'][0]
        start = self.__get_timestamp(self.archon['Activation'])
        end = self.__get_timestamp(self.archon['Expiry'])
        boss = self.archon['Boss']
        missions = self.archon['Missions']
        for mission in missions:
            mission['node'] = self.manifests.nodes.get(mission['node'], mission['node'])
        return start, end, boss, missions

    def get_fissure(self):
        self.__get_data()
        # always ask for new data cuz fissures are dynamically updated
        self.fissure = self.data['ActiveMissions']
        for mission in self.fissure:
            mission['Activation'] = self.__get_timestamp(mission['Activation'])
            mission['Expiry'] = self.__get_timestamp(mission['Expiry'])
            mission['Node'] = self.manifests.nodes.get(mission['Node'], mission['Node'])
            del mission['_id']
            del mission['Region']
            del mission['Seed']
        return self.fissure

    def get_voidstorms(self):
        self.__get_data()
        # always ask for new data cuz voidstorms are dynamically updated
        self.voidstorm = self.data['VoidStorms']
        for mission in self.voidstorm:
            mission['Activation'] = self.__get_timestamp(mission['Activation'])
            mission['Expiry'] = self.__get_timestamp(mission['Expiry'])
            mission['Node'] = self.manifests.nodes.get(mission['Node'], mission['Node'])
            del mission['_id']
            del mission['Region']
            del mission['Seed']
        return self.voidstorm

    def get_daily_deals(self):
        self.__get_data()
        # always ask for new data cuz amountSold is dynamically updated
        self.daily_deals = self.data['DailyDeals']
        self.daily_deals['Activation'] = self.__get_timestamp(self.daily_deals['Activation'])
        self.daily_deals['Expiry'] = self.__get_timestamp(self.daily_deals['Expiry'])
        return self.daily_deals

    def get_nightwave(self):
        if self.data == {}:
            self.__get_data()
        if 'SeasonInfo' not in self.data:
            return None
        self.nightwave = self.data['SeasonInfo']
        self.nightwave['Activation'] = self.__get_timestamp(self.nightwave['Activation'])
        self.nightwave['Expiry'] = self.__get_timestamp(self.nightwave['Expiry']
                                                        )
        if 'affiliationTag' not in self.manifests.nightwave or self.manifests.nightwave['affiliationTag'] != self.nightwave['AffiliationTag']:
            self.manifests.update()
        for challenge in self.nightwave['ActiveChallenges']:
            del challenge['_id']
            challenge['Activation'] = self.__get_timestamp(challenge['Activation'])
            challenge['Expiry'] = self.__get_timestamp(challenge['Expiry'])
            challenge_info = self.manifests.nightwave['challenges'].get(challenge['Challenge'])
            if challenge_info is None:
                challenge['name'] = 'Unknown'
                challenge['standing'] = 'Unknown'
            else:
                challenge['name'] = challenge_info[self.language]['name']
                challenge['standing'] = challenge_info['standing']
        del self.nightwave['Params']
        del self.nightwave['Phase']
        del self.nightwave['Season']
        return self.nightwave


if __name__ == '__main__':
    parser = WorldStateParser()
    parser.manifests.update()
    pprint(parser.get_nightwave())
