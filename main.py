from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from src.components.luaparser.slmodStatsParser import getLuaDecoded_slmodStats
from src.components.data.SlmodStats.playerData import getPlayersList
from src.components.data.SlmodStats.playerData import getPlayerDataByUCID
from src.components.data.SlmodStats.playerData import getPlayerUCIDByName

from src.components.data.SlmodStats.Rankings.playerRankingByFlighTime import getPlayerRankingByFlightTime;

app = FastAPI()

luadecoded = getLuaDecoded_slmodStats(False)

@app.on_event("startup")
@repeat_every(seconds=10)
def refresh():
    global luadecoded
    # print("Refreshing...")
    # luadecoded = getLuaDecoded_slmodStats(True)
    # print("Refreshed")  


@app.get("/")
async def root():
    luadecoded = getLuaDecoded_slmodStats(True)
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
