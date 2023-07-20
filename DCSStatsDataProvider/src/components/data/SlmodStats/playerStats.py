from src.components.data.SlmodStats.playerData import getPlayerUCIDByName
from fastapi import FastAPI, Request, HTTPException, Response
from src.util.serverlogger import serverLogger

LOGGER = serverLogger()

def getPlayerStats(name, luadecoded):
    player_stats = {}

    ucid = getPlayerUCIDByName(name, luadecoded)

    if ucid is None:
        raise HTTPException(status_code=404, detail="Player not found")

    if luadecoded is None:
        return None

    player_data = luadecoded.get(ucid, [])
    a2akillstotal = 0
    a2gkillstotal = 0
    a2shipkillstotal = 0
    deathstotal = 0
    favorite_weapon = {
        "name": "",
        "kills": 0
    }
    fav_plane = {
        "name": "",
        "kills_planes": 0,
        "kills_groundunits": 0,
        "kills_ships": 0,
        "kills_buildings": 0,
        "kills_helicopters": 0,
        "time": 0,
    }

    player_name = ""

    names = player_data["names"]
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
            player_name = numeric_names[max_key]

    for aircraftname, aircraft_data in player_data.get("times", {}).items():
        if aircraftname == "totalFlightTime":
            continue
        a2akillstotal += aircraft_data.get("kills", {}).get("Planes", {}).get("total", 0)
        a2akillstotal += aircraft_data.get("kills", {}).get("Helicopters", {}).get("total", 0)
        a2gkillstotal += aircraft_data.get("kills", {}).get("Ground Units", {}).get("total", 0)
        a2shipkillstotal += aircraft_data.get("kills", {}).get("Ships", {}).get("total", 0)
        deathstotal += aircraft_data.get("actions", {}).get("losses", {}).get("pilotDeath", 0)
        if aircraft_data.get("total", 0) > fav_plane["time"]:
            fav_plane["name"] = aircraftname
            fav_plane["kills_planes"] = aircraft_data.get("kills", {}).get("Planes", {}).get("total", 0)
            fav_plane["kills_groundunits"] = aircraft_data.get("kills", {}).get("Ground Units", {}).get("total", 0)
            fav_plane["kills_ships"] = aircraft_data.get("kills", {}).get("Ships", {}).get("total", 0)
            fav_plane["kills_buildings"] = aircraft_data.get("kills", {}).get("Buildings", {}).get("total", 0)
            fav_plane["kills_helicopters"] = aircraft_data.get("kills", {}).get("Helicopters", {}).get("total", 0)
            fav_plane["time"] = aircraft_data.get("total", 0)

        for weaponname, weapon_data in aircraft_data.get("weapons", {}).items():
            if weaponname == "shot":  # shot sometimes appears as a weapon
                continue

            if isinstance(weapon_data, dict) and weapon_data.get("kills", 0) > favorite_weapon["kills"]:
                favorite_weapon["name"] = weaponname
                favorite_weapon["kills"] = weapon_data.get("kills", 0)

    player_stats = {
        "name": player_name,
        "ucid": ucid,
        "join_date": player_data.get("joinDate"),
        "last_join": player_data.get("lastJoin"),
        "total_points": player_data.get("totalPoints", 0),
        "total_a2akills": a2akillstotal,
        "total_a2gkills": a2gkillstotal,
        "total_a2shipkills": a2shipkillstotal,
        "total_deaths": deathstotal,
        "fav_plane": fav_plane,
        "fav_weapon": favorite_weapon,
        "total_flight_time": player_data.get("times", {}).get("totalFlightTime", 0),
    }

    return player_stats
