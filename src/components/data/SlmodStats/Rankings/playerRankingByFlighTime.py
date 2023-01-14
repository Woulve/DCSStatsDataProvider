def getPlayerRankingByFlightTime(luadecoded, ranksToShow):
    playerRanking = {}
    
    for type in luadecoded:
        for ucid in luadecoded[type]:
            playerRanking[list(luadecoded["stats"][ucid]["names"].values())[-1]] = luadecoded["stats"][ucid]["times"]["totalFlightTime"]

    return sorted(playerRanking.items(), key=lambda x:x[1], reverse=True)