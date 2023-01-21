from fastapi import HTTPException
from src.util.serverlogger import serverLogger

LOGGER = serverLogger()

def getAllPlayerStats(luadecoded):
    playerStats = {}
    if luadecoded is None:
        return None
    else:
        for type in luadecoded:
            for ucid in luadecoded[type]:
                joinDate = 0
                lastjoin = 0
                joinDate = luadecoded["stats"][ucid]["joinDate"]
                lastjoin = luadecoded["stats"][ucid]["lastJoin"]
                totalPoints = luadecoded["stats"][ucid]["totalPoints"]
                totalFlightTime = luadecoded["stats"][ucid]["times"]["totalFlightTime"]
                lastUsedName = list(luadecoded["stats"][ucid]["names"].values())[-1]
                playerStats[lastUsedName] = {}
                playerStats[lastUsedName]["joinDate"] = joinDate
                playerStats[lastUsedName]["lastJoin"] = lastjoin
                playerStats[lastUsedName]["totalPoints"] = totalPoints
                playerStats[lastUsedName]["totalFlightTime"] = totalFlightTime
                try:
                    for aircrafttimes in luadecoded[type][ucid]["times"]:
                        for aircraftname in luadecoded[type][ucid]["times"].keys():
                            if aircraftname == "totalFlightTime":
                                continue
                            playerStats[lastUsedName][aircraftname] = {}
                            playerStats[lastUsedName][aircraftname]["total"] = luadecoded[type][ucid]["times"][aircraftname]["total"]
                            playerStats[lastUsedName][aircraftname]["kills"] = {}
                            playerStats[lastUsedName][aircraftname]["actions"] = {}
                            try:
                                for killedtype in luadecoded[type][ucid]["times"][aircraftname]["kills"]:
                                    playerStats[lastUsedName][aircraftname]["kills"][killedtype] = luadecoded[type][ucid]["times"][aircraftname]["kills"][killedtype]
                            except:
                                continue
                            try:
                                for actions in luadecoded[type][ucid]["times"][aircraftname]["actions"]:
                                    playerStats[lastUsedName][aircraftname]["actions"][actions] = luadecoded[type][ucid]["times"][aircraftname]["actions"][actions]
                            except:
                                continue
                except:
                    LOGGER.error("Error getting player stats")
                    raise HTTPException(status_code=500)
        return sorted(playerStats.items(), key=lambda x:x[1]["totalPoints"], reverse=True)