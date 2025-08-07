import requests
import pandas as pd
import time
from collections.abc import MutableMapping

API_KEY = ""
BASE_URL = "https://api.sportradar.com/rugby-union/trial/v3/en/seasons"

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
    "sr:season:131539"
]

headers = {
    "accept": "application/json",
    "x-api-key": API_KEY
}

def flatten(d, parent_key='', sep='.'):
    """Recursively flattens a nested dictionary."""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            # Convert lists to string or flatten if list of dicts
            if v and isinstance(v[0], dict):
                for idx, item in enumerate(v):
                    items.extend(flatten(item, f"{new_key}[{idx}]", sep=sep).items())
            else:
                items.append((new_key, str(v)))
        else:
            items.append((new_key, v))
    return dict(items)

all_data = []

for season_id in SEASON_IDS:
    url = f"{BASE_URL}/{season_id}/summaries.json"
    print(f"Fetching: {url}")
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        flat = flatten(data)
        flat["season_id"] = season_id  # Always include the season_id
        all_data.append(flat)
    else:
        print(f"Error for {season_id}: {response.status_code} - {response.text}")
    time.sleep(10)  # Wait 10 seconds between requests

# Write to Excel
df = pd.DataFrame(all_data)
df.to_excel("season_summaries_full.xlsx", index=False)
print("Data written to season_summaries_full.xlsx")