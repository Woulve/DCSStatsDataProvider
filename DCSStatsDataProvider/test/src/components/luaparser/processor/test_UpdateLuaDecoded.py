from src.components.luaparser.processor.updateLuaDecoded import convert_lua_notation_to_python

testLua = 'stats["ef202237873822643b1f533fc865a353"]["times"]["F-14B"]["total"] = "hehe"'

class TestupdateLuaDecoded:
    def testconvert_lua_notation_to_python(self):
        teststrings = [
            'stats["ef202237873822643b1f533fc865a353"]["times"]["F-14B"]["total"] = "Test"',
            'stats["ef202237873822643b1f533fc865a353"]["times"]["F-14B"]["total"] = 20.018',
            'stats["ef202237873822643b1f533fc865a353"]["times"]["F-14B"]["total"] = nil',
            'stats["a2d915b3ef39e46672b972e33fbe2343"] = { }',
            'stats["a2d915b3ef39e46672b972e33fbe2343"]["times"]["Su-25T"] = { ["total"] = 0, ["inAir"] = 0, }',
            'stats["a2d915b3ef39e46672b972e33fbe2343"]["times"]["Su-25T"] = 1',
        ]
        assert str(convert_lua_notation_to_python(teststrings[0])) == "{\'stats\': {\'ef202237873822643b1f533fc865a353\': {\'times\': {\'F-14B\': {\'total\': \'Test\'}}}}}", "decodeLua 0 matches"
        assert str(convert_lua_notation_to_python(teststrings[1])) == "{\'stats\': {\'ef202237873822643b1f533fc865a353\': {\'times\': {\'F-14B\': {\'total\': 20.018}}}}}", "decodeLua 1 matches"
        assert str(convert_lua_notation_to_python(teststrings[2])) == "{\'stats\': {\'ef202237873822643b1f533fc865a353\': {\'times\': {\'F-14B\': {\'total\': None}}}}}", "decodeLua 2 matches"
        assert str(convert_lua_notation_to_python(teststrings[3])) == "{\'stats\': {\'a2d915b3ef39e46672b972e33fbe2343\': {}}}", "decodeLua 3 matches"
        assert str(convert_lua_notation_to_python(teststrings[4])) == "{\'stats\': {\'a2d915b3ef39e46672b972e33fbe2343\': {\'times\': {\'Su-25T\': {\'total\': 0, \'inAir\': 0}}}}}", "decodeLua 4 matches"
