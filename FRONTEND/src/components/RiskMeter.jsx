import React from "react";

export default function RiskMeter({ score = 0 }) {
  const numericScore = Number(score) || 0;
  const clampedScore = Math.min(Math.max(numericScore, 0), 100);

  // Math for full rainbow arc gauge
  const radius = 75;
  const circumference = Math.PI * radius;
  const strokeDashoffset = circumference - (clampedScore / 100) * circumference;

  const getSeverity = (s) => {
    if (s >= 75) {
      return {
        label: "REDLINE THREAT",
        badgeClass: "border-rose-500/50 bg-rose-500/10 text-rose-400 shadow-rose-500/20",
        scoreColor: "text-rose-400",
      };
    }
    if (s >= 50) {
      return {
        label: "ELEVATED RPM",
        badgeClass: "border-amber-500/50 bg-amber-500/10 text-amber-400 shadow-amber-500/20",
        scoreColor: "text-amber-400",
      };
    }
    return {
      label: "OPTIMAL PROTOCOL",
      badgeClass: "border-emerald-500/50 bg-emerald-500/10 text-emerald-400 shadow-emerald-500/20",
      scoreColor: "text-emerald-400",
    };
  };

  const theme = getSeverity(clampedScore);

  return (
    <div className="flex flex-col items-center justify-center font-mono my-2 w-full">
      <div className="relative w-72 h-44 flex justify-center items-end bg-slate-950/90 border border-slate-800 rounded-3xl p-4 shadow-2xl overflow-hidden">
        
        {/* Tachometer SVG Arc & Radial Tick Marks */}
        <svg className="w-full h-full overflow-visible" viewBox="0 0 200 115">
          <defs>
            {/* Rainbow Gradient across the tachometer arc */}
            <linearGradient id="rainbowGradient" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#10b981" />   {/* Emerald / Safe */}
              <stop offset="50%" stopColor="#fbbf24" />  {/* Amber / Warning */}
              <stop offset="100%" stopColor="#f43f5e" /> {/* Red / Redline */}
            </linearGradient>
          </defs>

          {/* Background Outer Arc Track */}
          <path
            d="M 25 100 A 75 75 0 0 1 175 100"
            fill="none"
            stroke="#1e293b"
            strokeWidth="14"
            strokeLinecap="round"
          />

          {/* Radial Tick Marks (0 to 10 RPM Index) */}
          {Array.from({ length: 11 }).map((_, i) => {
            const angle = -180 + i * 18; // Evenly spaced along semi-circle
            const rad = (angle * Math.PI) / 180;
            const x1 = 100 + 60 * Math.cos(rad);
            const y1 = 100 + 60 * Math.sin(rad);
            const x2 = 100 + 66 * Math.cos(rad);
            const y2 = 100 + 66 * Math.sin(rad);

            return (
              <line
                key={i}
                x1={x1}
                y1={y1}
                x2={x2}
                y2={y2}
                stroke={i >= 8 ? "#f43f5e" : "#64748b"}
                strokeWidth={i % 2 === 0 ? "2" : "1"}
              />
            );
          })}

          {/* Active Filled Rainbow Arc */}
          <path
            d="M 25 100 A 75 75 0 0 1 175 100"
            fill="none"
            stroke="url(#rainbowGradient)"
            strokeWidth="14"
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            className="transition-all duration-1000 ease-out"
          />
        </svg>

        {/* Digital Speedo Center Display */}
        <div className="absolute bottom-2 flex flex-col items-center z-10">
          <span className={`text-5xl font-black tracking-tight ${theme.scoreColor}`}>
            {clampedScore}
          </span>
          <span className="text-[10px] text-slate-500 uppercase tracking-widest font-bold mt-1">
            x 1000 RPM / RISK
          </span>
        </div>
      </div>

      {/* Status Capsule Badge */}
      <div className={`mt-3 px-4 py-1.5 rounded-full border text-xs font-black tracking-widest shadow-lg ${theme.badgeClass}`}>
        {theme.label}
      </div>
    </div>
  );
}