export default function CityCard({ city }) {
  return (
    <div className="bg-linear-to-br from-[#1A1F36] to-[#121629] rounded-2xl p-6 shadow-xl border border-[#2A2E46] hover:shadow-2xl transition-all">
      <h2 className="text-xl font-bold mb-3 text-slate-100">{city.city}</h2>
      <p className="text-slate-400">🌡 {city.temperature}°C</p>
      <p className="text-slate-400">🌫 AQI: {city.aqi}</p>
      <p className="text-slate-400">💧 {city.humidity}%</p>
      <p className="text-slate-400">🌬 {city.wind_speed} km/h</p>
      {city.severity === "high" && (
        <p className="text-red-400 font-bold mt-2 flex items-center gap-1">
          <span>⚠</span> High Anomaly
        </p>
      )}
    </div>
  );
}