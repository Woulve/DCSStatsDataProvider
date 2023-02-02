from slpp import slpp as lua
from src.util.serverlogger import serverLogger
import os
from fastapi import HTTPException
from src.util.getConfigValue import getConfigValue
from src.components.luaparser.readfile import readfile
from src.components.luaparser.slmodstats.luaprocessor import process
from src.components.luaparser.slmodstats.processor.updateLuaDecoded import updateLuaDecoded

LOGGER = serverLogger()

def getLuaDecoded_slmodStats(filepath, update):
    filecontent = readfile(filepath)
    if filecontent == "":
        LOGGER.error("SlmodStats.lua is empty!")
        return None

    luadecoded_serialized = lua.decode("{"+filecontent.split("-- end of stats\n\n")[0]+"}")

    #The log file contains an array, and every event is appended to the file as a lua assignment. So we have to get the initial state here, and modify the dict for every line in the log file. Ugly, but it works.
    luadecoded_additions = filecontent.split("-- end of stats\n\n")[1]

    if update == True:
            updatedLua = updateLuaDecoded(luadecoded_serialized, luadecoded_additions)
            if updatedLua != '':
                LOGGER.debug("Successfully updated serialized lua")
                return process(updatedLua["stats"])
            else:
                LOGGER.error("Error updating serialized lua")
                return process(luadecoded_serialized["stats"])
    else:
        luadecoded_serialized = process(luadecoded_serialized["stats"])
        return luadecoded_serialized