import { useEffect, useState } from "react";

export default function Header() {
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => {
      setTime(new Date());
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="px-10 py-8 flex justify-between items-center z-40 bg-[#070913]/40 backdrop-blur-xl border-b border-white/5">
      <div className="flex items-center gap-6">
        <div className="flex flex-col">
          <p className="text-xl text-indigo-400 font-black uppercase tracking-[0.2em] mb-2 drop-shadow-sm">
            {(() => {
              const hour = time.getHours();
              if (hour === 0) return "The Midnight Hour 🕛";
              if (hour >= 21 || hour < 5) return "Good Night 🌙";
              if (hour < 12) return "Good Morning ☀️";
              if (hour < 17) return "Good Afternoon 🌤️";
              return "Good Evening 🌆";
            })()}
          </p>
          <div className="flex items-center gap-4 opacity-40">
            <div className="w-1.5 h-1.5 rounded-full bg-indigo-500 animate-pulse" />
            <p className="text-[10px] text-slate-500 font-black uppercase tracking-[0.4em]">
              {time.toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" }).toUpperCase()}
            </p>
          </div>
        </div>
      </div>

      <div className="text-2xl font-bold text-slate-300 font-mono tracking-widest opacity-80 select-none">
        {time.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true }).toUpperCase()}
      </div>

    </div>
  );
}