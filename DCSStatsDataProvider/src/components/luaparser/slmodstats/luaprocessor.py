from src.components.luaparser.slmodstats.processor.addTotalTimeProcessor import addTotalTime
from src.components.luaparser.slmodstats.processor.removeHostProcessor import removeHost
from src.components.luaparser.slmodstats.processor.addTotalKills import addTotalKills

def process(luadecoded):
    luadecoded = removeHost(luadecoded)
    luadecoded = addTotalTime(luadecoded)
    luadecoded = addTotalKills(luadecoded)
    return luadecoded