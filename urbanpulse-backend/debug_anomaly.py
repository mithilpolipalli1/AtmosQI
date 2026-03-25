import sys
sys.path.insert(0, ".")
from backend.database.session import SessionLocal
from backend.models.city_weather import CityWeather
from backend.models.city_air_quality import CityAirQuality
from backend.anomaly.service import fetch_recent_combined_data
from backend.anomaly.detector import detect_anomaly

db = SessionLocal()

# Check record counts
wc = db.query(CityWeather).filter(CityWeather.city == "Hyderabad").count()
ac = db.query(CityAirQuality).filter(CityAirQuality.city == "Hyderabad").count()
print(f"Weather records: {wc}")
print(f"AirQuality records: {ac}")

# Check timestamps
if wc > 0:
    w = db.query(CityWeather).filter(CityWeather.city == "Hyderabad").order_by(CityWeather.source_timestamp.desc()).first()
    print(f"Latest weather ts: {w.source_timestamp}")
if ac > 0:
    a = db.query(CityAirQuality).filter(CityAirQuality.city == "Hyderabad").order_by(CityAirQuality.source_timestamp.desc()).first()
    print(f"Latest AQ ts: {a.source_timestamp}, AQI: {a.aqi}")

# Test merge
df = fetch_recent_combined_data(db, "Hyderabad")
if df is not None:
    print(f"\nMerged DataFrame: {df.shape}")
    print(df.columns.tolist())
    print(df.tail(3))
    
    # Test detection
    try:
        result = detect_anomaly(df)
        print(f"\nDetection result: {result}")
    except Exception as e:
        print(f"\nDetection ERROR: {e}")
        import traceback
        traceback.print_exc()
else:
    print("\nMerged DataFrame is None! Timestamps may not align.")

db.close()
