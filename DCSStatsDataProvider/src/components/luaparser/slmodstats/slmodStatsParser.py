from slpp import slpp as lua
from src.util.serverlogger import serverLogger
import os
from fastapi import HTTPException
from src.util.getConfigValue import getConfigValue
from src.components.luaparser.slmodstats.luaprocessor import process
from src.components.luaparser.slmodstats.processor.updateLuaDecoded import updateLuaDecoded

LOGGER = serverLogger()


def getLuaDecoded_slmodStats(update):
    file_path = getConfigValue("localfiles", "slmodstatsluapath")

    if not os.path.isfile(file_path):
        LOGGER.error(file_path + " not found")
        raise HTTPException(status_code=500)
    try:
        f = open(file_path, "r")
    except Exception as e:
        LOGGER.exception(e)
        raise HTTPException(status_code=500)
    filecontent = f.read()

    f.close()
    if filecontent == "":
        LOGGER.error("./SlmodStats.lua is empty!")
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
                LOGGER.error("Error updating serialized lua")
                return process(luadecoded_serialized)
    else:
        luadecoded_serialized = process(luadecoded_serialized)
        return luadecoded_serialized