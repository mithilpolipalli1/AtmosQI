from sqlalchemy import Column, Integer, String, Float, BigInteger, DateTime, Text
from sqlalchemy.sql import func

from backend.database.session import Base


class EnvironmentalAnomaly(Base):
    __tablename__ = "environmental_anomalies"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True, nullable=False)  # city name
    metric_name = Column(String, nullable=False)
    source_timestamp = Column(BigInteger, nullable=False)

    value = Column(Float, nullable=False)
    baseline = Column(Float, nullable=True)
    z_score = Column(Float, nullable=True)
    ml_score = Column(Float, nullable=True)

    detection_type = Column(String, nullable=False)   # statistical / ml / both
    severity = Column(String, nullable=False)         # low / medium / high / critical
    insight = Column(Text, nullable=True)             # human-readable explanation
    
    # RESPONSE FIELDS
    probable_cause = Column(String, nullable=True)
    recommended_action = Column(String, nullable=True)
    target_actor = Column(String, nullable=True)
    status = Column(String, default="TRIGGERED")      # TRIGGERED / MITIGATED / RESOLVED

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)