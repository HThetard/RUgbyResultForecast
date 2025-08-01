from rugby_api.client import SportradarRugbyClient

client = SportradarRugbyClient()
season_id = "sr:season:131539"  # Example season ID
seasons = client.get_seasons_for_competition(season_id)
print(seasons)
