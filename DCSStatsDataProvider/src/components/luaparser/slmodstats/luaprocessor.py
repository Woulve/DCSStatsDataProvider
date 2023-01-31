from src.components.luaparser.slmodstats.processor.addTotalTimeProcessor import addTotalTime
from src.components.luaparser.slmodstats.processor.removeHostProcessor import removeHost
from src.components.luaparser.slmodstats.processor.addTotalPoints import addTotalPoints

def process(luadecoded):
    luadecoded = removeHost(luadecoded)
    luadecoded = addTotalTime(luadecoded)
    luadecoded = addTotalPoints(luadecoded)
    return luadecoded