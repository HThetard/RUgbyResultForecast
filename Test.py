import requests
import pandas as pd
from time import sleep

# ⚠️ Replace this with your actual API key
API_KEY = 'YK0FXF4QPWAdldOz0vzypPzSEvTEVfDtCubkL3hN'

# ✅ Use the correct base URL for v3
BASE_URL = 'https://api.sportradar.com/rugby-union/trial/v3/en/'
#https://api.sportradar.com/rugby-union/trial/v3/en/competitions/sr:season:33091/seasons.json
# ✅ Replace with correct competition ID — this ID is a placeholder
COMPETITION_ID = 'sr:competition:789'

# Define which seasons you want (years 2010–2025)
YEARS = [str(year) for year in range(2010, 2026)]
print(YEARS)
# ------------------ Function: Get All Seasons for Competition ------------------
def get_seasons():
    url = f"{BASE_URL}/competitions/{COMPETITION_ID}/seasons.json?api_key={API_KEY}"
    #print(url)
    response = requests.get(url)
    if response.status_code == 403:
        raise Exception("Forbidden: Check your API key and access to Rugby v3.")
    response.raise_for_status()
    return response.json()['seasons']

# ------------------ Function: Get Schedule for a Given Season ------------------
def get_schedule(season_id):
    url = f"{BASE_URL}/seasons/{season_id}/schedules.json?api_key={API_KEY}"
    #print(url)
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

# ------------------ Function: Loop Through All Seasons and Collect Matches ------------------
def collect_all_matches():
    data = []
    seasons = get_seasons()
    for season in seasons:
        start_year = season['start_date'][:4]
        if start_year in YEARS:
            print(f"Fetching season {start_year}")
            season_id = season['id']
            try:
                schedule = get_schedule(season_id)
                for match in schedule.get('sport_events', []):
                    match_info = {
                        'season': start_year,
                        'match_id': match['id'],
                        'date': match['start_time'],
                        'home_team': match['competitors'][0]['name'],
                        'away_team': match['competitors'][1]['name'],
                        'venue': match.get('venue', {}).get('name', 'N/A')
                    }
                    data.append(match_info)
                sleep(1)  # Avoid hitting rate limits
            except Exception as e:
                print(f"Error fetching season {start_year}: {e}")
    return pd.DataFrame(data)

# ------------------ Run Everything ------------------
if __name__ == '__main__':
    try:
        df = collect_all_matches()
        df.to_csv('rugby_championship_matches.csv', index=False)
        print("Data saved to rugby_championship_matches.csv")
    except Exception as e:
        print(f"Script failed: {e}")
