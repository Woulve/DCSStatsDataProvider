from fastapi import HTTPException
from src.util.serverlogger import serverLogger

LOGGER = serverLogger()

def getPlayerRankingByFlightTime(luadecoded):
    playerRanking = {}
    for type in luadecoded:
        for ucid in luadecoded[type]:
            try:
                playerRanking[list(luadecoded["stats"][ucid]["names"].values())[-1]] = luadecoded["stats"][ucid]["times"]["totalFlightTime"]
            except:
                LOGGER.info("Error getting player ranking by flight time")
                raise HTTPException(status_code=500)

    return sorted(playerRanking.items(), key=lambda x:x[1], reverse=True)