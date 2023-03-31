import cloudscraper
import os
import re
import requests
import subprocess
import shutil
import json
import time
import sys
import logging
from contextlib import contextmanager
from bs4 import BeautifulSoup as parser
from requests.exceptions import ConnectionError, ConnectTimeout
from cloudscraper.exceptions import CloudflareException, CaptchaException

BASE_PATH = "{}/GLR_Manager".format(os.getenv("LOCALAPPDATA"))
PROFILES_PATH = "{}/Profiles".format(BASE_PATH)
CURRENT_VERSION = "1.3.9"

class Game:
    def __init__(self, id, name, type):
        self.id = id.strip()
        self.name = name.strip()
        self.type = type.strip()

    def to_JSON(self):
        return {"id": self.id, "name": self.name, "type": self.type}

    def to_string(self):
        return "ID: {0}\nName: {1}\nType: {2}\n".format(self.id, self.name, self.type)

    def to_list(self):
        return [self.id, self.name, self.type]

    def __eq__(self, value):
        return self.id == value.id and self.name == value.name and self.type == value.type

    def __getitem__(self, index):
        values_list = list(vars(self).values())
        return values_list[index]

    @staticmethod
    def from_JSON(data):
        return Game(data["id"], data["name"], data["type"])

    @staticmethod
    def from_table_list(list):
        games = []
        for i in range(int(len(list) / 3)):
            games.append(Game(list[i * 3], list[i * 3 + 1], list[i * 3 + 2]))

        return games

class Profile:
    def __init__(self, name="default", games=[]):
        self.name = name
        self.games = games

    def add_game(self, game):
        self.games.append(game)

    def remove_game(self, game):
        if type(game) is Game:
            self.games.remove(game)
        else:
            for game_ in self.games:
                if game_.name == game:
                    self.games.remove(game_)

    def export_profile(self, path=PROFILES_PATH):
        data = {"name": self.name, "games": [game.to_JSON() for game in self.games]}
        with open("{}/{}.json".format(path, self.name), "w") as outfile:
            json.dump(data, outfile, indent=4)

    def __eq__(self, value):
        return self.name == value.name

    @staticmethod
    def from_JSON(data):
        return Profile(data["name"], [Game.from_JSON(game) for game in data["games"]])

class ProfileManager:
    def __init__(self):
        self.profiles = {}
        self.load_profiles()

    def load_profiles(self):
        if not os.path.exists(PROFILES_PATH):
            os.makedirs(PROFILES_PATH)
            self.create_profile("default")
        elif len(os.listdir(PROFILES_PATH)) == 0:
            self.create_profile("default")

        for filename in os.listdir(PROFILES_PATH):
            if os.path.splitext(filename)[1] == ".json":
                with open("{}/{}".format(PROFILES_PATH, filename), "r") as file:
                    try:
                        data = json.load(file)
                        self.register_profile(Profile.from_JSON(data))
                    except (UnicodeDecodeError, json.JSONDecodeError) as e:
                        logging.exception(e)

    def register_profile(self, profile):
        self.profiles[profile.name] = profile

    def create_profile(self, name, games=[]):
        if name == "":
            return

        self.register_profile(Profile(name, games))
        self.profiles[name].export_profile(PROFILES_PATH)

    def remove_profile(self, profile_name):
        self.profiles.pop(profile_name)
        os.remove("{}/{}.json".format(PROFILES_PATH, profile_name))

class Config:
    def __init__(self, steam_path="", greenluma_path="", no_hook=True, compatibility_mode=True, version=CURRENT_VERSION, last_profile="default", check_update=True, use_steamdb=False, manager_msg=False):
        self.steam_path = steam_path
        self.greenluma_path = greenluma_path
        self.no_hook = no_hook
        self.compatibility_mode = compatibility_mode
        self.version = version
        self.last_profile = last_profile
        self.check_update = check_update
        self.use_steamdb = use_steamdb
        self.manager_msg = manager_msg

    def export_config(self):
        with open("{}/config.json".format(BASE_PATH), "w") as outfile:
            json.dump(vars(self), outfile, indent=4)

    @staticmethod
    def from_JSON(data):
        config = Config()
        for key, value in data.items():
            if key in vars(config).keys():
                setattr(config, key, value)

        if not "greenluma_path" in data and "steam_path" in data:
            if os.path.isfile(os.path.join(config.steam_path, "DLLInjector.exe")):
                config.greenluma_path = config.steam_path
        return config

    @staticmethod
    def load_config():
        if not os.path.isfile("{}/config.json".format(BASE_PATH)):
            if not os.path.exists(BASE_PATH):
                os.makedirs(BASE_PATH)

            config = Config()
            config.export_config()
            return config
        else:
            with open("{}/config.json".format(BASE_PATH), "r") as file_:
                try:
                    data = json.load(file_)
                    config = Config.from_JSON(data)
                except Exception as e:
                    logging.exception(e)
                    config = Config()

                config.version = CURRENT_VERSION
                config.export_config()
                return config

class ConfigNotLoadedException(Exception):
    pass

#-------------
logging.basicConfig(filename="errors.log", filemode="w", level=logging.DEBUG)
logging.info("GreenLuma 2023 Manager " + CURRENT_VERSION)
config = Config.load_config()
query_filter = re.compile("[ \u00a9\u00ae\u2122]")

@contextmanager
def get_config():
    global config
    try:
        if config:
            yield config
        else:
            config = Config.load_config()
    finally:
        config.export_config()

def createFiles(games):
    if not os.path.exists("{}/AppList".format(config.greenluma_path)):
        os.makedirs("{}/AppList".format(config.greenluma_path))
    else:
        shutil.rmtree("{}/AppList".format(config.greenluma_path))
        time.sleep(0.5)
        os.makedirs("{}/AppList".format(config.greenluma_path))

    for i in range(len(games)):
        with open("{}/AppList/{}.txt".format(config.greenluma_path, i), "w") as file:
            file.write(games[i].id)

def parseSteamDB(html):
    p = parser(html, "html.parser")

    rows = p.find_all("tr", class_="app")

    games = []
    for row in rows:
        data = row("td")
        if data[1].get_text() != "Unknown":
            game = Game(data[0].get_text(), data[2].get_text(), data[1].get_text())
            games.append(game)

    return games

def parseDlcs(html):
    p = parser(html, "html.parser")

    dlcs = p.find_all("div", class_="recommendation")

    games = []
    for dlc in dlcs:
        appid = dlc.find("a")["data-ds-appid"]
        name = dlc.find("span", class_="color_created").get_text()
        games.append(Game(appid, name, "DLC"))

    return games

def getDlcs(storeUrl):
    if "app/" not in storeUrl:
        # edge case: 'https://store.steampowered.com/sub/516201/?snr=1_7_7_151_150_1'
        return []
    appinfo = storeUrl.split("app/")[1].split("/")
    appid = appinfo[0]
    sanitazedName = appinfo[1]

    params = {"sort": "newreleases", "count": 64, "start": 0}
    baseUrl = "https://store.steampowered.com/dlc/{0}/{1}/ajaxgetfilteredrecommendations"
    response = requests.get(baseUrl.format(appid, sanitazedName), params=params).json()
    return parseDlcs(response["results_html"])

def parseGames(html, query):
    query = query_filter.sub("", query.lower())
    p = parser(html, "html.parser")

    results = p.find_all("a", class_="search_result_row")

    games = []
    for result in results:
        if result.has_attr("data-ds-appid"):
            appid = result["data-ds-appid"]
            name = result.find("span", class_="title").get_text()
            # Filter out garbage
            if "," not in appid and query in query_filter.sub("", name.lower()):
                games.append(Game(appid, name, "Game"))
                games.extend(getDlcs(result["href"]))

    return games

def queryfy(input_):
    arr = input_.split()
    result = arr.pop(0)
    for word in arr:
        result = result + "+" + word
    print(result)
    return result

def queryGames(query):
    try:
        if config.use_steamdb and False:
            scraper = cloudscraper.create_scraper()
            params = {"a": "app", "q": query, "type": -1, "category": 0}
            response = scraper.get("https://steamdb.info/search/", params=params)
            return parseSteamDB(response.content)
        else:
            params = {"term": query, "count": 25, "start": 0, "category1": 998}
            response = requests.get("https://store.steampowered.com/search/results", params=params)
            return parseGames(response.content, query)
    except (ConnectionError, ConnectTimeout, CloudflareException, CaptchaException) as err:
        logging.exception(err)
        return err

def runUpdater():
    if "-NoUpdate" not in sys.argv and config.check_update and os.path.exists("GL2020 Updater.exe"):
        try:
            subprocess.run("GL2020 Updater.exe")
        except OSError as err:
            logging.error("Error while checking for updates")
            logging.exception(err)

    # Post update measure
    if "-PostUpdate" in sys.argv:
        for fl in os.listdir("./"):
            if fl.startswith("new_"):
                real_name = fl.replace("new_", "")
                os.remove(real_name)
                os.rename(fl, real_name)
