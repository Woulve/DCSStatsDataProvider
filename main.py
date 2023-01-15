from fastapi import FastAPI, Request, HTTPException, Response
from fastapi_utils.tasks import repeat_every
from fastapi.middleware.cors import CORSMiddleware
from src.util.webDAV import getFileFromWebDAV
from src.util.serverlogger import serverLogger
import time
import configparser


from src.components.luaparser.slmodStatsParser import getLuaDecoded_slmodStats
from src.components.data.SlmodStats.playerData import getPlayersList
from src.components.data.SlmodStats.playerData import getPlayerDataByUCID
from src.components.data.SlmodStats.playerData import getPlayerUCIDByName

from src.components.data.SlmodStats.Rankings.playerRankingByFlighTime import getPlayerRankingByFlightTime;

app = FastAPI()

# logging.basicConfig(filename="serverlog.log", format='%(asctime)s %(message)s', filemode='a')

LOGGER = serverLogger()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SlmodStatsFiles():
    slmodStats_File = "Slmod/SlmodStats.lua"

class LastFetchSuccessful():
    lastFetchSuccessful = False
    def setLastFetchSuccessful(self, value: bool):
        self.lastFetchSuccessful = value
    def getLastFetchSuccessful(self):
        return self.lastFetchSuccessful

lastFetchSuccessful = LastFetchSuccessful();

def getDecoded(file, response):
    config = configparser.ConfigParser()
    config.read('config.cfg')

    slmodStats_File = SlmodStatsFiles.slmodStats_File

    if config["configuration"]["enablerealtimeupdates"] == "True":
        response.headers["Realtimeupdates"] = "True"
        enablerealtimeupdates = True
    else:
        enablerealtimeupdates = False
        response.headers["Realtimeupdates"] = "False"
        
    match file:
        case slmodStats_File:
            luadecoded = getLuaDecoded_slmodStats(enablerealtimeupdates)
            if luadecoded == None:
                LOGGER.error("Couldn't read "+slmodStats_File)
                raise HTTPException(status_code=500)
            else:
                return luadecoded["stats"]
    


luadecoded = getLuaDecoded_slmodStats(False)

@app.on_event("startup")
@repeat_every(seconds=600)
def get_lua_from_webdav():
    if getFileFromWebDAV(SlmodStatsFiles.slmodStats_File) == 0:
        lastFetchSuccessful.setLastFetchSuccessful(False)
        LOGGER.exception("Couldn't fetch "+SlmodStatsFiles.slmodStats_File+" from WEBDav server.")
        raise HTTPException(status_code=500)
    else:
        lastFetchSuccessful.setLastFetchSuccessful(True)
        LOGGER.info("Successfully fetched "+SlmodStatsFiles.slmodStats_File)
    

@app.middleware("http")
async def getData(request: Request, call_next):
    LOGGER.debug("Processing...")
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    LOGGER.debug("Processed in "+str(process_time)+" seconds")
    return response


@app.get("/")
async def root(response: Response):
    return {"stats" : getDecoded(SlmodStatsFiles.slmodStats_File, response)}

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

@app.get("/lastfetchsuccessful")
async def LastFetchSuccessful():
    return { "lastFetchSuccessful" : lastFetchSuccessful.getLastFetchSuccessful() }
