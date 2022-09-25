import json
import logging
import os

import requests
from mobile_export import MobileExportParser

from localization.language import language

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
        with open(os.path.join(dirname, '../../setting.json'), 'r') as _jfile:
            jdata = json.load(_jfile)
        self.language = jdata['language']
        self.manifests = MobileExportParser
        self.manifests_dir = self.manifests.manifests_dir
        # with open(os.path.join(self.manifests_dir, self.language, 'ExportRegions.json')) as regions:
        #     self.nodes = json.load(regions)['ExportRegions']
        with open(os.path.join(self.manifests_dir, self.language, 'ExportRelicArcane.json')) as arcane:
            self.arcanes = json.load(arcane)['ExportRelicArcane']
        with open(os.path.join(self.manifests_dir, self.language, 'ExportResources.json')) as resource:
            self.resources = json.load(resource)['ExportResources']
        with open(os.path.join(self.manifests_dir, self.language, 'ExportWeapons.json')) as weapon:
            self.weapons = json.load(weapon)['ExportWeapons']
        self.items = [self.arcanes, self.resources, self.weapons]

    def __get_timestamp(self, timestamp):
        return int(timestamp['$date']['$numberLong'])/1000
        # return timestamp in second. DE provided them as ms

    def __get_data(self):
        resp = requests.get(self.url)
        resp.raise_for_status()
        self.data = json.loads(resp.text)

    def __get_baro(self):
        if self.data == {}:
            self.__get_data()
        self.baro = self.data['VoidTraders'][0]
        node = self.baro['Node']
        # node_name = None
        # systemName = None
        arrive = self.__get_timestamp(self.baro['Activation'])
        expiry = self.__get_timestamp(self.baro['Expiry'])

    def __get_varzia(self):
        '''
        get offering list of PrimeVaultTraders
        '''
        if self.data == {}:
            self.__get_data()
        self.varzia = self.data['PrimeVaultTraders']
        for index in self.varzia:
            start = self.__get_timestamp(index['Activation'])
            end = self.__get_timestamp(index['Expiry'])
            items = index['Manifests']
            for item in items:
                game_ref = item['ItemType'].replace("/StoreItems/", "/")
                # RelicArcanes
                # Resources
                # Weapons
                # use `get` in case not exists in both three
