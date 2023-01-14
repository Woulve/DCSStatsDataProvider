
def addTotalTime(luadecoded):
    for type in luadecoded:
        # print(luadecoded[type])
        for ucid in luadecoded[type]:
            totalTime = 0
            for aircrafttimes in luadecoded[type][ucid]["times"]:
                totalTime+=luadecoded[type][ucid]["times"][aircrafttimes]["total"]
            luadecoded[type][ucid]["times"]["totalFlightTime"] = totalTime

    return luadecoded