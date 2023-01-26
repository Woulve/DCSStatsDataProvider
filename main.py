import time
import uvicorn
import os

from fastapi import FastAPI, Request, HTTPException, Response, Header
from fastapi_utils.tasks import repeat_every
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from datetime import date
import base64

from src.util.webDAV import getFileFromWebDAV, pushFileToWebdav
from src.util.serverlogger import serverLogger
from src.util.getConfigValue import getConfigValue, getAllConfigValues
from src.components.luaparser.slmodStatsParser import getLuaDecoded_slmodStats
from src.components.data.SlmodStats.playerData import getPlayersList
from src.components.data.SlmodStats.playerStats import getPlayerStats
from src.components.data.SlmodStats.playerData import getPlayerDataByUCID
from src.components.data.SlmodStats.playerData import getPlayerUCIDByName
from src.components.data.SlmodStats.allPlayerStats import getAllPlayerStats
from src.util.realweather.run_weatherupdate import update_miz_weather
from src.components.data.SlmodStats.Rankings.playerRankingByFlightTime import getPlayerRankingByFlightTime;
from src.components.data.SlmodStats.Rankings.playerRankingByPoints import getPlayerRankingByPoints;
from src.util.realweather.run_weatherupdate import check_if_weather_update_is_needed

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


LOGGER = serverLogger()

origins = [
    "http://localhost:3000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SlmodStatsFiles(): #remote lcoation of the slmodstats file
    slmodStats_File = "Slmod/SlmodStats.lua"

class LastFetchSuccessful():
    lastFetchSuccessful = False
    def setLastFetchSuccessful(self, value: bool):
        self.lastFetchSuccessful = value
    def getLastFetchSuccessful(self):
        return self.lastFetchSuccessful

lastFetchSuccessful = LastFetchSuccessful();

def getDecoded(file, response):

    slmodStats_File = SlmodStatsFiles.slmodStats_File

    if getConfigValue("configuration", "enablerealtimeupdates") == "True":
        response.headers["Realtimeupdates"] = "True"
        enablerealtimeupdates = False
    else:
        enablerealtimeupdates = False
        response.headers["Realtimeupdates"] = "False"

    if file == SlmodStatsFiles.slmodStats_File:
        luadecoded = getLuaDecoded_slmodStats(enablerealtimeupdates)
        if luadecoded == None:
            LOGGER.error("Couldn't read "+slmodStats_File)
            raise HTTPException(status_code=500)
        else:
            return luadecoded["stats"]

def updateWeather():
    #when enablewebdav and webdavmission is true, we fetch the mission.miz from the webdav server and update the weather in it.
    #If it is false, we use the local files in the realweather/Active folder.
    if getConfigValue("realweather", "webdavmission") == "True" and getConfigValue("webdav", "enablewebdav") == "True":
        if (getFileFromWebDAV("Active/mission.miz", "./src/util/realweather/Active/mission.miz")) == 0:
            LOGGER.error("Couldn't fetch mission.miz from WEBDav server.")
            return
    update_miz_weather()

    mypath = os.path.abspath(os.path.dirname(__file__))
    os.chdir(mypath) #change back working directory to this folder, we had to change it in the weather updater so it can find the .json file.

    if getConfigValue("realweather", "webdavmission") == "True" and getConfigValue("webdav", "enablewebdav") == "True":
        if (pushFileToWebdav("Active/foothold_remastered_realweather.miz", "./src/util/realweather/Active/foothold_remastered_realweather.miz")) == 0:
            LOGGER.error("Couldn't push foothold_remastered_realweather.miz to WEBDav server.")
            return



luadecoded = getLuaDecoded_slmodStats(False)

cache_time = 60 * 5 #5 minutes
rate_limit = "60/minute"

@app.on_event("startup")
def startup():
    FastAPICache.init(InMemoryBackend())
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    ENDC = '\033[0m'
    # print(getAllConfigValues("configuration"))

@app.on_event("startup")
@repeat_every(seconds=60 * 30) #every 30 minutes
def repeated():
    if getConfigValue("realweather", "enableweatherchanges") == "True":
        updateWeather() #checks if weather update is needed and updates it if it is.

    if getConfigValue("webdav", "enablewebdav") == "True":
        if getFileFromWebDAV(SlmodStatsFiles.slmodStats_File, "./SlmodStats.lua") == 0:
            lastFetchSuccessful.setLastFetchSuccessful(False)
            raise HTTPException(status_code=500)
        else:
            lastFetchSuccessful.setLastFetchSuccessful(True)

def getAuth(request: Request):
    if request.method == "GET" or request.method == "POST":
        datet = date.today().strftime("%Y%m%d")
        try:
            auth_header = request.headers.get("Authentication")
            dec = base64.b64decode(auth_header)
            if dec != datet.encode():
                raise HTTPException(status_code=401, detail="Invalid authentication")
        except:
            LOGGER.error("Authentication header not found")
            raise HTTPException(status_code=401, detail="Invalid authentication")


@app.middleware("http")
async def getData(request: Request, call_next):
    if getConfigValue("authentication", "enablesimpleauth") == "True":
        getAuth(request)
    LOGGER.debug("Processing...")
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    LOGGER.debug("Processed in "+str(process_time)+" seconds")
    return response


@app.get("/")
@limiter.limit(rate_limit)
@cache(namespace="api", expire=cache_time)
async def root(request: Request, response: Response):
    return {"stats" : getDecoded(SlmodStatsFiles.slmodStats_File, response)}

@app.get("/players")
@limiter.limit(rate_limit)
@cache(namespace="api", expire=cache_time)
async def PlayersList(request: Request, response: Response):
    return {"players" : getPlayersList(getDecoded(SlmodStatsFiles.slmodStats_File, response))}

@app.get("/player/{name}")
@limiter.limit(rate_limit)
@cache(namespace="api", expire=cache_time)
async def PlayersList(name, request: Request, response: Response):
    return {"player" : getPlayerStats(name, getDecoded(SlmodStatsFiles.slmodStats_File, response))}

@app.get("/playerbyucid/{UCID}")
@limiter.limit(rate_limit)
@cache(namespace="api", expire=cache_time)
async def PlayerDataByUCID(UCID,request: Request, response: Response):
    return { UCID : getPlayerDataByUCID(getDecoded(SlmodStatsFiles.slmodStats_File, response), UCID)}

@app.get("/playerbyname/{name}")
@limiter.limit(rate_limit)
@cache(namespace="api", expire=cache_time)
async def PlayerDataByName(name, request: Request, response: Response):
    return {"UCID" : getPlayerUCIDByName(name, getDecoded(SlmodStatsFiles.slmodStats_File, response))}

@app.get("/playerrankingbyflighttime")
@limiter.limit(rate_limit)
@cache(namespace="api", expire=cache_time)
async def PlayerRankingByFlightTime(request: Request, response: Response):
    return {"ranking" : getPlayerRankingByFlightTime(getDecoded(SlmodStatsFiles.slmodStats_File, response))}

@app.get("/playerrankingbypoints")
@limiter.limit(rate_limit)
@cache(namespace="api", expire=cache_time)
async def PlayerRankingByFlightTime(request: Request, response: Response):
    return {"ranking" : getPlayerRankingByPoints(getDecoded(SlmodStatsFiles.slmodStats_File, response))}

@app.get("/lastfetchsuccessful")
@limiter.limit(rate_limit)
@cache(namespace="api", expire=cache_time)
async def LastFetch(request: Request, response: Response):
    return { "lastFetchSuccessful" : lastFetchSuccessful.getLastFetchSuccessful() }

@app.get("/allplayerstats")
@limiter.limit(rate_limit)
@cache(namespace="api", expire=cache_time)
async def AllPlayerStats(request: Request, response: Response):
    return { "allPlayerStats" : getAllPlayerStats(getDecoded(SlmodStatsFiles.slmodStats_File, response)) }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)