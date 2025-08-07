import requests
import json
import pandas as pd

url = "https://api.sportradar.com/rugby-union/trial/v3/en/seasons.json"

headers = {
    "accept": "application/json",
    "x-api-key": ""
}

response = requests.get(url, headers=headers)
data = response.json()

# Assuming the seasons are in a list under the key 'seasons'
seasons = data.get('seasons', [])

# Convert to DataFrame
df = pd.DataFrame(seasons)

# Write to Excel
df.to_excel('seasons.xlsx', index=False)

print("Data written to seasons.xlsx")