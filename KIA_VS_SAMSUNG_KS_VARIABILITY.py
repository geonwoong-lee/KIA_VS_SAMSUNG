import math
import random
from tkinter import Tk, Label, Text, END

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

file_path = "regular_season_kia_samsung_score.xlsx"

df = pd.read_excel(file_path)

df['승리 팀'] = df.apply(lambda row: 1 if row['승리 팀'] == row['홈 팀'] else 0, axis=1)

X = df[['홈 팀 점수', '원정 팀 점수', '홈 팀 타율', '원정 팀 타율', '홈 팀 ERA', '원정 팀 ERA']]
y = df['승리 팀']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=200)

model = RandomForestClassifier(random_state=200)
model.fit(X_train, y_train)

kia_home = df[df['홈 팀'] == 'KIA']
kia_away = df[df['원정 팀'] == 'KIA']
samsung_home = df[df['홈 팀'] == '삼성']
samsung_away = df[df['원정 팀'] == '삼성']

def calculate_team_stats(home, away):
    return {
        'Average Home Score': home['홈 팀 점수'].mean(),
        'Average Away Score': away['원정 팀 점수'].mean(),
        'Average Home AVG': home['홈 팀 타율'].mean(),
        'Average Away AVG': away['원정 팀 타율'].mean(),
        'Average Home ERA': home['홈 팀 ERA'].mean(),
        'Average Away ERA': away['원정 팀 ERA'].mean(),
    }

kia_stats = calculate_team_stats(kia_home, kia_away)
samsung_stats = calculate_team_stats(samsung_home, samsung_away)

korea_series_games_updated = []
kia_wins = 0
samsung_wins = 0

for game_number in range(1, 8):
    if kia_wins == 4 or samsung_wins == 4:
        break

    if game_number in [1, 2, 5, 6, 7]:
        location = "Gwangju"
        home_team = "KIA"
        away_team = "Samsung"
        home_stats = kia_stats
        away_stats = samsung_stats
    else:
        location = "Daegu"
        home_team = "Samsung"
        away_team = "KIA"
        home_stats = samsung_stats
        away_stats = kia_stats

    kia_boost = random.uniform(-0.5, 1.0)
    samsung_boost = random.uniform(-1.0, 0.5)

    random_variation_home = random.uniform(-2, 3) + (kia_boost if home_team == "KIA" else samsung_boost)
    random_variation_away = random.uniform(-3, 2) + (kia_boost if away_team == "KIA" else samsung_boost)

    home_advantage_score = 1.5
    home_advantage_avg = 0.005
    home_advantage_era = -0.1

    game = {
        'Game Number': game_number,
        'Location': location,
        'Home Team': home_team,
        'Away Team': away_team,
        'Home Team Score': max(0, math.floor(home_stats['Average Home Score'] + random_variation_home + home_advantage_score)),
        'Away Team Score': max(0, math.floor(away_stats['Average Away Score'] + random_variation_away)),
        'Home Team AVG': round(home_stats['Average Home AVG'] + home_advantage_avg, 3),
        'Away Team AVG': round(away_stats['Average Away AVG'], 3),
        'Home Team ERA': round(home_stats['Average Home ERA'] + home_advantage_era, 2),
        'Away Team ERA': round(away_stats['Average Away ERA'], 2),
    }

    while game['Home Team Score'] == game['Away Team Score']:
        extra_innings_home = random.uniform(0, 3)
        extra_innings_away = random.uniform(0, 3)

        game['Home Team Score'] += math.ceil(extra_innings_home)
        game['Away Team Score'] += math.ceil(extra_innings_away)

    if game['Home Team Score'] > game['Away Team Score']:
        game['Prediction Result'] = "Home Team Wins"
        game['Winning Team'] = home_team
        if home_team == "KIA":
            kia_wins += 1
        else:
            samsung_wins += 1
    else:
        game['Prediction Result'] = "Away Team Wins"
        game['Winning Team'] = away_team
        if away_team == "KIA":
            kia_wins += 1
        else:
            samsung_wins += 1

    korea_series_games_updated.append(game)


korea_series_df_updated = pd.DataFrame(korea_series_games_updated)
final_winner = "KIA Tigers" if kia_wins > samsung_wins else "Samsung Lions"

def show_results_console(df, winner):
    print("\n=== Korean Series Prediction Results ===")
    if winner == "KIA Tigers":
        print(f"🎉 Congratulations on {winner}'s 12th victory! 🎉")
    else:
        print(f"🎉 Congratulations on {winner}'s 9th victory! 🎉")

    print("\n{:<5}{:<10}{:<10}{:<10}{:<10}{:<10}{:<8}{:<8}{:<8}{:<8}{:<10}".format(
        "Game", "Location", "Home", "Away",
        "H-Score", "A-Score", "H-AVG", "A-AVG",
        "H-ERA", "A-ERA", "Winner"
    ))
    print("-" * 85)

    for _, row in df.iterrows():
        print("{:<5}{:<10}{:<10}{:<10}{:<10}{:<10}{:<8.3f}{:<8.3f}{:<8.2f}{:<8.2f}{:<10}".format(
            row['Game Number'], row['Location'], row['Home Team'], row['Away Team'],
            row['Home Team Score'], row['Away Team Score'],
            row['Home Team AVG'], row['Away Team AVG'],
            row['Home Team ERA'], row['Away Team ERA'],
            row['Winning Team']
        ))

show_results_console(korea_series_df_updated, final_winner)

# Insert Actual Game Result
actual_results = {
    1: "KIA",
    2: "KIA",
    3: "Samsung",
    4: "KIA",
    5: "KIA"
}

korea_series_df_updated['Actual Winning Team'] = korea_series_df_updated['Game Number'].map(actual_results)

korea_series_df_updated['Prediction Correct'] = (
    korea_series_df_updated['Winning Team'] == korea_series_df_updated['Actual Winning Team']
)
accuracy = korea_series_df_updated['Prediction Correct'].mean() * 100

print(f"Prediction Accuracy: {accuracy:.2f}%")

print(korea_series_df_updated[['Game Number', 'Winning Team', 'Actual Winning Team', 'Prediction Correct']])
