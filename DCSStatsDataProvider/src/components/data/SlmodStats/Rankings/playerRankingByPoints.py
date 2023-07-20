from fastapi import HTTPException
from src.util.serverlogger import serverLogger

LOGGER = serverLogger()

def getPlayerRankingByPoints(luadecoded):
    player_ranking = {}
    for ucid, player_data in luadecoded.items():
        try:
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

            player_ranking[player_name] = player_data.get("totalPoints", 0)
        except Exception as e:
            LOGGER.error(f"Error getting player ranking by points for UCID: {ucid}")
            LOGGER.exception(e)
            raise HTTPException(status_code=500)

    return sorted(player_ranking.items(), key=lambda x: x[1], reverse=True)
