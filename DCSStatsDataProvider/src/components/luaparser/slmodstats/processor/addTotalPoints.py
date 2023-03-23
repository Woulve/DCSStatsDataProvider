

def addTotalPoints(luadecoded):
    for ucid in luadecoded:
        total_points = 0
        for aircrafttimes in luadecoded[ucid]["times"]:
            try:
                for unit_type in luadecoded[ucid]["times"][aircrafttimes]["kills"]:
                    unit_value = luadecoded[ucid]["times"][aircrafttimes]["kills"][unit_type].get("total", 0)
                    if unit_type == "Ground Units":
                        total_points += unit_value * 2
                    elif unit_type == "Planes":
                        total_points += unit_value * 3
                    elif unit_type == "Ships":
                        total_points += unit_value * 5
                    elif unit_type == "Helicopters":
                        total_points += unit_value * 1
            except Exception:
                pass
        luadecoded[ucid]["totalPoints"] = total_points

    return luadecoded


