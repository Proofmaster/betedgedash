import json
import os
from datetime import datetime
import pandas as pd
from scipy.stats import poisson

def get_live_data():
    """Fetches the latest Premier League data."""
    # E0 is the Premier League data for the 25/26 season (adjust if needed)
    url = "https://www.football-data.co.uk/mmz4281/2526/E0.csv"
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        print(f"Error downloading data: {e}")
        return None

def calculate_team_strengths(df):
    """Calculates basic attacking and defensive strength using historical goals."""
    # Filter for matches that have already been played (have goals recorded)
    played_matches = df.dropna(subset=['FTHG', 'FTAG'])
    
    # Calculate league averages
    avg_home_goals = played_matches['FTHG'].mean()
    avg_away_goals = played_matches['FTAG'].mean()

    strengths = {}
    teams = played_matches['HomeTeam'].unique()

    for team in teams:
        # Home Attack & Defense
        home_games = played_matches[played_matches['HomeTeam'] == team]
        home_goals_scored = home_games['FTHG'].mean()
        home_goals_conceded = home_games['FTAG'].mean()
        
        # Away Attack & Defense
        away_games = played_matches[played_matches['AwayTeam'] == team]
        away_goals_scored = away_games['FTAG'].mean()
        away_goals_conceded = away_games['FTHG'].mean()

        # Calculate indices relative to league average
        home_attack = home_goals_scored / avg_home_goals if avg_home_goals > 0 else 1
        away_attack = away_goals_scored / avg_away_goals if avg_away_goals > 0 else 1
        home_defense = home_goals_conceded / avg_away_goals if avg_away_goals > 0 else 1
        away_defense = away_goals_conceded / avg_home_goals if avg_home_goals > 0 else 1

        strengths[team] = {
            'home_attack': home_attack,
            'away_attack': away_attack,
            'home_defense': home_defense,
            'away_defense': away_defense
        }
        
    return strengths, avg_home_goals, avg_away_goals

def predict_match(home_team, away_team, strengths, avg_home, avg_away):
    """Uses Poisson distribution to predict probabilities."""
    if home_team not in strengths or away_team not in strengths:
        return None

    # Calculate Expected Goals (xG)
    home_xg = strengths[home_team]['home_attack'] * strengths[away_team]['away_defense'] * avg_home
    away_xg = strengths[away_team]['away_attack'] * strengths[home_team]['home_defense'] * avg_away

    # Simulate probabilities (up to 5 goals)
    home_win_prob = 0
    draw_prob = 0
    away_win_prob = 0

    for home_goals in range(6):
        for away_goals in range(6):
            prob = poisson.pmf(home_goals, home_xg) * poisson.pmf(away_goals, away_xg)
            if home_goals > away_goals:
                home_win_prob += prob
            elif home_goals == away_goals:
                draw_prob += prob
            else:
                away_win_prob += prob

    # Normalize to percentages
    total = home_win_prob + draw_prob + away_win_prob
    
    return {
        "homeWinProb": round((home_win_prob / total) * 100, 1),
        "drawProb": round((draw_prob / total) * 100, 1),
        "awayWinProb": round((away_win_prob / total) * 100, 1),
        "home_xG": round(home_xg, 2),
        "away_xG": round(away_xg, 2)
    }

def generate_predictions():
    df = get_live_data()
    if df is None:
        return []

    strengths, avg_home, avg_away = calculate_team_strengths(df)
    
    # Get upcoming matches (where goals are NaN)
    upcoming = df[df['FTHG'].isna()].head(10) # Just get the next 10 fixtures
    
    predictions = []
    
    for index, row in upcoming.iterrows():
        home_team = row['HomeTeam']
        away_team = row['AwayTeam']
        date = row['Date']
        
        match_prediction = predict_match(home_team, away_team, strengths, avg_home, avg_away)
        
        if match_prediction:
            # Simple logic for 'value': if model thinks home team wins > 50%, flag it.
            # In the future, you will compare this against real Vegas odds.
            edge = match_prediction['homeWinProb'] > 50
            action = "Home Win" if edge else "Pass"
            
            predictions.append({
                "date": date,
                "homeTeam": home_team,
                "awayTeam": away_team,
                "homeWinProb": match_prediction['homeWinProb'],
                "drawProb": match_prediction['drawProb'],
                "awayWinProb": match_prediction['awayWinProb'],
                "modelValueEdge": edge,
                "recommendedBet": action
            })
            
    return predictions

def save_to_frontend(data):
    output_dir = "frontend/public/data"
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, "daily_predictions.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"Successfully saved {len(data)} live predictions.")

if __name__ == "__main__":
    live_predictions = generate_predictions()
    save_to_frontend(live_predictions)
