import requests

url = "https://rugby.sportdevs.com/seasons-rounds"

payload={}
headers = {
  'Accept': 'application/json'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)