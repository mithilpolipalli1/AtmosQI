import requests  # pyre-fixme[21]: Could not find module `requests`.
import time

cities = ["Hyderabad", "Delhi", "Mumbai", "Kolkata", "Bengaluru", "Chennai"]

print("🚀 Starting Atmospheric Data Sync Worker (Urban Network Edition)...")
print("Fetching live city metrics from OpenWeather every 15 seconds.")

while True:
    for city in cities:
        try:
            w = requests.post(f"http://127.0.0.1:8000/ingest/weather/{city}")
            a = requests.post(f"http://127.0.0.1:8000/ingest/air-quality/{city}")
            if w.status_code == 200 and a.status_code == 200:
                print(f"✅ Synced live data for {city}")
            else:
                print(f"⚠️ Failed to sync {city}: Weather {w.status_code}, AQI {a.status_code}")
        except Exception as e:
            print(f"❌ Error communicating with backend for {city}")
    
    print("⏳ Waiting 15 seconds before next sync...\n")
    time.sleep(15)
