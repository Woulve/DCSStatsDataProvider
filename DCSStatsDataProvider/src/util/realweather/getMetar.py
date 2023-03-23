from src.util.serverlogger import serverLogger

LOGGER = serverLogger()


def getMetar ():
    try:
        with open("./src/util/realweather/current_metar.txt", "r") as metarfile:
            metar = metarfile.read()
            return metar
    except Exception as e:
        LOGGER.info("No metar file found.")
        return False