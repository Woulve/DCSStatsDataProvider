import configparser
from src.util.serverlogger import serverLogger
from fastapi import HTTPException

LOGGER = serverLogger()

def getConfigValue(category: str, value: str):
    config = configparser.ConfigParser()
    try:
        config.read('config.cfg')
    except Exception as e:
        LOGGER.error("Couldn't read config file")
        LOGGER.exception(e)
    try:
        val = config[category][value]
        return val
    except Exception as e:
        LOGGER.error("Config file doesn't contain: "+ category + " " + value)
        LOGGER.exception(e)
        raise HTTPException(status_code=500)

def getAllConfigValues(section: str):
    parsed = {}
    config = configparser.ConfigParser()
    try:
        config.read('config.cfg')
    except Exception as e:
        LOGGER.error("Couldn't read config file")
        LOGGER.exception(e)
    try:
        for each_section in config.sections():
            parsed[each_section] = {}
            for (each_key, each_val) in config.items(each_section):
                parsed[each_section][each_key] = each_val
    except Exception as e:
        LOGGER.error("Error getting Config file sections")
        LOGGER.exception(e)
        raise HTTPException(status_code=500)
    return parsed