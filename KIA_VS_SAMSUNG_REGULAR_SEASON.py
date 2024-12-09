from tkinter import Tk, Label, Text, END

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

file_path = "regular_season_kia_samsung_score.xlsx"

df = pd.read_excel(file_path)

X = df[['홈 팀 타율', '원정 팀 타율', '홈 팀 ERA', '원정 팀 ERA']]
y_home = df['홈 팀 점수']
y_away = df['원정 팀 점수']
y_score_diff = df['홈 팀 점수'] - df['원정 팀 점수']

X_train, X_test, y_train_home, y_test_home = train_test_split(X, y_home, test_size=0.2, random_state=42)
_, _, y_train_away, y_test_away = train_test_split(X, y_away, test_size=0.2, random_state=42)
_, _, y_train_diff, y_test_diff = train_test_split(X, y_score_diff, test_size=0.2, random_state=42)

home_model = RandomForestRegressor(random_state=50)
away_model = RandomForestRegressor(random_state=50)
diff_model = RandomForestRegressor(random_state=50)

home_model.fit(X_train, y_train_home)
away_model.fit(X_train, y_train_away)
diff_model.fit(X_train, y_train_diff)

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
        home_input = {
            '홈 팀 타율': kia_stats['Average Home AVG'],
            '원정 팀 타율': samsung_stats['Average Away AVG'],
            '홈 팀 ERA': kia_stats['Average Home ERA'],
            '원정 팀 ERA': samsung_stats['Average Away ERA'],
        }
    else:
        location = "Daegu"
        home_team = "Samsung"
        away_team = "KIA"
        home_input = {
            '홈 팀 타율': samsung_stats['Average Home AVG'],
            '원정 팀 타율': kia_stats['Average Away AVG'],
            '홈 팀 ERA': samsung_stats['Average Home ERA'],
            '원정 팀 ERA': kia_stats['Average Away ERA'],
        }

    home_input_df = pd.DataFrame([home_input])

    predicted_home_score = home_model.predict(home_input_df)[0]
    predicted_away_score = away_model.predict(home_input_df)[0]
    predicted_score_diff = diff_model.predict(home_input_df)[0]

    if predicted_home_score > predicted_away_score:
        winning_team = home_team
        kia_wins += 1 if home_team == "KIA" else 0
        samsung_wins += 1 if home_team == "Samsung" else 0
    else:
        winning_team = away_team
        kia_wins += 1 if away_team == "KIA" else 0
        samsung_wins += 1 if away_team == "Samsung" else 0

    korea_series_games_updated.append({
        'Game Number': game_number,
        'Location': location,
        'Home Team': home_team,
        'Away Team': away_team,
        'Predicted Home Score': round(predicted_home_score, 1),
        'Predicted Away Score': round(predicted_away_score, 1),
        'Score Difference': round(predicted_score_diff, 1),
        'Winning Team': winning_team
    })

korea_series_df_updated = pd.DataFrame(korea_series_games_updated)
final_winner = "KIA Tigers" if kia_wins > samsung_wins else "Samsung Lions"

def show_results_window(df, winner):
    root = Tk()
    root.title("2024 Korean Series Prediction Results")
    root.geometry("1000x500")

    Label(root, text=f"🎉 Congratulations to {winner}! 🎉", font=("Arial", 16, "bold"), fg="blue").pack(pady=10)

    text = Text(root, wrap="none", font=("Courier", 11))
    text.pack(fill="both", expand=True)

    header = "{:<5}{:<10}{:<10}{:<10}{:<12}{:<12}{:<12}{:<12}\n".format(
        "Game", "Location", "Home", "Away",
        "H-Score", "A-Score", "Score Diff", "Winner"
    )
    text.insert(END, header)
    text.insert(END, "-" * 80 + "\n")

    for _, row in df.iterrows():
        line = "{:<5}{:<10}{:<10}{:<10}{:<12.1f}{:<12.1f}{:<12.1f}{:<12}\n".format(
            row['Game Number'], row['Location'], row['Home Team'], row['Away Team'],
            row['Predicted Home Score'], row['Predicted Away Score'],
            row['Score Difference'], row['Winning Team']
        )
        text.insert(END, line)

    root.mainloop()

show_results_window(korea_series_df_updated, final_winner)
