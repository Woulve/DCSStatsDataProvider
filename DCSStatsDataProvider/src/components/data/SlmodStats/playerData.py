from fastapi import FastAPI, Request, HTTPException, Response
from src.util.serverlogger import serverLogger

LOGGER = serverLogger()

def getPlayersList(luadecoded):
    playersList = []
    for ucid in luadecoded:
        playerdata = {}
        playerdata["name"] = list(luadecoded[ucid]["names"].values())[-1]
        playerdata["ucid"] = ucid
        playersList.append(playerdata)
    return playersList


def getPlayerUCIDByName(playerName: str, luadecoded):
    for ucid in luadecoded:
        try:
            if(playerName.lower() in list(luadecoded[ucid]["names"].values())[-1].lower()):
                return(ucid)
        except Exception as e:
            LOGGER.error("Error getting player UCID by name")
            LOGGER.exception(e)
            raise HTTPException(status_code=500)
    raise HTTPException(status_code=404, detail="Player not found")
