from src.components.data.SlmodStats.playerData import getPlayerUCIDByName
from src.components.data.SlmodStats.playerAirplaneList import getPlayerAirplaneList
from fastapi import FastAPI, Request, HTTPException, Response

def hasFlownAirplane(ucid, player_data, name, airplane, luadecoded):
    if ucid == None:
        raise HTTPException(status_code=404, detail="Player not found")

    if luadecoded is None:
        return None

    for aircraft in getPlayerAirplaneList(name, luadecoded):
        if aircraft["name"] == airplane:
            return True

    return False

def getPlayerAirplaneStats(name, airplane, luadecoded):
    airplane_stats = {
        "name": "",
        "kills_planes": 0,
        "kills_groundunits": 0,
        "kills_ships": 0,
        "kills_buildings": 0,
        "kills_helicopters": 0,
        "time": 0,
    }
    ucid = getPlayerUCIDByName(name, luadecoded)
    player_data = luadecoded.get(ucid, [])

    if hasFlownAirplane(ucid, player_data, name, airplane, luadecoded) == False:
        raise HTTPException(status_code=404, detail="Player has not flown this airplane")

    if luadecoded is None:
        return None


    for aircraftname, aircraft_data in player_data.get("times", {}).items():
        if aircraftname == airplane:
            airplane_stats["name"] = aircraftname
            airplane_stats["kills_planes"] = aircraft_data.get("kills", {}).get("Planes", {}).get("total", 0)
            airplane_stats["kills_groundunits"] = aircraft_data.get("kills", {}).get("Ground Units", {}).get("total", 0)
            airplane_stats["kills_ships"] = aircraft_data.get("kills", {}).get("Ships", {}).get("total", 0)
            airplane_stats["kills_buildings"] = aircraft_data.get("kills", {}).get("Buildings", {}).get("total", 0)
            airplane_stats["kills_helicopters"] = aircraft_data.get("kills", {}).get("Helicopters", {}).get("total", 0)
            airplane_stats["time"] = aircraft_data.get("total", 0)
            break

    return airplane_stats