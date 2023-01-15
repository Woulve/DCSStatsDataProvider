from slpp import slpp as lua
from src.util.serverlogger import serverLogger
import os
from src.components.luaparser.luaprocessor import process
from src.components.luaparser.processor.updateLuaDecoded import updateLuaDecoded

LOGGER = serverLogger()


def getLuaDecoded_slmodStats(update):
    file_path = "./SlmodStats.lua"

    if not os.path.isfile(file_path):
        return None
    try:
        f = open(file_path, "r")
    except:
        return None
    filecontent = f.read()
    f.close() 
    if filecontent == "":
        return None

    luadecoded_serialized = lua.decode("{"+filecontent.split("-- end of stats\n\n")[0]+"}")

    #The log file contains an array, and every event is appended to the file as a lua assignment. So we have to get the initial state here, and modify the dict for every line in the log file. Ugly, but it works.
    luadecoded_additions = filecontent.split("-- end of stats\n\n")[1]

    if update == True:
            updatedLua = updateLuaDecoded(luadecoded_serialized, luadecoded_additions)
            if updatedLua != '':
                LOGGER.info("Successfully updated serialized lua")
                return process(updatedLua)
            else:
                LOGGER.error("!!!!Error updating serialized lua!!!!")
                return process(luadecoded_serialized)
    else:
        luadecoded_serialized = process(luadecoded_serialized)
        return luadecoded_serialized