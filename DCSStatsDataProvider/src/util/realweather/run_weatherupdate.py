import os
import json
from subprocess import PIPE, run
from src.util.getConfigValue import getConfigValue
from src.util.serverlogger import serverLogger
from datetime import datetime, timedelta
from src.util.webDAV import getFileFromWebDAV, pushFileToWebdav
import pathlib
import platform

LOGGER = serverLogger()

#This file can provide real time weather, by using a modified fork "evogelsa's" real weather updater https://github.com/evogelsa/DCS-real-weather.
#Set enableweatherchanges to True in the config.ini file, to get real time weather updates (the interval is set in main.py)

#The file checks if the weather has been updated in the last 24 hours. If not, it will update the weather.
#The realweather tool looks in the folder specified in the config file under "localinputmissionlocation", for a mission named "mission.miz".
# It will then update the weather in that mission, and save it in the folder specified with "localoutputmissionlocation".

def over_24_hours(date1, date2):
    try:
        date1 = datetime.strptime(date1, "%Y/%m/%d %H:%M:%S")
        date2 = datetime.strptime(date2, "%Y/%m/%d %H:%M:%S")
        difference = date2 - date1
        return difference > timedelta(hours=24)
    except ValueError:
        LOGGER.error("Error: Incorrect date format.")

def check_if_weather_update_is_needed():

    try:
        with open("./src/util/realweather/weather_last_time_updated.txt", "r") as datefile:
            last_time_updated = datefile.read()
            if over_24_hours(last_time_updated, datetime.now().strftime("%Y/%m/%d %H:%M:%S")):
                LOGGER.info("Weather update needed, over 24 hours since last update.")
                return True
            else:
                LOGGER.info("Weather update not needed, less than 24 hours since last update.")
                return False
    except Exception as e:
        LOGGER.info("Weather update needed, no weather_last_time_updated.txt file found.")
        return True

def update_miz_weather():

    #If you want to use real weather, you need to set the CHECKWX_APIKEY environment variable.
    values = {
        "api-key" : os.getenv("CHECKWX_APIKEY"),
        "icao" : getConfigValue("realweather", "icao"),
        "hour-offset": 0,
        "input-mission-file": getConfigValue("localfiles", "localinputmissionlocation"),
        "output-mission-file": getConfigValue("localfiles", "localoutputmissionlocation"),
        "update-weather": True,
        "logfile": "./src/util/realweather/weather.log",
        "metar-remarks": ""
    }


    if (check_if_weather_update_is_needed() == False):
        return False

    if getConfigValue("realweather", "webdavmission") == "True" and getConfigValue("webdav", "enablewebdav") == "True":
        LOGGER.info("Fetching mission.miz from WEBDAV server.")
        if (getFileFromWebDAV(getConfigValue("webdav", "remoteinputmissionlocation"), getConfigValue("localfiles", "localinputmissionlocation"))) == 0:
            LOGGER.error("Couldn't fetch mission.miz from WEBDav server.")
            return

    #Write values to config.json and run realweather
    try:
        json_object = json.dumps(values, indent=4)

        try:
            with open("./src/util/realweather/config.json", "w+") as outfile:
                outfile.write(json_object)
        except Exception as e:
            LOGGER.error("Error: An error occurred while writing to config.json.")
            LOGGER.exception(e)
            return

        system, node, release, version, machine, processor = platform.uname()

        if machine == "aarch64":
            LOGGER.info("Running realweather for arm64")
            command = ["./src/util/realweather/realweather_arm64", "./src/util/realweather/"]
        elif machine == "x86_64" and system == "Linux":
            LOGGER.info("Running realweather for amd64")
            command = ["./src/util/realweather/realweather_amd64", "./src/util/realweather/"]
        elif machine == "AMD64" and system == "Windows":
            LOGGER.info("Running realweather for Windows")
            command = ["./src/util/realweather/realweather.exe", "./src/util/realweather/"]
        else:
            LOGGER.error("Error: Unsupported Architecture: "+machine + " " + system)
            return False

        result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)

        if "Removed mission_unpacked" in result.stdout:
            with open("./src/util/realweather/weather_last_time_updated.txt", "w+") as datefile:
                datefile.write(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
                LOGGER.info("Weather successfully updated. (Found \"Removed mission_unpacked\" in the realweather output)")

                if getConfigValue("realweather", "webdavmission") == "True" and getConfigValue("webdav", "enablewebdav") == "True":
                    if (pushFileToWebdav(getConfigValue("webdav", "remoteoutputmissionlocation"), getConfigValue("localfiles", "localoutputmissionlocation"))) == 0:
                        LOGGER.error("Couldn't push foothold_remastered_realweather.miz to WEBDav server.")
                        return False
            return True
        else:
            LOGGER.error("Error: realweather output didn't contain \"Removed mission_unpacked\". realweather output: " + result.stderr)
            return False
    except Exception as e:
        # handle other possible errors
        LOGGER.error("Error: An error occurred while updating weather.")
        LOGGER.exception(e)