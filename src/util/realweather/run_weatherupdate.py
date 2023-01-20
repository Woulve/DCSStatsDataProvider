import os
import json
import subprocess
from src.util.getConfigValue import getConfigValue
from src.util.serverlogger import serverLogger
from datetime import datetime, timedelta

LOGGER = serverLogger()

#This file can provide real time weather, by using "evogelsa's" real weather updater. It is not included in the default package, but can be downloaded from https://github.com/evogelsa/DCS-real-weather
#Put the realweather.exe in this folder, and set enableweatherchanges to True in the config.ini file, to get real time weather updates (every 10 minutes by default, as set in main.py)

#The file checks if the weather has been updated in the last 12 hours. If not, it will update the weather.
#The realweather.exe looks in the "Active" folder, for a mission named "active_mission.miz". It will then update the weather in that mission, and save it as "realweather.miz" in the same folder.
#The log of realweather.exe is saved in this folder, as "logfile.log"

def over_12_hours(date1, date2):
    try:
        date1 = datetime.strptime(date1, "%d/%m/%Y %H:%M:%S")
        date2 = datetime.strptime(date2, "%d/%m/%Y %H:%M:%S")
        difference = date2 - date1
        return difference > timedelta(hours=12)
    except ValueError:
        # handle error if date strings are in an incorrect format
        LOGGER.error("Error: Incorrect date format.")

def check_if_weather_update_is_needed():
    #Switch to current directory to run realweather.exe
    try:
        with open("weather_last_time_updated.txt", "r") as datefile:
            last_time_updated = datefile.read()
            if over_12_hours(last_time_updated, datetime.now().strftime("%d/%m/%Y %H:%M:%S")):
                LOGGER.info("Weather update needed.")
                print("Weather update needed.")
                return True
            else:
                LOGGER.info("Weather update not needed.")
                return False
    except:
        LOGGER.info("Weather update needed.")
        return True

def update_miz_weather():

    values = {
        "api-key" : os.getenv("CHECKWX_APIKEY"),
        "icao" : getConfigValue("icao"),
        "hour-offset": 0,
        "input-mission-file": "Active/active_mission.miz",
        "output-mission-file": "Active/realweather.miz",
        "update-time" : getConfigValue("update-time"),
        "update-time" : False,
        "update-weather": True,
        "logfile": "logfile.log",
        "metar-remarks": ""
    }

    activepath = os.path.abspath(os.path.dirname(__file__))
    os.chdir(activepath)

    if (check_if_weather_update_is_needed() == False):
        return False

    #Write values to config.json and run realweather.exe
    try:
        json_object = json.dumps(values, indent=4)

        with open("config.json", "w+") as outfile:
            outfile.write(json_object)
        result = subprocess.run([activepath+"/realweather.exe"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode()


        with open("weather_last_time_updated.txt", "w+") as datefile:
            datefile.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        return True
    except:
        # handle other possible errors
        LOGGER.error("Error: An error occurred while updating weather.")