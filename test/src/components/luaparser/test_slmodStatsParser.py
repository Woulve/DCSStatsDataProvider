from src.components.luaparser.slmodStatsParser import getLuaDecoded_slmodStats
from src.util.serverlogger import serverLogger
import json

LOGGER = serverLogger()

class TestSLModStatsParser:
    def returns_valid_json(self, json_text):
        try:
            json.loads(json_text)
        except ValueError as err:
            return False
        return True
    def test_returns_valid_json(self):
        assert self.returns_valid_json(json.dumps(getLuaDecoded_slmodStats(False))) == True, "Returns valid JSON"
