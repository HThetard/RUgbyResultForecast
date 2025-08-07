import requests
import time

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
    "accept": "application/xml",
    "x-api-key": API_KEY
}

for season_id in SEASON_IDS:
    url = f"{BASE_URL}/{season_id}/summaries.json"
    print(f"Fetching: {url}")
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        filename = f"{season_id.replace(':', '_')}_summary.json"
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"Saved {filename}")
    else:
        print(f"Error for {season_id}: {response.status_code} - {response.text}")
    time.sleep(10)  # Wait 10 seconds between requests