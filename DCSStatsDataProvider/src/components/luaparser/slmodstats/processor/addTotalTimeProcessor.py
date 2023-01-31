from src.components.luaparser.slmodstats.processor.updateLuaDecoded import recursive_dict_merge


def addTotalTime(luadecoded):
    for ucid in luadecoded:
        totalTime = 0
        for aircrafttimes in luadecoded[ucid]["times"]:
            totalTime+=luadecoded[ucid]["times"][aircrafttimes]["total"]
        luadecoded[ucid]["times"]["totalFlightTime"] = totalTime

    return luadecoded