import os
from sqlalchemy import create_engine, text
from backend.database.session import Base
from backend.models.environmental_anomaly import EnvironmentalAnomaly
# Force loading models to populate Base.metadata
from backend.models.city_weather import CityWeather
from backend.models.city_air_quality import CityAirQuality

from dotenv import load_dotenv

load_dotenv(".env")
db_url = os.getenv("DATABASE_URL")

if not db_url:
    print("❌ DATABASE_URL not found")
    exit(1)

engine = create_engine(db_url)

print(f"Connecting to {db_url}...")
try:
    with engine.connect() as conn:
        print("Dropping old environmental_anomalies table...")
        conn.execute(text("DROP TABLE IF EXISTS environmental_anomalies CASCADE"))
        conn.commit()
    
    print("Recreating all metropolitan tables...")
    Base.metadata.create_all(engine)
    print("✅ Successfully recreated all tables.")
except Exception as e:
    print(f"❌ Initialization failed: {e}")
