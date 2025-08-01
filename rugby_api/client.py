import requests
from Configuration import API_key

class SportradarRugbyClient:
    BASE_URL = "https://api.sportradar.com/rugby/trial/union/v3/en/competitions"

    def __init__(self, api_key=API_key):
        self.api_key = api_key

    def get_matches(self, competition_id, season_id):
    #    """
    #    Fetches matches for a given competition and season.
    #    """
        endpoint = f"/competitions/{competition_id}/seasons/{season_id}/schedules.json"
        url = f"{self.BASE_URL}{endpoint}"
        params = {"api_key": self.api_key}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    #def get_competitions(self):
    #    """
    #    Fetches all available competitions.
    #    """
    #    url = f"{self.BASE_URL}/competitions.json"
    #    params = {"api_key": self.api_key}
    #    response = requests.get(url, params=params)
    #    if response.status_code != 200:
    #        print("Error:", response.status_code, response.text)
    #    response.raise_for_status()
    #    return response.json()

    #def get_seasons_for_competition(self, competition_id):
    #    url = f"https://api.sportradar.com/rugby-union/trial/v3/en/competitions/{competition_id}/seasons.json"
    #    print(url)
    #    headers = {
    #        "accept": "application/json",
    #        "x-api-key": self.api_key
    #    }
    #    response = requests.get(url, headers=headers)
    #    response.raise_for_status()
    #    return response.json()


    # Add more methods as needed, e.g., get_teams, get_player_stats, etc.