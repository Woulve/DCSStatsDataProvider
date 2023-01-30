from src.components.luaparser.slmodstats.processor.updateLuaDecoded import recursive_dict_merge


def add_totals(obj):
    total = 0
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == 'total':
                total += value
            else:
                total += add_totals(value)
    return total

def addTotalKills(luadecoded):
    for type in luadecoded:
        for ucid in luadecoded[type]:
            totalPoints = 0
            # if (ucid == "12d41bd5fdc3ac1412e45b52f2851252"):
            for aircrafttimes in luadecoded[type][ucid]["times"]:
                # print(aircrafttimes)
                try:
                    for type_unitkilled in luadecoded[type][ucid]["times"][aircrafttimes]["kills"]:
                        if type_unitkilled == "Ground Units":
                            try:
                                totalPoints += luadecoded[type][ucid]["times"][aircrafttimes]["kills"]["Ground Units"]["total"] * 2
                            except Exception as e:
                                continue
                        if type_unitkilled == "Planes":
                            try:
                                totalPoints += luadecoded[type][ucid]["times"][aircrafttimes]["kills"]["Planes"]["total"] * 3
                            except Exception as e:
                                continue
                        if type_unitkilled == "Ships":
                            try:
                                totalPoints += luadecoded[type][ucid]["times"][aircrafttimes]["kills"]["Ships"]["total"] * 5
                            except Exception as e:
                                continue
                        if type_unitkilled == "Helicopters":
                            try:
                                totalPoints += luadecoded[type][ucid]["times"][aircrafttimes]["kills"]["Helicopters"]["total"] * 1
                            except Exception as e:
                                continue
                except Exception as e:
                    continue
            luadecoded[type][ucid]["totalPoints"] = totalPoints

    return luadecoded