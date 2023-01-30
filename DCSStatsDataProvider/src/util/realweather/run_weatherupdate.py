import os
import json
from subprocess import PIPE, run
from src.util.getConfigValue import getConfigValue
from src.util.serverlogger import serverLogger
from datetime import datetime, timedelta
import pathlib

LOGGER = serverLogger()

#This file can provide real time weather, by using "evogelsa's" real weather updater. It is not included in the default package, but can be downloaded from https://github.com/evogelsa/DCS-real-weather
#Put the realweather.exe in this folder, and set enableweatherchanges to True in the config.ini file, to get real time weather updates (every 10 minutes by default, as set in main.py)

#The file checks if the weather has been updated in the last 24 hours. If not, it will update the weather.
#The realweather.exe looks in the "Active" folder, for a mission named "mission.miz". It will then update the weather in that mission, and save it as "foothold_remastered_realweather" in the same folder.
#The log of realweather.exe is saved in this folder, as "logfile.log"

def over_24_hours(date1, date2):
    try:
        date1 = datetime.strptime(date1, "%Y/%m/%d %H:%M:%S")
        date2 = datetime.strptime(date2, "%Y/%m/%d %H:%M:%S")
        difference = date2 - date1
        return difference > timedelta(hours=24)
    except ValueError:
        # handle error if date strings are in an incorrect format
        LOGGER.error("Error: Incorrect date format.")

def check_if_weather_update_is_needed():

    try:
        with open("weather_last_time_updated.txt", "r") as datefile:
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
    #If you want to use real weather, you need to set the CHECKWX_APIKEY environment variables in a .env file in the root folder.
    values = {
        "api-key" : os.getenv("CHECKWX_APIKEY"),
        "icao" : getConfigValue("realweather", "icao"),
        "hour-offset": 0,
        "input-mission-file": "Active/mission.miz",
        "output-mission-file": "Active/foothold_remastered_realweather.miz",
        "update-time" : False,
        "update-weather": True,
        "logfile": "logfile.log",
        "metar-remarks": ""
    }

    weatherpath = os.path.abspath(os.path.dirname(__file__))
    os.chdir(weatherpath)

    if (check_if_weather_update_is_needed() == False):
        return False


    #Write values to config.json and run realweather
    try:
        json_object = json.dumps(values, indent=4)

        try:
            with open("config.json", "w+") as outfile:
                outfile.write(json_object)
        except Exception as e:
            LOGGER.error("Error: An error occurred while writing to config.json.")
            return

        command = [weatherpath+"/DCS-real-weather"]
        result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)

        if "Removed mission_unpacked" in result.stdout:
            with open("weather_last_time_updated.txt", "w+") as datefile:
                datefile.write(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
                LOGGER.info("Weather successfully updated. (Found \"Removed mission_unpacked\" in the DCS-real-weather output)")
            return True
        else:
            LOGGER.error("Error: realweather output didn't contain \"Removed mission_unpacked\". DCS-real-weather output: " + result.stderr)
            return False
    except Exception as e:
        # handle other possible errors
        LOGGER.error("Error: An error occurred while updating weather.")