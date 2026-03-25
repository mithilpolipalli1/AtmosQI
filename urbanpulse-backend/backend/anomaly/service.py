import pandas as pd
from sqlalchemy.orm import Session

from backend.models.city_weather import CityWeather
from backend.models.city_air_quality import CityAirQuality
from backend.models.environmental_anomaly import EnvironmentalAnomaly
from backend.anomaly.detector import detect_anomaly


def generate_delivery_worker_alert(severity: str, value: float, insight: str) -> dict:
    advisory = {
        "target_group": "Delivery workers",
        "risk_level": severity.upper(),
        "recommended_action": "",
        "risk_window": "Active now until environmental conditions shift.",
        "safe_window": "Awaiting normalization. Monitor app for updates."
    }
    
    s = (severity or "").lower()
    if s == "critical":
        advisory["recommended_action"] = "CRITICAL EXPOSURE RISK. Minimize prolonged outdoor load immediately. Halt high-exertion delivery activity. Heavy duty N95 masks mandatory."
        advisory["risk_window"] = "Current conditions indicate severe sustained exposure risk."
        advisory["safe_window"] = "Seek indoor refuge / localized safety zones immediately."
    elif s == "high":
        advisory["recommended_action"] = "ELEVATED EXPOSURE RISK. Wear N95 masks. Reduce shift duration and take frequent breaks."
        advisory["risk_window"] = "High particulate load persisting during current window."
    elif s == "medium":
        advisory["recommended_action"] = "Moderate exposure risk. Wear standard protective masks if sensitive. Avoid idling in high traffic zones."
    else:
        advisory["recommended_action"] = "Standard exposure risk. Monitor dashboard for sudden changes."
        advisory["risk_window"] = "Conditions currently stable."
        advisory["safe_window"] = "Optimal window for standard delivery operations."
        
    return advisory


def fetch_recent_combined_data(db: Session, city: str, limit: int = 20) -> pd.DataFrame | None:
    weather_records = (
        db.query(CityWeather)
        .filter(CityWeather.city == city)
        .order_by(CityWeather.created_at.desc())
        .limit(limit)
        .all()
    )

    air_records = (
        db.query(CityAirQuality)
        .filter(CityAirQuality.city == city)
        .order_by(CityAirQuality.created_at.desc())
        .limit(limit)
        .all()
    )

    if not weather_records or not air_records:
        return None

    # Use row index to pair records (they are ingested in lockstep by live_sync)
    min_len = min(len(weather_records), len(air_records))
    if min_len < 3:
        return None

    rows = []
    for i in range(min_len - 1, -1, -1):  # Reverse: oldest first, newest last
        w = weather_records[i]
        a = air_records[i]
        rows.append({
            "source_timestamp": a.source_timestamp,
            "aqi": float(a.aqi),
            "temperature": float(w.temperature_c),
            "feels_like": float(w.feels_like_c),
            "humidity": float(w.humidity),
            "wind_speed": float(w.wind_speed),
        })

    df = pd.DataFrame(rows)
    if df.empty:
        return None

    return df.reset_index(drop=True)


def anomaly_already_exists(db: Session, city: str, metric_name: str, source_timestamp: int) -> bool:
    existing = (
        db.query(EnvironmentalAnomaly)
        .filter(EnvironmentalAnomaly.city == city)
        .filter(EnvironmentalAnomaly.metric_name == metric_name)
        .filter(EnvironmentalAnomaly.source_timestamp == source_timestamp)
        .first()
    )
    return existing is not None


def run_anomaly_detection(db: Session, city: str):
    df = fetch_recent_combined_data(db, city)

    if df is None or df.empty:
        return None

    result = detect_anomaly(df)

    if not result:
        return None

    if anomaly_already_exists(db, city, result["metric_name"], result["source_timestamp"]):
        return result

    anomaly = EnvironmentalAnomaly(
        city=city,
        metric_name=result["metric_name"],
        source_timestamp=result["source_timestamp"],
        value=result["value"],
        baseline=result["baseline"],
        z_score=result["z_score"],
        ml_score=result["ml_score"],
        detection_type=result["detection_type"],
        severity=result["severity"],
        insight=result.get("insight"),
        probable_cause=result.get("probable_cause"),
        recommended_action=result.get("recommended_action"),
        target_actor=result.get("target_actor"),
    )

    db.add(anomaly)
    db.commit()
    db.refresh(anomaly)

    return {
        "id": anomaly.id,
        "city": anomaly.city,
        "metric_name": anomaly.metric_name,
        "source_timestamp": anomaly.source_timestamp,
        "value": anomaly.value,
        "baseline": anomaly.baseline,
        "z_score": anomaly.z_score,
        "ml_score": anomaly.ml_score,
        "detection_type": anomaly.detection_type,
        "severity": anomaly.severity,
        "insight": anomaly.insight,
        "probable_cause": anomaly.probable_cause,
        "recommended_action": anomaly.recommended_action,
        "target_actor": anomaly.target_actor,
        "created_at": anomaly.created_at,
        "delivery_advisory": generate_delivery_worker_alert(anomaly.severity, anomaly.value, anomaly.insight)
    }