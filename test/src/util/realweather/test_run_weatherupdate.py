import os
from src.util.realweather.run_weatherupdate import over_12_hours, check_if_weather_update_is_needed, update_miz_weather

class TestRunWeatherupdate:


    def test_over_12_hours(self):
        assert over_12_hours("01/01/2022 00:00:00", "01/01/2022 13:00:00") == True, "over_12_hours"
        assert over_12_hours("01/01/2022 00:00:00", "01/01/2022 11:00:00") == False, "under_12_hours"


