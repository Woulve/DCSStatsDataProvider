import time
import uvicorn
import os

from fastapi import FastAPI, Path, Request, HTTPException, Response, Header
from fastapi.responses import JSONResponse
from fastapi_utils.tasks import repeat_every
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi_cache import FastAPICache
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from datetime import date
# from dotenv import load_dotenv
import base64

from src.util.webDAV import getFileFromWebDAV, pushFileToWebdav
from src.util.serverlogger import serverLogger
from src.util.getConfigValue import getConfigValue, getAllConfigValues
from src.components.luaparser.slmodstats.slmodStatsParser import getLuaDecoded_slmodStats
from src.components.data.SlmodStats.playerData import getPlayersList
from src.components.data.SlmodStats.playerStats import getPlayerStats
from src.components.data.SlmodStats.playerData import getPlayerUCIDByName
from src.components.data.SlmodStats.allPlayerStats import getAllPlayerStats
from src.components.data.SlmodStats.playerAirplaneList import getPlayerAirplaneList
from src.components.data.SlmodStats.playerAirplaneStats import getPlayerAirplaneStats
from src.util.realweather.run_weatherupdate import update_miz_weather
from src.util.realweather.getMetar import getMetar
from src.components.data.SlmodStats.Rankings.playerRankingByFlightTime import getPlayerRankingByFlightTime;
from src.components.data.SlmodStats.Rankings.playerRankingByPoints import getPlayerRankingByPoints;

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


LOGGER = serverLogger()
# load_dotenv()

origins = [
    "http://localhost:3000",
    os.getenv("ALLOWED_ORIGIN")
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class slmodstatslua():
    luadecoded = {}
    def setLuaDecoded(self, file):
        LOGGER.debug("decoding "+file)
        if file == "SlmodStats":
            path = getConfigValue("localfiles", "slmodstatsluapath")
        elif file == "SlmodStatsDebugging":
            path = getConfigValue("localfiles", "slmodstatsdebuggingluapath")
        enablerealtimeupdates = True if getConfigValue("configuration", "enablerealtimeupdates") == "True" else False
        self.luadecoded[file] = getLuaDecoded_slmodStats(path, enablerealtimeupdates)

    def getLuaDecoded(self, file):
        if file != "SlmodStats": #SlmodStats is set every 30 minutes, all other files are set when requested.
            self.setLuaDecoded(file)
        return self.luadecoded[file]

slmodstats = slmodstatslua()
slmodstats.setLuaDecoded("SlmodStats")

def getDecoded(request, file):
    if file == "SlmodStats":
        if request.headers.get("debug") == "true":
            file = "SlmodStatsDebugging"

    luadecoded = slmodstats.getLuaDecoded(file)

    if luadecoded == None:
            LOGGER.error("Couldn't decode "+file)
            raise HTTPException(status_code=500)
    else:
        return luadecoded


def print_configvalues(): #prints all config values in the console
    d = getAllConfigValues("configuration")
    for k1, v1 in d.items():
        if isinstance(v1, dict):
            for k2, v2 in v1.items():
                if v2 == "True":
                    print("{}: \033[32m{}\033[0m".format(k2, v2))
                elif v2 == "False":
                    print("{}: \033[31m{}\033[0m".format(k2, v2))
                else:
                    print("{}: \033[33m{}\033[0m".format(k2, v2))
        else:
            if v1 == "True":
                print("{}: \033[32m{}\033[0m".format(k1, v1))
            elif v1 == "False":
                print("{}: \033[31m{}\033[0m".format(k1, v1))
            else:
                print("{}: \033[33m{}\033[0m".format(k1, v1))

cache_time = 60 * 5 #5 minutes
rate_limit = "60/minute"

@app.on_event("startup")
def startup():
    print_configvalues()

@app.on_event("startup")
@repeat_every(seconds=60 * 30) #every 30 minutes
def repeated():

    slmodstats.setLuaDecoded("SlmodStats")

    if getConfigValue("realweather", "enableweatherchanges") == "True":
        update_miz_weather() #checks if weather update is needed and updates it if it is.

    if getConfigValue("webdav", "enablewebdav") == "True":
        getFileFromWebDAV("Slmod/SlmodStats.lua", "./SlmodStats.lua")


@app.middleware("http")
async def getData(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    LOGGER.debug("Request from "+request.client.host+" to "+request.url.path+" processed in "+str(process_time)+" seconds")
    return response


@app.get("/")
@limiter.limit(rate_limit)
async def root(request: Request, response: Response):
    return {"stats" : getDecoded(request, "SlmodStats")}

@app.get("/metar")
@limiter.limit(rate_limit)
async def Metar(request: Request, response: Response):
    return {"metar" : getMetar()}

@app.get("/players")
@limiter.limit(rate_limit)
async def PlayersList(request: Request, response: Response):
    return {"players" : getPlayersList(getDecoded(request, "SlmodStats"))}

@app.get("/player/{name:path}")
@limiter.limit(rate_limit)
async def PlayersStats(request: Request, response: Response, name: str):
    return {"player" : getPlayerStats(name, getDecoded(request, "SlmodStats"))}

@app.get("/playerairplanelist/{name:path}")
@limiter.limit(rate_limit)
async def PlayerAirplaneList(request: Request, response: Response, name: str):
    return {"airplanes" : getPlayerAirplaneList(name, getDecoded(request, "SlmodStats"))}

@app.get("/playerairplanestats/{name:path}/{airplane}")
@limiter.limit(rate_limit)
async def PlayerAirplaneStats(name: str, airplane, request: Request, response: Response):
    return {"airplane_stats" : getPlayerAirplaneStats(name, airplane, getDecoded(request, "SlmodStats"))}

@app.get("/playerbyname/{name:path}")
@limiter.limit(rate_limit)
async def PlayerDataByName(name: str, request: Request, response: Response):
    return {"UCID" : getPlayerUCIDByName(name, getDecoded(request, "SlmodStats"))}

@app.get("/playerrankingbyflighttime")
@limiter.limit(rate_limit)
async def PlayerRankingByFlightTime(request: Request, response: Response):
    return {"flighttimeranking" : getPlayerRankingByFlightTime(getDecoded(request, "SlmodStats"))}

@app.get("/playerrankingbypoints")
@limiter.limit(rate_limit)
async def PlayerRankingByFlightTime(request: Request, response: Response):
    return {"pointranking" : getPlayerRankingByPoints(getDecoded(request, "SlmodStats"))}

@app.get("/allplayerstats")
@limiter.limit(rate_limit)
async def AllPlayerStats(request: Request, response: Response):
    return { "allplayerstats" : getAllPlayerStats(getDecoded(request, "SlmodStats")) }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)