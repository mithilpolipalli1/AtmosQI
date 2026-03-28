import os
from sqlalchemy import create_engine, text  # type: ignore
from backend.database.session import Base  # type: ignore
from backend.models.environmental_anomaly import EnvironmentalAnomaly  # type: ignore
# Force loading models to populate Base.metadata
from backend.models.city_weather import CityWeather  # type: ignore
from backend.models.city_air_quality import CityAirQuality  # type: ignore

from dotenv import load_dotenv  # type: ignore

env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)
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
