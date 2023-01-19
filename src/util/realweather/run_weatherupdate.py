import os
import json
from src.util.getConfigValue import getConfigValue
from src.util.serverlogger import serverLogger
LOGGER = serverLogger()
from datetime import datetime, timedelta

#This file can provide real time weather, by using "evogelsa's" real weather updater. It is not included in the default package, but can be downloaded from https://github.com/evogelsa/DCS-real-weather
#Put the realweather.exe in this folder, and set enableweatherchanges to True in the config.ini file, to get real time weather updates (every 10 minutes by default, as set in main.py)


def over_12_hours(date1, date2):
    try:
        date1 = datetime.strptime(date1, "%d/%m/%Y %H:%M:%S")
        date2 = datetime.strptime(date2, "%d/%m/%Y %H:%M:%S")
        difference = date2 - date1
        return difference > timedelta(hours=12)
    except ValueError:
        # handle error if date strings are in an incorrect format
        LOGGER.error("Error: Incorrect date format.")

def update_miz_weather():

    values = {
        "api-key" : os.getenv("CHECKWX_APIKEY"),
        "icao" : getConfigValue("icao"),
        "hour-offset": 0,
        "input-mission-file": "active_mission.miz",
        "output-mission-file": "realweather.miz",
        "update-time" : getConfigValue("update-time"),
        "update-time" : False,
        "update-weather": True,
        "logfile": "logfile.log",
        "metar-remarks": ""
    }

    mypath = os.path.abspath(os.path.dirname(__file__))
    os.chdir(mypath)

    exit = 0
    if (os.path.isfile("weather_last_time_updated.txt")):
        try:
            with open("weather_last_time_updated.txt", "r+") as datefile:
                last_time_updated = datefile.read()
                if over_12_hours(last_time_updated, datetime.now().strftime("%d/%m/%Y %H:%M:%S")):
                    LOGGER.info("Updating weather")
                else:
                    exit = 1
        except FileNotFoundError:
            # handle error if weather_last_time_updated.txt doesn't exist
            LOGGER.error("Error: weather_last_time_updated.txt not found.")

    if exit == 1:
        return

    try:
        json_object = json.dumps(values, indent=4)

        with open("config.json", "w+") as outfile:
            outfile.write(json_object)

        os.system(f'"{mypath}/realweather.exe"')

        with open("weather_last_time_updated.txt", "w+") as datefile:
            datefile.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    except:
        # handle other possible errors
        LOGGER.error("Error: An error occurred while updating weather.")