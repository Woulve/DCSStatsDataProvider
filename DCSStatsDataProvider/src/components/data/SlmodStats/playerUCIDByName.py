def getPlayerUCIDByName(playerName, luadecoded):
    for item in luadecoded:
        for ucid in luadecoded[item]:
            if(playerName in list(luadecoded[item][ucid]["names"].values())):
                return(ucid)