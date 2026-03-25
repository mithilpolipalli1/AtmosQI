import { useEffect, useState } from "react";

export default function Header() {
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => {
      setTime(new Date());
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  const getGreeting = () => {
    const hour = time.getHours();
    if (hour < 12) return "Good Morning";
    if (hour < 17) return "Good Afternoon";
    return "Good Evening";
  };

  return (
    <div className="px-10 py-8 flex justify-between items-center z-40 bg-[#070913]/40 backdrop-blur-xl border-b border-white/5">

      <div className="flex items-center gap-6">
        <div className="relative group cursor-pointer active:scale-95 transition">
          <img
            src="https://i.pravatar.cc/150?u=samuel"
            className="w-16 h-16 rounded-full border-2 border-white/10 group-hover:border-blue-500/50 transition-all shadow-2xl"
            alt="Profile Avatar"
          />
          <span className="absolute bottom-[2px] right-[2px] w-4 h-4 bg-emerald-500 rounded-full border-2 border-[#070913]"></span>
        </div>

        <div className="flex flex-col">
          <p className="text-sm text-slate-500 font-bold uppercase tracking-widest mb-1 opacity-60 italic">{getGreeting()} 🌤</p>
          <h1 className="text-2xl font-bold text-white tracking-tight leading-none">Samuel Johnson</h1>
          <p className="text-[10px] text-slate-500 font-bold uppercase tracking-[0.2em] mt-2 opacity-40">
            {time.toLocaleDateString("en-US", { month: "numeric", day: "numeric", year: "numeric" })}
          </p>
        </div>
      </div>

      <div className="text-2xl font-bold text-slate-300 font-mono tracking-widest opacity-80 select-none">
        {time.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true }).toUpperCase()}
      </div>

    </div>
  );
}