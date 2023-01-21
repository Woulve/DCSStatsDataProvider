from src.components.luaparser.processor.addTotalTimeProcessor import addTotalTime
from src.components.luaparser.processor.removeHostProcessor import removeHost
from src.components.luaparser.processor.addTotalKills import addTotalKills

def process(luadecoded):
    luadecoded = removeHost(luadecoded)
    luadecoded = addTotalTime(luadecoded)
    luadecoded = addTotalKills(luadecoded)
    return luadecoded