from fastapi import FastAPI, Request
from fastapi_utils.tasks import repeat_every
import time
import configparser
from src.components.luaparser.slmodStatsParser import getLuaDecoded_slmodStats
from src.components.data.SlmodStats.playerData import getPlayersList
from src.components.data.SlmodStats.playerData import getPlayerDataByUCID
from src.components.data.SlmodStats.playerData import getPlayerUCIDByName

from src.components.data.SlmodStats.Rankings.playerRankingByFlighTime import getPlayerRankingByFlightTime;

app = FastAPI()

luadecoded = getLuaDecoded_slmodStats(False)

@app.middleware("http")
async def getData(request: Request, call_next):
    config = configparser.ConfigParser()
    config.read('config.cfg')
    print("Refreshing...")
    start_time = time.time()
    global luadecoded
    response = await call_next(request)
    if config["configuration"]["enablerealtimeupdates"] == "True":
        response.headers["Realtimeupdates"] = "True"
        luadecoded = getLuaDecoded_slmodStats(True)
    else:
        response.headers["Realtimeupdates"] = "False"
        luadecoded = getLuaDecoded_slmodStats(False) 
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    print("Refreshed in "+str(process_time)+ " seconds")
    return response


@app.get("/")
async def root():
    return {"message": luadecoded}

@app.get("/players")
async def PlayersList():
    return {"players" : getPlayersList(luadecoded)}

@app.get("/playerbyucid/{UCID}")
async def PlayerDataByUCID(UCID):
    return { UCID : getPlayerDataByUCID(luadecoded, UCID)}

@app.get("/playerbyname/{name}")
async def PlayerDataByName(name):
    return {"UCID" : getPlayerUCIDByName(name, luadecoded)}

@app.get("/playerrankingbyflighttime")
async def PlayerRankingByFlightTime():
    return {"ranking" : getPlayerRankingByFlightTime(luadecoded, 10)}
