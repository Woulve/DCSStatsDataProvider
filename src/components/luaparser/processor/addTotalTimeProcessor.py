from src.components.luaparser.processor.updateLuaDecoded import recursive_dict_merge


def addTotalTime(luadecoded):
    print(luadecoded)
    for type in luadecoded:
        for ucid in luadecoded[type]:
            totalTime = 0
            # print(luadecoded[type][ucid]["times"])
            print("bbb")
            for aircrafttimes in luadecoded[type][ucid]["times"]:
                totalTime+=luadecoded[type][ucid]["times"][aircrafttimes]["total"]
            luadecoded[type][ucid]["times"]["totalFlightTime"] = totalTime

    return luadecoded