from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestGetRoot:
    def test_get_root(self):
        response = client.get("/", headers={"h9vQ$GYw4v2Z#D": "d%xnC68H*F6!iF"})
        assert response.status_code == 200
        assert list(response.json().keys())[0] == "stats" #contains stats
        assert len(list(response.json()["stats"].keys())) > 0 #stats object is not empty

class TestGetPlayers:
    def test_get_players(self):
        response = client.get("/players", headers={"h9vQ$GYw4v2Z#D": "d%xnC68H*F6!iF"})
        assert response.status_code == 200
        assert list(response.json().keys())[0] == "players" #contains players
        assert len(list(response.json()["players"])) > 0 #players array is not empty

    def test_get_players_debugdata(self):
        response = client.get("/players", headers={"debug": "true", "h9vQ$GYw4v2Z#D": "d%xnC68H*F6!iF"})
        assert response.status_code == 200
        assert list(response.json().keys())[0] == "players"
        assert len(list(response.json()["players"])) == 54

class TestGetPlayer:
    def test_get_player_debugdata(self):
        response = client.get("/player/woulve", headers={"debug": "true", "h9vQ$GYw4v2Z#D": "d%xnC68H*F6!iF"})
        assert response.status_code == 200
        assert list(response.json().keys())[0] == "player" #contains player
        assert len(list(response.json()["player"])) > 0 #player object is not empty
        assert response.json()["player"]["ucid"] == "winnerbypoints"

class TestGetPlayerByName:
    def test_get_player_by_name_debugdata(self):
        response = client.get("/playerbyname/woulve", headers={"debug": "true", "h9vQ$GYw4v2Z#D": "d%xnC68H*F6!iF"})
        assert response.status_code == 200
        # print(response.json())
        assert response.json()["UCID"] == "winnerbypoints"
    def test_get_player_by_name_notfound_debugdata(self):
        response = client.get("/playerbyname/yyyyyyy", headers={"debug": "true", "h9vQ$GYw4v2Z#D": "d%xnC68H*F6!iF"})
        assert response.status_code == 404

class TestGetPlayerRankingByFlightTime:
    def test_get_player_ranking_by_flight_time(self):
        response = client.get("/playerrankingbyflighttime", headers={"h9vQ$GYw4v2Z#D": "d%xnC68H*F6!iF"})
        assert response.status_code == 200
        assert list(response.json().keys())[0] == "flighttimeranking" #contains flighttimeranking
        assert len(list(response.json()["flighttimeranking"])) > 0 #flighttimeranking array is not empty

    def test_get_player_ranking_by_flight_time_debugdata(self):
        response = client.get("/playerrankingbyflighttime", headers={"debug": "true", "h9vQ$GYw4v2Z#D": "d%xnC68H*F6!iF"})
        assert response.status_code == 200
        assert list(response.json().keys())[0] == "flighttimeranking" #contains flighttimeranking
        assert len(list(response.json()["flighttimeranking"])) > 0 #flighttimeranking array is not empty
        assert list(response.json()["flighttimeranking"])[0][0] == "Woulve" #first player is woulve

class TestGetPlayerRankingByPoints:
    def test_get_player_ranking_by_points(self):
        response = client.get("/playerrankingbypoints", headers={"h9vQ$GYw4v2Z#D": "d%xnC68H*F6!iF"})
        assert response.status_code == 200
        assert list(response.json().keys())[0] == "pointranking" #contains pointranking
        assert len(list(response.json()["pointranking"])) > 0 #pointranking array is not empty

    def test_get_player_ranking_by_points_debugdata(self):
        response = client.get("/playerrankingbypoints", headers={"debug": "true","h9vQ$GYw4v2Z#D": "d%xnC68H*F6!iF"})
        assert response.status_code == 200
        assert list(response.json().keys())[0] == "pointranking" #contains pointranking
        assert len(list(response.json()["pointranking"])) > 0 #pointranking array is not empty
        assert list(response.json()["pointranking"])[0][0] == "Woulve" #first player is woulve

class TestGetAllPlayerStats:
    def test_get_all_player_stats(self):
        response = client.get("/allplayerstats", headers={"h9vQ$GYw4v2Z#D": "d%xnC68H*F6!iF"})
        assert response.status_code == 200
        assert list(response.json().keys())[0] == "allplayerstats" #contains allplayerstats
        assert len(list(response.json()["allplayerstats"])) > 0 #allplayerstats array is not empty

    def test_get_all_player_stats_debugdata(self):
        response = client.get("/allplayerstats", headers={"debug": "true", "h9vQ$GYw4v2Z#D": "d%xnC68H*F6!iF"})
        assert response.status_code == 200
        assert list(response.json().keys())[0] == "allplayerstats" #contains allplayerstats
        assert len(list(response.json()["allplayerstats"])) > 0 #allplayerstats array is not empty
        assert list(response.json()["allplayerstats"])[0][0] == "Woulve" #first player is woulve