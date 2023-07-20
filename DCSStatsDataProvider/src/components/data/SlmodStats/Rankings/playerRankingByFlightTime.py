from fastapi import HTTPException
from src.util.serverlogger import serverLogger

LOGGER = serverLogger()

def getPlayerRankingByFlightTime(luadecoded):
    playerRanking = {}
    for ucid in luadecoded:
        try:
            player_name = ""
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
                    player_name = numeric_names[max_key]

            playerRanking[player_name] = luadecoded[ucid]["times"]["totalFlightTime"]
        except Exception as e:
            LOGGER.error("Error getting player ranking by flight time for UCID: " + ucid)
            LOGGER.exception(e)
            raise HTTPException(status_code=500)

    return sorted(playerRanking.items(), key=lambda x: x[1], reverse=True)
