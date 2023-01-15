
class TestMain:
    def inc(self, x):
        return x + 1
    def test_answer(self):
        assert self.inc(4) == 5, "4 + 1 equals 5"