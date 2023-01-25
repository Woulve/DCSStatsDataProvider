import configparser
from src.util.serverlogger import serverLogger

import pathlib


LOGGER = serverLogger()

def getConfigValue(category: str, value: str):
    config = configparser.ConfigParser()
    config.read('config.cfg')
    # if config[category][value] == None:
    #     LOGGER.error("Couldn't read config value: "+category+" "+value)
    #     return None
    return config[category][value]

def getAllConfigValues(section: str):
    parsed = {}
    config = configparser.ConfigParser()
    config.read('config.cfg')
    for each_section in config.sections():
        parsed[each_section] = {}
        for (each_key, each_val) in config.items(each_section):
            parsed[each_section][each_key] = each_val
    return parsed