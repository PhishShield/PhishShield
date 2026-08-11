import React from "react";

export default function StatsHUD({ stats }) {
  const metricItems = [
    { label: "PROTOCOL_SCANS_TOTAL", value: stats.totalScans, color: "text-sky-400", bg: "bg-sky-500/10", border: "border-sky-500/30" },
    { label: "MALICIOUS_VECTORS_NEUTRALIZED", value: stats.threatsBlocked, color: "text-rose-400", bg: "bg-rose-500/10", border: "border-rose-500/30" },
    { label: "VERIFIED_SAFE_ENDPOINTS", value: stats.safeUrls, color: "text-emerald-400", bg: "bg-emerald-500/10", border: "border-emerald-500/30" },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      {metricItems.map((item, idx) => (
        <div key={idx} className={`hud-panel p-5 ${item.border} ${item.bg} flex flex-col relative`}>
          <span className="text-slate-500 text-[10px] uppercase tracking-widest font-bold mb-2">
            {item.label}
          </span>
          <div className={`font-cyber font-black text-4xl ${item.color} leading-none tracking-tight`}>
            {String(item.value).padStart(2, '0')}
          </div>
        </div>
      ))}
    </div>
  );
}