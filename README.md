# Who will win the Korean Series?

---

![koreanseries2.jpg](imgs%2Fkoreanseries2.jpg)

[Image Source](https://www.wbsc.org/ko/news/kia-tigers-and-samsung-lions-to-compete-in-korean-series-2024)

---

# Korean Series Prediction

## KIA Tigers vs. Samsung Lions

This project simulates the outcomes of a hypothetical Korean Series between the **KIA Tigers** and **Samsung Lions** using historical regular-season data, machine learning predictions, and additional considerations for Korean Series-specific dynamics.

---

## 📊 Project Overview
![koreanseries.png](imgs%2Fkoreanseries.png)

1. **Data Visualization**: Analyzed and visualized the head-to-head records between KIA and Samsung during the 2021-2024 regular seasons.
2. **Regular Season Regression Analysis**: Used regular season data to predict game score differences and identify the winning team.
3. **Korean Series Variability Model**: Enhanced predictions by accounting for Korean Series-specific dynamics (e.g., home advantage, KIA's strengths, Samsung's challenges).

---

## 📈 Head-to-Head Visualization

### **1. Yearly Wins**
![Yearly Wins](yearly_wins.jpg)

- A graph comparing yearly win counts for **KIA** and **Samsung**.
  - Since 2023, KIA's win count has increased significantly, while Samsung has been on a declining trend.

### **2. Yearly Batting Averages**
![Yearly Batting Average](yearly_avg.jpg)

- A comparison of average batting averages for both teams, including home and away games.
  - KIA's batting average saw a sharp rise in 2024.

### **3. Yearly ERA (Earned Run Average)**
![Yearly ERA](yearly_era.jpg)

- A graph comparing the teams' yearly ERAs.
  - KIA's ERA has consistently improved, showcasing better pitching, while Samsung's ERA has worsened.

---

## 🧮 Regular Season Regression Analysis

The `KIA_VS_SAMSUNG_REGULAR_SEASON.py` file performs **regression analysis** based on regular season data.

- **Algorithm** :
  - **Random Forest Regressor** to predict the home/away team scores and determine the winner based on score differences.
- **Input Data** :
  - Used regular-season data from 2021 to 2024.
  - Features: Home/Away Batting Averages, ERAs.
- **Results** :
  - The model predicted Samsung as the winner based on data from 2021 to 2024.
  - However, 2024-specific head-to-head data showed **KIA leading 12 wins to 4 losses** against Samsung. Due to limited 2024 data, predictions included data from 2021 to 2024.
  - Predictions are as follows:

![prediction_regression.jpg](imgs%2Fprediction_regression.jpg)

---

## ⚾ Korean Series Variability Model

The `KIA_VS_SAMSUNG_KS_VARIABILITY.py` file introduces a **variability model** specific to the Korean Series.

### **Model Explanation**
- **Random Forest Classifier** : Used to classify the winning team based on regular-season data.
- **Korean Series Specific Factors** :
  1. **KIA Tigers' Strengths** :
     - KIA has a track record of **11 appearances and 11 championships in the Korean Series**, making them a dominant force.
       - Code: `kia_boost = random.uniform(-0.5, 1.0)`
       - This gives KIA a performance boost in the model.
  2. **Samsung Lions' Challenges** :
     - The absence of key player **Koo Ja-wook** is modeled to weaken Samsung's batting performance.
       - Code: `samsung_boost = random.uniform(-1.0, 0.5)`
  3. **Home Advantage** :
     - Home games increase batting averages and scores while decreasing ERA due to the support of home fans.
       - Code: 
         ```python
         random_variation_home = random.uniform(-2, 3) + (kia_boost if home_team == "KIA" else samsung_boost)
         random_variation_away = random.uniform(-3, 2) + (kia_boost if away_team == "KIA" else samsung_boost)
         ```
     - Home team performance is adjusted with random variability.

### **Results**
- Factoring in these variables, the model predicted **KIA to win their 12th Korean Series title** against Samsung.

![prediction_adding_variability.jpg](imgs%2Fprediction_adding_variability.jpg)

---

## 🧮 Prediction Results

- The model demonstrated **66.67% accuracy** in most simulations.
- Some simulations achieved **100% accuracy** in predicting the Korean Series winner and game results.

![prediction_accuracy2.jpg](imgs%2Fprediction_accuracy2.jpg)
![prediction_accuracy.jpg](imgs%2Fprediction_accuracy.jpg)

---

## 📂 File Descriptions

### **1. `regular_season_kia_samsung_score.xlsx`**
- Excel file containing regular-season game data.
- Key columns: Date, Home/Away teams, scores, batting averages, ERA, etc.

### **2. `Visualizing_Data.py`**
- Python script for visualizing win counts, batting averages, and ERA from 2021 to 2024.

### **3. `KIA_VS_SAMSUNG_REGULAR_SEASON.py`**
- Python script for performing regression analysis on regular-season data.
- Model: Random Forest Regressor.

### **4. `KIA_VS_SAMSUNG_KS_VARIABILITY.py`**
- Python script for a variability-enhanced prediction model tailored to the Korean Series.
- Model: Random Forest Classifier.

---

## References
- KBO (Korean Baseball Organization / Game Schedule Result) [https://www.koreabaseball.com/Schedule/Schedule.aspx](https://www.koreabaseball.com/Schedule/Schedule.aspx)
- ChatGPT [openai.com](https://openai.com)
