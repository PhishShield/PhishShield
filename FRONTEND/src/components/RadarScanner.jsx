import React from "react";

export default function ResultCard({ result, url }) {
  if (result?.error) {
    return (
      <div className="animate-fade-in bg-rose-950/40 border border-rose-800 text-rose-300 p-5 rounded-xl text-center font-mono">
        ⚠️ {result.message || "An error occurred while analyzing the target."}
      </div>
    );
  }

  const score = result?.risk?.score ?? result?.risk_score ?? 0;
  const threatLevel = score >= 75 ? "CRITICAL THREAT" : score >= 50 ? "SUSPICIOUS" : "SAFE";
  
  const statusColor =
    score >= 75
      ? "text-rose-500 border-rose-500/30 bg-rose-500/10"
      : score >= 50
      ? "text-amber-400 border-amber-400/30 bg-amber-400/10"
      : "text-emerald-400 border-emerald-400/30 bg-emerald-400/10";

  return (
    <div className="animate-fade-in bg-slate-900/80 border border-slate-800 rounded-xl p-6 shadow-xl flex flex-col gap-4">
      <div className="flex justify-between items-start border-b border-slate-800 pb-4">
        <div>
          <span className="text-slate-400 text-xs font-mono uppercase tracking-widest">
            Target Analyzed
          </span>
          <h3 className="text-slate-100 font-mono font-semibold text-lg break-all">
            {url}
          </h3>
        </div>
        <div
          className={`px-3 py-1 rounded-full border text-xs font-mono font-bold ${statusColor}`}
        >
          {threatLevel}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Risk Score Gauge Display */}
        <div className="bg-slate-950/50 p-4 rounded-lg border border-slate-800/80 flex flex-col justify-center items-center">
          <span className="text-slate-400 text-xs font-mono mb-1">RISK SCORE</span>
          <span className={`text-4xl font-bold font-mono ${statusColor.split(" ")[0]}`}>
            {score} / 100
          </span>
        </div>

        {/* Engine Verdict Summary */}
        <div className="bg-slate-950/50 p-4 rounded-lg border border-slate-800/80 flex flex-col justify-center">
          <span className="text-slate-400 text-xs font-mono mb-1">ANALYSIS DETAILS</span>
          <p className="text-slate-300 text-xs font-mono">
            {result?.message || result?.verdict || "Multi-engine analysis complete. Threat metrics generated from security feed indicators."}
          </p>
        </div>
      </div>
    </div>
  );
}