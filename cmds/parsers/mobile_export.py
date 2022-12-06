import json
import logging
import os
import re
from pprint import pprint

import requests
from const import AVAILABLE_LANGUAGES

dirname = os.path.dirname(__file__)
logger = logging.getLogger('mobileExportParser')
logger.setLevel(-1)
handler = logging.FileHandler(filename=os.path.join(dirname, '../../log/runtime.log'), encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(lineno)d: %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
logger.addHandler(handler)


glyphs = [
    '<DT_GAS>',
    '<DT_VIRAL>',
    '<DT_CORROSIVE>',
    '<DT_MAGNETIC>',
    '<DT_IMPACT>',
    '<DT_FIRE>',
    '<DT_COLD>',
    '<DT_ELECTRICITY>',
    '<DT_EXPLOSION>',
    '<DT_RADIATION>',
    '<DT_POISON>',
    '<ARCHWING>',
    '<DT_PUNCTURE>',
    '<DT_FREEZE>',
    '<DT_SLASH>',
    '<DT_SENTIENT>',
    '<SHIELD>',
    '<CREDITS>',
    '<SHARD_RED_SIMPLE>',
    '<SHARD_BLUE_SIMPLE>',
    '<SHARD_YELLOW_SIMPLE>',
    '<REPUTATION_SMALL>',
    '<ARCHWING>',
    '|val|%',
    '|val|s',
    '|STAT1|%',
    '|val|',
    '|BONUS|'
]

doublespace_remover = re.compile(r'\s{2,}')

factions = {
    0: 'Grineer',
    1: 'Corpus',
    2: 'Infested',
    3: 'Corrupted'
}

mission = {
    0: 'Assassination',
    1: 'Exterminate',
    2: 'Survival',
    3: 'Rescue',
    4: 'Sabotage',
    5: 'Capture',
    7: 'Spy',
    8: 'Defense',
    9: 'Mobile Defense',
    13: 'Interception',
    14: 'Hijack',
    15: 'Hive Sabotage',
    17: 'Excavation',
    21: 'Infested Salvage',
    22: 'Rathuum',
    24: 'Pursuit',
    25: 'Rush',
    26: 'Assault',
    27: 'Defection',
    28: 'Landscape',
    32: 'Disruption',
    33: 'Void Flood',
    34: 'Void Cascade',
    35: 'Void Armageddon'
}


class MobileExportParser():
    manifests_dir = os.path.join(dirname, "../../manifests")

    def __init__(self):
        self.index_url = "https://origin.warframe.com/PublicExport/index_{language_code}.txt.lzma"
        self.manifest_url = "http://content.warframe.com/PublicExport/Manifest/{file_name}"
        if os.path.exists(os.path.join(self.manifests_dir, 'items.json')) and os.path.exists(os.path.join(self.manifests_dir, 'nodes.json')):
            logger.debug('[init] local manifests found, loading into RAM')
            with open(os.path.join(self.manifests_dir, 'items.json'), 'r', encoding='utf-8') as _manifests:
                self.manifest_data = json.load(_manifests)
            with open(os.path.join(self.manifests_dir, 'nodes.json'), 'r', encoding='utf-8') as _nodes:
                self.nodes = json.load(_nodes)
        else:
            logger.debug('[init] local manifests not found, start to update manifests')
            self.update()

    def download_manifests(self, language):
        if language == "zh-hant":
            resp_lang = 'tc'
        elif language == "zh-hans":
            resp_lang = 'zh'
        else:
            resp_lang = language
        if not os.path.exists(os.path.join(self.manifests_dir, language)):
            logger.debug(f'[download_manifests] manifests_languagr_dir not exists, creating {language}')
            os.makedirs(os.path.join(self.manifests_dir, language))
        resp = requests.get(self.index_url.format(language_code=resp_lang))
        with open(os.path.join(self.manifests_dir, language, 'index.txt.lzma'), 'wb') as out:
            out.write(resp.content)
        command = f"7z x -y {os.path.join(self.manifests_dir, language, 'index.txt.lzma')} -o{os.path.join(self.manifests_dir, language)}"
        os.system(command)
        with open(os.path.join(self.manifests_dir, language, 'index.txt')) as index:
            for file in index.readlines():
                logger.debug(f'[download_manifests] downloading {language}/{file.strip()}')
                print(f"\033[92mDownloading file\033[0m:{file.strip()}")
                resp = requests.get(self.manifest_url.format(file_name=file).replace('\n', ''))
                file = file.split("!")[0].replace(f"_{resp_lang}", "")
                with open(os.path.join(self.manifests_dir, language, file), "wb") as out:
                    for chunk in resp:
                        out.write(chunk)
        for file in os.listdir(os.path.join(self.manifests_dir, language)):
            if 'index.txt' in file:
                continue
            logger.debug(f'[download_manifests] fixing {language}/{file}')
            print(f"\033[92mFixing file\033[0m: {file}")
            with open(os.path.join(self.manifests_dir, language, file), 'r', encoding="utf-8") as f:
                text = f.read()
                text = text.replace('\n', '').replace('\r', '')
                _json = json.loads(text)
                with open(os.path.join(self.manifests_dir, language, file), 'w', encoding='utf-8') as _file:
                    _file.write(json.dumps(_json, ensure_ascii=False, indent=4))

    def update(self):
        for language in AVAILABLE_LANGUAGES:
            self.download_manifests(language)
        self.manifest_data = {}
        self.nodes = {}
        categories = ['ExportRelicArcane', 'ExportResources', 'ExportWeapons', 'ExportWarframes']
        for language in AVAILABLE_LANGUAGES:
            _items = []
            _locations = []
            logger.debug(f'[update] Updating {language} manifests data')
            dir_language_manifests = os.path.join(self.manifests_dir, language)

            # Concat the manifests into one
            for manifest in os.listdir(dir_language_manifests):
                if not manifest.endswith('.json'):
                    continue
                with open(os.path.join(dir_language_manifests, manifest), 'r', encoding='utf-8') as _file:
                    _json = json.load(_file)
                    for _cat, data in _json.items():
                        if _cat == 'ExportRegions':
                            _locations += data
                        if _cat not in categories:
                            continue
                        _items += data

            for item in _items:
                if 'name' not in item or 'uniqueName' not in item:
                    continue
                # do sth to add into memory storage then dump
                self.__add_item(language, item)

            for location in _locations:
                if 'name' not in location or 'uniqueName' not in location:
                    continue
                self.__add_node(language, location)
        print()
        print('Finished Update')

        with open(os.path.join(self.manifests_dir, 'items.json'), 'w', encoding='utf-8') as _file:
            _file.write(json.JSONEncoder(indent=4, ensure_ascii=False).encode(self.manifest_data))
        with open(os.path.join(self.manifests_dir, 'nodes.json'), 'w', encoding='utf-8') as _file:
            _file.write(json.JSONEncoder(indent=4, ensure_ascii=False).encode(self.nodes))
        logger.debug('[update] Dumped manifests data')

    def __add_item(self, lang, item):
        """
        lang (string): language
        item (dict): raw item record
        """

        uniq_name = item['uniqueName']

        name = self.clear_text_from_manifest(item['name'])
        description = item['description'] if 'description' in item else ''
        description = self.clear_text_from_manifest(description)

        if uniq_name not in self.manifest_data:
            self.manifest_data[uniq_name] = {}

        item = self.manifest_data[uniq_name]

        # Set locale values
        item[lang] = {
            'item_name': name,
            'description': description
        }

        # check if all lang fields were defined
        for _lang in AVAILABLE_LANGUAGES:
            if _lang not in item:
                return

        print('', end='\x1b[2K\r')
        print(f"\033[92madded item\033[0m: {item['en']['item_name']}", end='\r', flush=True)

    def __add_node(self, lang, node):
        """
        lang (string): language
        node (dict): raw node data
        """

        uniq_name = node['uniqueName']

        name = self.clear_text_from_manifest(node['name'])
        system = self.clear_text_from_manifest(node['systemName'])

        if uniq_name not in self.nodes:
            self.nodes[uniq_name] = {
                'faction': factions.get(node.get('factionIndex')),
                'mission': mission.get(node.get('missionIndex')),
                'minEnemyLevel': node.get('minEnemyLevel'),
                'maxEnemyLevel': node.get('maxEnemyLevel')
            }

        node = self.nodes[uniq_name]

        # Set locale values
        node[lang] = {
            'name': name,
            'system': system
        }

        # check if all lang fields were defined
        for _lang in AVAILABLE_LANGUAGES:
            if _lang not in node:
                return

        print('', end='\x1b[2K\r')
        print(f"\033[92madded item\033[0m: {node['en']['name']}", end='\r', flush=True)

    def clear_text_from_manifest(self, name):
        """
        Remove special glyphs that used in manifests
        """
        for _cut in glyphs:
            if _cut in name:
                name = name.replace(_cut, '')
        name = doublespace_remover.sub(' ', name.replace('\r\n', '\n').replace('\r\r', '\n').replace('\r', '\n').strip())
        return name


if __name__ == '__main__':
    Parser = MobileExportParser()
    Parser.update()
    pprint(Parser.manifest_data[list(Parser.manifest_data)[0]])
