import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt

# Connect to MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Hein5024!@',
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
WHERE ses.home_score IS NOT NULL AND ses.away_score IS NOT NULL
"""

df = pd.read_sql(query, conn)
conn.close()

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
print(summary)

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
plt.show()

