import configparser

def getConfigValue(value: str):
    config = configparser.ConfigParser()
    config.read('config.cfg')
    return config["configuration"][value]

def getAllCongigValues(section: str):
    config = configparser.ConfigParser()
    config.read('config.cfg')
    return dict(config.items(section))