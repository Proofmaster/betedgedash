import json
import os
import random
from datetime import datetime

def generate_predictions():
    # In the future, this is where you pull from FBRef or football-data.co.uk
    # and run the actual Poisson distribution or XGBoost model.
    
    # For now, we simulate the output format of a predictive model
    predictions = [
        {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "homeTeam": "Red Star Belgrade",
            "awayTeam": "Partizan",
            "homeWinProb": 52.4,
            "drawProb": 25.1,
            "awayWinProb": 22.5,
            "modelValueEdge": True,
            "recommendedBet": "Home Win"
        },
        {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "homeTeam": "Arsenal",
            "awayTeam": "Liverpool",
            "homeWinProb": 41.0,
            "drawProb": 29.0,
            "awayWinProb": 30.0,
            "modelValueEdge": False,
            "recommendedBet": "Pass"
        }
    ]
    return predictions

def save_to_frontend(data):
    # Ensure the target directory exists
    output_dir = "frontend/public/data"
    os.makedirs(output_dir, exist_ok=True)
    
    # Save the JSON file directly into the Next.js public folder
    file_path = os.path.join(output_dir, "daily_predictions.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
        
    print(f"Successfully saved {len(data)} predictions to {file_path}")

if __name__ == "__main__":
    daily_data = generate_predictions()
    save_to_frontend(daily_data)
