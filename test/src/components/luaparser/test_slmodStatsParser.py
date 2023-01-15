from src.components.luaparser.slmodStatsParser import getLuaDecoded_slmodStats
import logging
import json

LOGGER = logging.getLogger(__name__)
# import unittest

# class test_slmodStatsParser(unittest.TestCase):
#     def test_json(self):
#         self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
#         print("json!")

class TestSLModStatsParser:
    def returns_valid_json(self, json_text):
        try:
            json.loads(json_text)
        except ValueError as err:
            return False
        return True
    def test_returns_valid_json(self):
        assert self.returns_valid_json(json.dumps(getLuaDecoded_slmodStats(False))) == True, "Returns valid JSON"
