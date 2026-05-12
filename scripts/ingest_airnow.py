import os
import requests
import pandas as pd
from datetime import datetime

# Read API Key from environment variables
AIRNOW_API_KEY = os.environ.get("AIRNOW_API_KEY")

def fetch_airnow_data():
    if not AIRNOW_API_KEY:
        raise ValueError("AIRNOW_API_KEY environment variable is not set.")
    
    # Example base URL and parameters for AirNow API (e.g., Current Observation by Zip Code)
    url = "https://www.airnowapi.org/aq/observation/zipCode/current/"
    
    params = {
        "format": "application/json",
        "zipCode": "20002", # Example ZIP
        "distance": 25,
        "API_KEY": AIRNOW_API_KEY
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    return response.json()

def main():
    print("Starting AirNow ingestion...")
    data = fetch_airnow_data()
    
    if not data:
        print("No data received.")
        return
        
    df = pd.DataFrame(data)
    
    # Save output to Parquet
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(output_dir, f"airnow_{timestamp}.parquet")
    
    df.to_parquet(output_path, index=False)
    print(f"Data successfully saved to {output_path}")

if __name__ == "__main__":
    main()
