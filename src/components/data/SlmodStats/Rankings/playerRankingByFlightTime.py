from fastapi import HTTPException
from src.util.serverlogger import serverLogger

LOGGER = serverLogger()

def getPlayerRankingByFlightTime(luadecoded):
    playerRanking = {}
    for type in luadecoded:
        for ucid in luadecoded[type]:
            try:
                playerRanking[list(luadecoded[ucid]["names"].values())[-1]] = luadecoded[ucid]["times"]["totalFlightTime"]
            except Exception as e:
                LOGGER.info("Error getting player ranking by flight time")
                raise HTTPException(status_code=500)

    return sorted(playerRanking.items(), key=lambda x:x[1], reverse=True)