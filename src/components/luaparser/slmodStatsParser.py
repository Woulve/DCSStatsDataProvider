from slpp import slpp as lua
from src.components.luaparser.luaprocessor import process
from src.components.luaparser.processor.updateLuaDecoded import updateLuaDecoded
from collections import defaultdict
from collections import ChainMap


def getLuaDecoded_slmodStats(update):
    # f = open("C:\\Users\\elias\\Saved Games\\DCS.openbeta_server\\Slmod\\SlmodStats.lua", "r")
    f = open("C:\\Users\\elias\\Desktop\\SlmodStats.lua", "r")
    filecontent = f.read()
    luadecoded_serialized = lua.decode("{"+filecontent.split("-- end of stats\n\n")[0]+"}")

    #The log file contains an array, and every event is appended to the file as a lua assignment. So we have to get the initial state here, and modify the dict for every line in the log file. Ugly, but it works.
    luadecoded_additions = filecontent.split("-- end of stats\n\n")[1]
    f.close() 
    if update == True:
        return updateLuaDecoded(luadecoded_serialized, luadecoded_additions)
    else:
        return luadecoded_serialized