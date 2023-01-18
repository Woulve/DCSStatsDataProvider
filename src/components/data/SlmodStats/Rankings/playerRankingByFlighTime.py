def getPlayerRankingByFlightTime(luadecoded):
    playerRanking = {}

    for type in luadecoded:
        for ucid in luadecoded[type]:
            try:
                playerRanking[list(luadecoded["stats"][ucid]["names"].values())[-1]] = luadecoded["stats"][ucid]["times"]["totalFlightTime"]
            except:
                pass

    return sorted(playerRanking.items(), key=lambda x:x[1], reverse=True)