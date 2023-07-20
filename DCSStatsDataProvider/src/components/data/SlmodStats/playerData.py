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
                # Convert keys to integers if possible, otherwise log an error
                numeric_names = {}
                for k, v in names.items():
                    try:
                        key_int = int(k)
                        numeric_names[key_int] = v
                    except ValueError:
                        LOGGER.error(f"Key in 'names' is not an integer: {k}")

                if numeric_names:
                    max_key = max(numeric_names.keys())
                    last_name = numeric_names[max_key]
                    if playerName.lower() in last_name.lower():
                        return ucid
            # If names is empty, continue to the next ucid
        except Exception as e:
            LOGGER.error("Error getting player UCID by name")
            LOGGER.exception(e)
            raise HTTPException(status_code=500)
    raise HTTPException(status_code=404, detail="Player not found")

