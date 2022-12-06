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
        #TODO
        pass

    def get_archon(self):
        #TODO LiteSorties
        pass

    def get_fissure(self):
        #TODO
        pass

    def get_voidstorms(self):
        #TODO
        pass

    def get_daily_deals(self):
        #TODO
        pass

    

if __name__ == '__main__':
    parser = WorldStateParser()
    pprint(parser.get_baro())
