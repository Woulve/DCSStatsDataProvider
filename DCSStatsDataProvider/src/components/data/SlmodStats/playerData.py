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
            names = luadecoded[ucid]["names"]
            if names:
                max_key = max(names.keys())
                if max_key is not None:
                    last_name = names[max_key]
                    if playerName.lower() in last_name.lower():
                        return ucid
            # If names is empty, continue to the next ucid
        except Exception as e:
            LOGGER.error("Error getting player UCID by name")
            LOGGER.exception(e)
            raise HTTPException(status_code=500)
    raise HTTPException(status_code=404, detail="Player not found")
