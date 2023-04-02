from fastapi import HTTPException
from src.util.serverlogger import serverLogger

LOGGER = serverLogger()

def getPlayerRankingByPoints(luadecoded):
    player_ranking = {}
    for ucid, player_data in luadecoded.items():

        player_name = ""

        names = player_data["names"]
        if names:
            max_key = max(names.keys())
            if max_key is not None:
                player_name = names[max_key]

        player_ranking[player_name] = player_data.get("totalPoints", 0)

    # return player_ranking
    return sorted(player_ranking.items(), key=lambda x: x[1], reverse=True)