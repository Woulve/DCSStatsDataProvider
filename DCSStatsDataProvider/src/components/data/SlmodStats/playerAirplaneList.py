from src.components.data.SlmodStats.playerData import getPlayerUCIDByName
from fastapi import FastAPI, Request, HTTPException, Response

def getPlayerAirplaneList(name, luadecoded):
    airplane_list = []
    ucid = getPlayerUCIDByName(name, luadecoded)

    if ucid == None:
        raise HTTPException(status_code=404, detail="Player not found")

    if luadecoded is None:
        return None

    player_data = luadecoded.get(ucid, [])

    for aircraftname, aircraft_data in player_data.get("times", {}).items():
        if aircraftname == "totalFlightTime":
            continue
        airplane_list.append(aircraftname)

    return airplane_list