export const transformData = (data) => {
  return data.map(item => ({
    city: item.city,
    temperature: item.temperature,
    humidity: item.humidity,
    wind_speed: item.wind_speed,
    aqi: item.aqi,
    severity: item.anomaly?.severity || "normal",
    z_score: item.anomaly?.z_score,
    ml_score: item.anomaly?.ml_score,
  }));
};