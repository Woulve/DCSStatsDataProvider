from fastapi import HTTPException
from src.util.serverlogger import serverLogger

LOGGER = serverLogger()

def getPlayerRankingByFlightTime(luadecoded):
    playerRanking = {}
    for ucid in luadecoded:
        try:
            playerRanking[list(luadecoded[ucid]["names"].values())[-1]] = luadecoded[ucid]["times"]["totalFlightTime"]
        except Exception as e:
            LOGGER.error("Error getting player ranking by flight time for UCID: " + ucid)
            LOGGER.exception(e)
            raise HTTPException(status_code=500)

    return sorted(playerRanking.items(), key=lambda x:x[1], reverse=True)