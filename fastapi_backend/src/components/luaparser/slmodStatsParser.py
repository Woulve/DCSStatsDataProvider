from slpp import slpp as lua
from src.components.luaparser.luaprocessor import process
from src.components.luaparser.processor.updateLuaDecoded import updateLuaDecoded
from collections import defaultdict


def getLuaDecoded_slmodStats(update):
    f = open("C:\\Users\\elias\\Saved Games\\DCS.openbeta_server\\Slmod\\SlmodStats.lua", "r")
    filecontent = f.read()
    luadecoded_serialized = lua.decode("{"+filecontent.split("-- end of stats\n\n")[0]+"}")
    # luadecoded_serialized = 
    # print(type(lua.decode("{"+filecontent.split("-- end of stats\n\n")[0]+"}")))
    # print(luadecoded_serialized.get())
    # luadecoded_serialized = 
    print(type(luadecoded_serialized))
    # luadecoded_serialized = 
    luadecoded_additions = defaultdict(lambda: defaultdict(dict))
    luadecoded_additions = filecontent.split("-- end of stats\n\n")[1]
    f.close() 
    if update == True:
        return updateLuaDecoded(luadecoded_serialized, luadecoded_additions)
    else:
        return lua.decode(luadecoded_serialized)