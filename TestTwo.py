import requests
import pandas as pd
from time import sleep

API_KEY = ''
BASE_URL = 'https://api.sportradar.com/rugby-union/trial/v3/en/competitions'

# List of season IDs to loop through
SEASON_IDS = [
    "sr:season:4106",
    "sr:season:5892",
    "sr:season:7506",
    "sr:season:10261",
    "sr:season:33091",
    "sr:season:40469",
    "sr:season:53700",
    "sr:season:67631",
    "sr:season:79091",
    "sr:season:84120",
    "sr:season:95003",
    "sr:season:105251",
    "sr:season:119475",
    "sr:season:131539",
    "sr:season:130429"
]

def get_schedule(season_id):
    url = f"{BASE_URL}/seasons/{season_id}/schedules.json?api_key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 404:
        print(f"No schedule found for season {season_id}")
        print(url)
        return []
    response.raise_for_status()
    return response.json().get('sport_events', [])


def collect_all_matches():
    data = []
    for season_id in SEASON_IDS:
        print(f"Fetching season {season_id}")
        try:
            matches = get_schedule(season_id)
            for match in matches:
                match_info = {
                    'season_id': season_id,
                    'match_id': match['id'],
                    'date': match['start_time'],
                    'home_team': match['competitors'][0]['name'],
                    'away_team': match['competitors'][1]['name'],
                    'venue': match.get('venue', {}).get('name', 'N/A')
                }
                data.append(match_info)
            sleep(1)  # Avoid hitting rate limits
        except Exception as e:
            print(f"Error fetching season {season_id}: {e}")
    return pd.DataFrame(data)

if __name__ == '__main__':
    try:
        df = collect_all_matches()
        df.to_csv('rugby_championship_matches.csv', index=False)
        print("Data saved to rugby_championship_matches.csv")
    except Exception as e:
        print(f"Script failed: {e}")

    # Save season IDs to CSV
    df_season_ids = pd.DataFrame({'season_id': SEASON_IDS})
    df_season_ids.to_csv('season_ids.csv', index=False)
    print("Season IDs saved to season_ids.csv")