from src.components.data.SlmodStats.playerData import getPlayerUCIDByName
from fastapi import FastAPI, Request, HTTPException, Response

def getPlayerStats(name, luadecoded):
    player_stats = {}
    ucid = getPlayerUCIDByName(name, luadecoded)

    if ucid == None:
        raise HTTPException(status_code=404, detail="Player not found")

    if luadecoded is None:
        return None

    player_stats = {}

    player_data = luadecoded.get(ucid, [])
    a2akillstotal = 0
    a2gkillstotal = 0
    deathstotal = 0
    player_name = player_data["names"][list(player_data["names"].keys())[-1]]

    for aircraftname, aircraft_data in player_data.get("times", {}).items():
        if aircraftname == "totalFlightTime":
            continue
        a2akillstotal += aircraft_data.get("kills", {}).get("Planes", {}).get("total", 0)
        a2akillstotal += aircraft_data.get("kills", {}).get("Helicopters", {}).get("total", 0)
        a2gkillstotal += aircraft_data.get("kills", {}).get("Ground Units", {}).get("total", 0)
        deathstotal += aircraft_data.get("actions", {}).get("losses", {}).get("pilotDeath", 0)

    player_stats = {
        "name": player_name,
        "ucid": ucid,
        "join_date": player_data.get("joinDate"),
        "last_join": player_data.get("lastJoin"),
        "total_points": player_data.get("totalPoints", 0),
        "total_a2akills": a2akillstotal,
        "total_a2gkills": a2gkillstotal,
        "total_deaths": deathstotal,
        "total_flight_time": player_data.get("times", {}).get("totalFlightTime", 0),
        "aircraft_stats": extract_aircraft_stats(player_data.get("times"))
    }

    return player_stats

def extract_aircraft_stats(times):
    aircraft_stats = {}
    for aircraftname, aircraft_data in times.items():
        if aircraftname == "totalFlightTime":
            continue
        aircraft_stats[aircraftname] = {
            "total": aircraft_data.get("total", 0),
            "actions": aircraft_data.get("action", {}),
            "kills": {
                killedtype: kills_data.get("total", 0)
                for killedtype, kills_data in aircraft_data.get("kills", {}).items()
            }
        }
    return aircraft_stats