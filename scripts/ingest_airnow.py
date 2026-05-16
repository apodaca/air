import os
import requests
import pandas as pd
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv() # Load variables from .env if present

# Read API Key from environment variables
AIRNOW_API_KEY = os.environ.get("AIRNOW_API_KEY")

TARGET_ZIPS = [
    {"zip": "20002", "city": "Washington", "state": "DC", "lat": 38.8951, "lon": -77.0364},
    {"zip": "90001", "city": "Los Angeles", "state": "CA", "lat": 33.9731, "lon": -118.2479},
    {"zip": "60601", "city": "Chicago", "state": "IL", "lat": 41.8853, "lon": -87.6221},
    {"zip": "33101", "city": "Miami", "state": "FL", "lat": 25.7743, "lon": -80.1937},
    {"zip": "10001", "city": "New York", "state": "NY", "lat": 40.7128, "lon": -74.0060},
    {"zip": "80249", "city": "Denver", "state": "CO", "lat": 39.8561, "lon": -104.6737}
]

def generate_mock_historical_data(days=7):
    print("WARNING: AIRNOW_API_KEY not found. Generating mock historical Air Quality data for demonstration purposes.")
    mock_data = []
    
    # Generate data for the past `days` days for each zip code
    for i in range(days):
        date_obs = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d ")
        
        for loc in TARGET_ZIPS:
            # Randomize AQI a bit to show trends
            base_o3_aqi = random.randint(30, 80)
            base_pm_aqi = random.randint(40, 110)
            
            mock_data.extend([
                {
                    "DateObserved": date_obs,
                    "HourObserved": 12,
                    "LocalTimeZone": "EST",
                    "ReportingArea": loc["city"],
                    "StateCode": loc["state"],
                    "Latitude": loc["lat"],
                    "Longitude": loc["lon"],
                    "ParameterName": "O3",
                    "AQI": base_o3_aqi,
                    "Category": {"Number": 1 if base_o3_aqi <= 50 else 2, "Name": "Good" if base_o3_aqi <= 50 else "Moderate"}
                },
                {
                    "DateObserved": date_obs,
                    "HourObserved": 12,
                    "LocalTimeZone": "EST",
                    "ReportingArea": loc["city"],
                    "StateCode": loc["state"],
                    "Latitude": loc["lat"],
                    "Longitude": loc["lon"],
                    "ParameterName": "PM2.5",
                    "AQI": base_pm_aqi,
                    "Category": {"Number": 1 if base_pm_aqi <= 50 else 2, "Name": "Good" if base_pm_aqi <= 50 else "Moderate"}
                }
            ])
            
    return mock_data

def fetch_airnow_data(days=7):
    if not AIRNOW_API_KEY:
        return generate_mock_historical_data(days)
    
    all_data = []
    url = "https://www.airnowapi.org/aq/observation/zipCode/historical/"
    
    for i in range(days):
        target_date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        print(f"Fetching data for {target_date}...")
        
        for loc in TARGET_ZIPS:
            params = {
                "format": "application/json",
                "zipCode": loc["zip"],
                "date": f"{target_date}T12-0000",
                "distance": 25,
                "API_KEY": AIRNOW_API_KEY
            }
            
            try:
                response = requests.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                if data:
                    all_data.extend(data)
            except Exception as e:
                print(f"Error fetching {loc['city']} on {target_date}: {e}")
                
    return all_data

def main():
    print("Starting AirNow historical ingestion...")
    data = fetch_airnow_data(days=7)
    
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
