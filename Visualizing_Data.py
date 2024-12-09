import pandas as pd
import matplotlib.pyplot as plt

file_path = 'regular_season_kia_samsung_score.xlsx'
data = pd.ExcelFile(file_path)
df = data.parse('Sheet1')

df['Year'] = pd.to_datetime(df['날짜']).dt.year

kia_vs_samsung_stats = df.groupby(['Year', '홈 팀', '원정 팀']).agg(
    KIA_Wins=('승리 팀', lambda x: (x == 'KIA').sum()),
    Samsung_Wins=('승리 팀', lambda x: (x == '삼성').sum()),
    KIA_Batting_Avg=('홈 팀 타율', 'mean'),
    Samsung_Batting_Avg=('원정 팀 타율', 'mean'),
    KIA_ERA=('홈 팀 ERA', 'mean'),
    Samsung_ERA=('원정 팀 ERA', 'mean')
).reset_index()

kia_vs_samsung_stats = kia_vs_samsung_stats[
    ((kia_vs_samsung_stats['홈 팀'] == 'KIA') & (kia_vs_samsung_stats['원정 팀'] == '삼성')) |
    ((kia_vs_samsung_stats['홈 팀'] == '삼성') & (kia_vs_samsung_stats['원정 팀'] == 'KIA'))
]

yearly_stats = kia_vs_samsung_stats.groupby('Year').agg(
    KIA_Wins=('KIA_Wins', 'sum'),
    Samsung_Wins=('Samsung_Wins', 'sum'),
    KIA_Batting_Avg=('KIA_Batting_Avg', 'mean'),
    Samsung_Batting_Avg=('Samsung_Batting_Avg', 'mean'),
    KIA_ERA=('KIA_ERA', 'mean'),
    Samsung_ERA=('Samsung_ERA', 'mean')
).reset_index()

plt.figure(figsize=(8, 6))
plt.plot(yearly_stats['Year'], yearly_stats['KIA_Wins'], marker='o', label='KIA Wins', color = 'red')
plt.plot(yearly_stats['Year'], yearly_stats['Samsung_Wins'], marker='o', label='Samsung Wins', color = 'blue')
plt.title('KIA vs Samsung Yearly Wins')
plt.xlabel('Year')
plt.xticks(yearly_stats['Year'])
plt.ylabel('Wins')
plt.legend()
plt.grid()
plt.show()

plt.figure(figsize=(8, 6))
plt.plot(yearly_stats['Year'], yearly_stats['KIA_Batting_Avg'], marker='o', label='KIA Batting Average', color = 'red')
plt.plot(yearly_stats['Year'], yearly_stats['Samsung_Batting_Avg'], marker='o', label='Samsung Batting Average', color = 'blue')
plt.title('KIA vs Samsung Yearly Batting Average')
plt.xlabel('Year')
plt.xticks(yearly_stats['Year'])
plt.ylabel('Batting Average')
plt.legend()
plt.grid()
plt.show()

plt.figure(figsize=(8, 6))
plt.plot(yearly_stats['Year'], yearly_stats['KIA_ERA'], marker='o', label='KIA ERA', color = 'red')
plt.plot(yearly_stats['Year'], yearly_stats['Samsung_ERA'], marker='o', label='Samsung ERA', color = 'blue')
plt.title('KIA vs Samsung Yearly ERA')
plt.xlabel('Year')
plt.xticks(yearly_stats['Year'])
plt.ylabel('ERA')
plt.legend()
plt.grid()
plt.show()

