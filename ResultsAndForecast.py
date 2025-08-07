import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import numpy as np
import dataframe_image as dfi
import matplotlib.colors as mcolors

# Connect to MySQL
conn = mysql.connector.connect(
    host='',
    user='',
    password='',
    database='rugby'
)

# Query to get match results with teams and year
query = """
SELECT
    se.id AS sport_event_id,
    s.year,
    c1.name AS home_team,
    c2.name AS away_team,
    ses.home_score,
    ses.away_score
FROM sport_events se
JOIN seasons s ON se.season_id = s.id
JOIN event_competitors ec1 ON se.id = ec1.sport_event_id AND ec1.qualifier = 'home'
JOIN event_competitors ec2 ON se.id = ec2.sport_event_id AND ec2.qualifier = 'away'
JOIN competitors c1 ON ec1.competitor_id = c1.id
JOIN competitors c2 ON ec2.competitor_id = c2.id
JOIN sport_event_status ses ON se.id = ses.sport_event_id
WHERE ses.home_score IS NOT NULL AND ses.away_score IS NOT NULL AND s.year >= 2016
"""

df = pd.read_sql(query, conn)

# Add result columns
def get_result(row, team, is_home):
    if row['home_score'] > row['away_score']:
        return 'win' if is_home else 'loss'
    elif row['home_score'] < row['away_score']:
        return 'loss' if is_home else 'win'
    else:
        return 'draw'

records = []
for _, row in df.iterrows():
    # Home team
    records.append({
        'team': row['home_team'],
        'year': row['year'],
        'result': get_result(row, row['home_team'], True)
    })
    # Away team
    records.append({
        'team': row['away_team'],
        'year': row['year'],
        'result': get_result(row, row['away_team'], False)
    })

results_df = pd.DataFrame(records)

# Aggregate
summary = results_df.groupby(['team', 'year', 'result']).size().unstack(fill_value=0).reset_index()

# Plot for all teams, each in a separate graph
for team_name in summary['team'].unique():
    team_data = summary[summary['team'] == team_name].set_index('year')[['win', 'loss', 'draw']]
    team_data.plot(kind='bar', stacked=True, figsize=(10,6))
    plt.title(f'Win/Loss/Draw per Year for {team_name}')
    plt.ylabel('Number of Matches')
    plt.xlabel('Year')
    plt.tight_layout()
    plt.savefig(f"{team_name}_win_loss_draw.png")
    plt.close()

# 1. Assign exponential weights to each season (most recent = highest, much more than oldest)
base = 2  # You can try 1.5, 2, 3, etc. for more/less steepness
all_years = sorted(summary['year'].unique())
weights = {year: base ** i for i, year in enumerate(all_years)}  # Oldest=base^0, Newest=base^n

# 2. Calculate weighted wins per team
summary['weight'] = summary['year'].map(weights)
summary['weighted_wins'] = summary['win'] * summary['weight']

# 3. Aggregate weighted wins per team
team_weighted_wins = summary.groupby('team')['weighted_wins'].sum()

# 4. Calculate probabilities
total_weighted_wins = team_weighted_wins.sum()
probabilities = (team_weighted_wins / total_weighted_wins) * 100

# 5. Plot as pie chart
plt.figure(figsize=(8,8))
plt.pie(probabilities, labels=probabilities.index, autopct='%1.1f%%', startangle=140)
plt.title('Forecasted Probability of Winning the Rugby Championship\n(Exponentially Weighted by Recent Performance)')
plt.tight_layout()
plt.savefig("forecast_pie_chart.png")  # <-- Save the pie chart as an image
#plt.show()



# List of teams to plot
teams_to_plot = ['New Zealand','South Africa', 'Argentina', 'Australia']

fig, axes = plt.subplots(2, 2, figsize=(18, 12), sharex=True)

for ax, team_name in zip(axes.flatten(), teams_to_plot):
    team_data = summary[summary['team'] == team_name].set_index('year')[['win', 'loss', 'draw']]
    team_data = team_data.reindex(sorted(summary['year'].unique()), fill_value=0)
    bars = team_data.plot(kind='bar', stacked=True, ax=ax, legend=False)
    ax.set_title(f'Win/Loss/Draw per Year for {team_name}', fontsize=26)  # <-- doubled font size
    ax.set_ylabel('Number of Matches', fontsize=20)
    ax.set_xlabel('Year', fontsize=20)
    legend = ax.legend(['Win', 'Loss', 'Draw'], loc='lower right', prop={'size': 24})  # <-- doubled font size

    # Increase y-axis limit for visibility
    max_total = team_data.sum(axis=1).max()
    ax.set_ylim(0, max_total + 1)

    # Add win percentage above each column
    for idx, year in enumerate(team_data.index):
        total = team_data.loc[year].sum()
        win = team_data.loc[year, 'win']
        if total > 0:
            percent = win / total * 100
            ax.text(idx, total + 0.2, f'{percent:.1f}%', ha='center', va='bottom', fontsize=16, fontweight='bold')

plt.tight_layout()
plt.savefig("win_loss_draw_four_panel.png")
#plt.show()

# Query for all scheduled 2025 matches (even if not played yet)
query_2025 = """
SELECT
    se.id AS sport_event_id,
    s.year,
    c1.name AS home_team,
    c2.name AS away_team,
    se.start_time
FROM sport_events se
JOIN seasons s ON se.season_id = s.id
JOIN event_competitors ec1 ON se.id = ec1.sport_event_id AND ec1.qualifier = 'home'
JOIN event_competitors ec2 ON se.id = ec2.sport_event_id AND ec2.qualifier = 'away'
JOIN competitors c1 ON ec1.competitor_id = c1.id
JOIN competitors c2 ON ec2.competitor_id = c2.id
WHERE s.year = 2025
"""

games_2025 = pd.read_sql(query_2025, conn)

# 2. Format the date as 'mmmm-dd'
games_2025['Date'] = pd.to_datetime(games_2025['start_time']).dt.strftime('%B-%d')

# Calculate team strengths and draw probability for 2025 forecast
recent_years = [2023, 2024]
recent_summary = summary[summary['year'].isin(recent_years)].copy()
weights = {2023: 1, 2024: 3}
recent_summary['weight'] = recent_summary['year'].map(weights)
recent_summary['weighted_wins'] = recent_summary['win'] * recent_summary['weight']
team_strength = recent_summary.groupby('team')['weighted_wins'].sum()
team_strength = team_strength.replace(0, 1)  # Avoid division by zero

# Calculate historical draw probability from recent years
total_games = recent_summary[['win', 'loss', 'draw']].sum().sum()
total_draws = recent_summary['draw'].sum()
historical_draw_prob = total_draws / total_games if total_games > 0 else 0.1

# 3. When building prob_rows, include the date
prob_rows = []
for _, row in games_2025.iterrows():
    home = row['home_team']
    away = row['away_team']
    date = row['Date']
    home_strength = team_strength.get(home, 1) * 1.2  # 20% home weighting
    away_strength = team_strength.get(away, 1)
    total_strength = home_strength + away_strength

    draw_prob = historical_draw_prob
    home_win_prob = (home_strength / total_strength) * (1 - draw_prob)
    away_win_prob = (away_strength / total_strength) * (1 - draw_prob)

    prob_rows.append({
        'Date': date,
        'Home Team': home,
        'Away Team': away,
        'Home Win %': round(home_win_prob * 100),
        'Away Win %': round(away_win_prob * 100)
    })

prob_df = pd.DataFrame(prob_rows)

# 4. Remove the DataFrame index from the image
styled = prob_df.style.background_gradient(
    subset=['Home Win %', 'Away Win %'],
    cmap=mcolors.LinearSegmentedColormap.from_list("winloss", ["red", "yellow", "green"])
)

dfi.export(styled.hide(axis="index"), '2025_match_probabilities_colored.png')
print("Saved 2025_match_probabilities_colored.png")

# Optionally, also print or save as CSV
print(prob_df)
prob_df.to_csv('2025_match_probabilities.csv', index=False)

