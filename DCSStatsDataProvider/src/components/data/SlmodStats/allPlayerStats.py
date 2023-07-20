from fastapi import HTTPException
from src.util.serverlogger import serverLogger

LOGGER = serverLogger()

def getAllPlayerStats(luadecoded):
    if luadecoded is None:
        return None

    player_stats = {}

    for ucid, player_data in luadecoded.items():
        try:
            a2akillstotal = 0
            a2gkillstotal = 0
            deathstotal = 0
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
                deathstotal += aircraft_data.get("actions", {}).get("losses", {}).get("pilotDeath", 0)

            player_stats[player_name] = {
                "join_date": player_data.get("joinDate"),
                "last_join": player_data.get("lastJoin"),
                "total_points": player_data.get("totalPoints", 0),
                "total_a2akills": a2akillstotal,
                "total_a2gkills": a2gkillstotal,
                "total_deaths": deathstotal,
                "total_flight_time": player_data.get("times", {}).get("totalFlightTime", 0),
                "aircraft_stats": extract_aircraft_stats(player_data.get("times"))
            }
        except Exception as e:
            LOGGER.error(f"Error getting stats for player with UCID: {ucid}")
            LOGGER.exception(e)
            raise HTTPException(status_code=500)

    return sorted(player_stats.items(), key=lambda x: x[1]['total_points'], reverse=True)

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