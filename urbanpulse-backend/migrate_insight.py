"""One-time migration: add insight column to environmental_anomalies table."""
from backend.database.session import engine
from sqlalchemy import text

with engine.connect() as conn:
    conn.execute(text("ALTER TABLE environmental_anomalies ADD COLUMN IF NOT EXISTS insight TEXT"))
    conn.commit()
    print("✅ Migration complete: 'insight' column added to environmental_anomalies")
