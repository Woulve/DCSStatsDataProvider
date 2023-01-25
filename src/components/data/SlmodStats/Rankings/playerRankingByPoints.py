from fastapi import HTTPException
from src.util.serverlogger import serverLogger

LOGGER = serverLogger()

# def getPlayerRankingByPoints(luadecoded):
#     playerRanking = {}
#     # print(luadecoded)
#     for type in luadecoded:
#         for ucid in luadecoded[type]:
#             try:
#                 playerRanking[list(luadecoded["stats"][ucid]["names"].values())[-1]] = luadecoded["stats"][ucid]["totalPoints"]
#             except:
#                 LOGGER.error("Error getting player ranking by points")
#                 raise HTTPException(status_code=500)

#     return sorted(playerRanking.items(), key=lambda x:x[1], reverse=True)

def getPlayerRankingByPoints(luadecoded):
    player_ranking = {}
    for ucid, player_data in luadecoded.get("stats", {}).items():
        player_name = player_data["names"][list(player_data["names"].keys())[-1]]
        player_ranking[player_name] = player_data.get("totalPoints", 0)

    # return player_ranking
    return sorted(player_ranking.items(), key=lambda x: x[1], reverse=True)