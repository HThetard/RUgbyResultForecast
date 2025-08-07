import os
import glob
import json
import mysql.connector

# Path to your JSON files
json_folder = r"C:\Users\Hein\Documents\GitHub\RUgbyResultForecast"
json_pattern = os.path.join(json_folder, "sr_season_*_summary.json")
json_files = glob.glob(json_pattern)

# Check if the folder exists
if not json_files:
    print("No JSON files found.")
json_files = glob.glob(json_pattern)
print(f"Found {len(json_files)} files:")
for f in json_files:
    print(f"  - {f}")


# Connect to MySQL
conn = mysql.connector.connect(
    host='',
    user='',
    password=''
)
cursor = conn.cursor()

# Create and use rugby schema
cursor.execute("CREATE DATABASE IF NOT EXISTS rugby")
cursor.execute("USE rugby")

# (Re)create all necessary tables (same as in previous script — shortened here for clarity)
# ... Add the same table creation code from previous script here ...

# Helper: process a single JSON file
def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for summary in data.get("summaries", []):
        event = summary["sport_event"]
        context = event["sport_event_context"]
        status = summary["sport_event_status"]
        competitors = event["competitors"]

        # Insert competition
        competition = context["competition"]
        cursor.execute("""
            INSERT IGNORE INTO competitions (id, name, gender)
            VALUES (%s, %s, %s)
        """, (competition["id"], competition["name"], competition.get("gender")))

        # Insert season
        season = context["season"]
        cursor.execute("""
            INSERT IGNORE INTO seasons (id, name, start_date, end_date, year, competition_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            season["id"], season["name"], season["start_date"],
            season["end_date"], season["year"], season["competition_id"]
        ))

        # Insert sport_event
        cursor.execute("""
            INSERT IGNORE INTO sport_events
            (id, start_time, start_time_confirmed, season_id, stage_type, stage_phase,
             stage_start_date, stage_end_date, round_number, group_id, group_name)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            event["id"], event["start_time"], event["start_time_confirmed"],
            season["id"], context["stage"]["type"], context["stage"]["phase"],
            context["stage"]["start_date"], context["stage"]["end_date"],
            context["round"]["number"],
            context["groups"][0]["id"], context["groups"][0]["name"]
        ))

        # Insert competitors and their event relation
        for comp in competitors:
            cursor.execute("""
                INSERT IGNORE INTO competitors (id, name, country, country_code, abbreviation, gender)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                comp["id"], comp["name"], comp["country"],
                comp["country_code"], comp["abbreviation"], comp["gender"]
            ))

            cursor.execute("""
                INSERT IGNORE INTO event_competitors (sport_event_id, competitor_id, qualifier)
                VALUES (%s, %s, %s)
            """, (event["id"], comp["id"], comp["qualifier"]))

        # Insert event status
        cursor.execute("""
            INSERT IGNORE INTO sport_event_status
            (sport_event_id, status, match_status, home_score, away_score, winner_id, match_tie)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            event["id"],
            status.get("status"),
            status.get("match_status"),  # Use .get() instead of []
            status.get("home_score"),
            status.get("away_score"),
            status.get("winner_id"),
            status.get("match_tie", False)
        ))

        # Insert period scores
        for period in status.get("period_scores", []):
            cursor.execute("""
                INSERT INTO period_scores (sport_event_id, home_score, away_score, type, number)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                event["id"], period["home_score"], period["away_score"],
                period["type"], period["number"]
            ))

# Step through and import all matching files
for json_file in json_files:
    print(f"Importing {json_file}...")
    process_file(json_file)

# Commit changes and close connection
conn.commit()
cursor.close()
conn.close()
print("All JSON files successfully imported into the 'rugby' schema.")
