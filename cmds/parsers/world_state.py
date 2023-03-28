import json
import logging
import os
from datetime import datetime, timedelta, timezone
from pprint import pprint

import requests
from pytz import utc

from cmds.parsers.mobile_export import MobileExportParser

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
        items = {}
        for item in self.baro.get('Manifest', {}):
            _item = self.manifests.manifest_data.get(item['ItemType'], item['ItemType'])
            items[_item] = {
                'PrimePrice': item.get('PrimePrice', 0),
                'RegularPrice': item.get('RegularPrice', 0)
            }
        print(self.baro)
        return arrive, expiry, node_name, system, items

    def __get_varzia(self):
        '''
        get offering list of PrimeVaultTraders
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
        boss = self.manifests.sortie[self.language]['bosses'][boss]['name']
        missions = self.sortie['Variants']
        for mission in missions:
            mission['node'] = self.manifests.nodes[mission['node']]
            mission['node'] = mission['node'][self.language]['name']+'('+mission['node'][self.language]['system']+')'
            mission['modifierType'] = self.manifests.sortie[self.language]['modifierTypes'][mission['modifierType']]
            mission['missionType'] = self.manifests.mission[self.language][mission['missionType']]['value']
        return start, end, boss, missions

    def get_archon(self):
        if self.data == {}:
            self.__get_data()
        self.archon = self.data['LiteSorties'][0]
        start = self.__get_timestamp(self.archon['Activation'])
        end = self.__get_timestamp(self.archon['Expiry'])
        boss = self.archon['Boss']
        boss = self.manifests.sortie[self.language]['bosses'][boss]['name']
        missions = self.archon['Missions']
        for mission in missions:
            mission['node'] = self.manifests.nodes[mission['node']]
            mission['node'] = mission['node'][self.language]['name']+'('+mission['node'][self.language]['system']+')'
            mission['missionType'] = self.manifests.mission[self.language][mission['missionType']]['value']
        return start, end, boss, missions

    def get_fissure(self):
        self.__get_data()
        # always ask for new data cuz fissures are dynamically updated
        self.fissure = self.data['ActiveMissions']
        for mission in self.fissure:
            mission['Activation'] = self.__get_timestamp(mission['Activation'])
            mission['Expiry'] = self.__get_timestamp(mission['Expiry'])
            mission['Node'] = self.manifests.nodes[mission['Node']]
            mission['Node'] = mission['Node'][self.language]['name']+'('+mission['Node'][self.language]['system']+')'
            mission['MissionType'] = self.manifests.mission[self.language][mission['MissionType']]['value']
            mission['Tier'] = self.manifests.fissuremod[self.language][mission['Modifier']]['value']
            del mission['_id']
            del mission['Region']
            del mission['Seed']
            print(mission)
        return self.fissure

    def get_voidstorms(self):
        self.__get_data()
        # always ask for new data cuz voidstorms are dynamically updated
        self.voidstorm = self.data['VoidStorms']
        for mission in self.voidstorm:
            mission['Activation'] = self.__get_timestamp(mission['Activation'])
            mission['Expiry'] = self.__get_timestamp(mission['Expiry'])
            mission['Node'] = self.manifests.nodes[mission['Node']]
            mission['Node'] = mission['Node'][self.language]['name']+'('+mission['Node'][self.language]['system']+')'
            mission['MissionType'] = self.manifests.mission[self.language][mission['MissionType']]['value']
            mission['Tier'] = self.manifests.fissuremod[self.language][mission['Modifier']]['value']
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

    def get_arbitration(self):
        raw = requests.get("https://api.warframestat.us/pc/tc/arbitration", headers={'Accept-Language': 'zh'})
        text = raw.text
        return json.loads(text)

    def __get_openworld_state(self, start_time: datetime, loop_time: timedelta, delay_time: timedelta, state_a: str, state_b: str):
        current_time = datetime.utcnow()
        time_elapsed = current_time - start_time
        loop_left = loop_time - time_elapsed % loop_time
        if loop_left > delay_time:
            # print(F"距離晚上還要{loop_left - delay_time}")
            endtime = current_time + (loop_left - delay_time)
            endtime = endtime.replace(tzinfo=timezone.utc).astimezone(tz=None).replace(tzinfo=None)
            return state_a, endtime
        else:
            # print(F"距離早上還要{loop_left}")
            endtime = current_time + (loop_left)
            endtime = endtime.replace(tzinfo=timezone.utc).astimezone(tz=None).replace(tzinfo=None)
            return state_b, endtime

    def get_poe_state(self):
        return self.__get_openworld_state(datetime(2021, 2, 5, 12, 27, 54, 00),
                                          timedelta(seconds=8998.874), timedelta(seconds=3000), 'day', 'night')

    def get_earth_state(self):
        return self.__get_openworld_state(datetime(2015, 12, 3, 00, 00, 00, 00),
                                          timedelta(seconds=28800), timedelta(seconds=14400), 'day', 'night')

    def get_orb_state(self):
        return self.__get_openworld_state(datetime(2021, 1, 9, 8, 13, 48, 00),
                                          timedelta(seconds=1600), timedelta(seconds=1200), 'warm', 'cold')

    def get_cambion_state(self):
        return self.__get_openworld_state(datetime(2021, 2, 5, 12, 27, 54, 00),
                                          timedelta(seconds=8998.874), timedelta(seconds=3000), 'fass', 'vome')


if __name__ == '__main__':
    parser = WorldStateParser()
    parser.manifests.update()
    pprint(parser.get_nightwave())