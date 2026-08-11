import React from "react";

export default function StatsBanner({ stats }) {
  const total = stats?.totalScans ?? 0;
  const threats = stats?.threatsBlocked ?? 0;
  const safe = stats?.safeUrls ?? 0;

  return (
    <div className="grid grid-cols-3 gap-4 bg-slate-900/60 border border-slate-800 rounded-xl p-4 text-center font-mono">
      <div className="flex flex-col items-center">
        <span className="text-slate-400 text-xs tracking-wider uppercase mb-1">Total Scans</span>
        <span className="text-2xl font-bold text-sky-400">{total}</span>
      </div>

      <div className="flex flex-col items-center border-x border-slate-800 px-2">
        <span className="text-slate-400 text-xs tracking-wider uppercase mb-1">Threats Blocked</span>
        <span className="text-2xl font-bold text-rose-500">{threats}</span>
      </div>

      <div className="flex flex-col items-center">
        <span className="text-slate-400 text-xs tracking-wider uppercase mb-1">Safe URLs</span>
        <span className="text-2xl font-bold text-emerald-400">{safe}</span>
      </div>
    </div>
  );
}