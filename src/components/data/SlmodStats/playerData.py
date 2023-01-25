from fastapi import FastAPI, Request, HTTPException, Response

def getPlayersList(luadecoded):
    playersList = []
    for ucid in luadecoded["stats"]:
        playerdata = {}
        playerdata["name"] = list(luadecoded["stats"][ucid]["names"].values())[-1]
        playerdata["ucid"] = ucid
        playersList.append(playerdata)
    return playersList

def getPlayerDataByUCID(luadecoded, UCID):
    return luadecoded["stats"][UCID]

def getPlayerUCIDByName(playerName: str, luadecoded):
    for item in luadecoded:
        for ucid in luadecoded[item]:
            if(playerName.lower() in list(luadecoded[item][ucid]["names"].values())[-1].lower()):
                return(ucid)
        raise HTTPException(status_code=404, detail="Player not found")
