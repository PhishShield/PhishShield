import React from "react";
import RiskMeter from "./RiskMeter";

export default function ResultCard({ result, url }) {
  if (result?.error) {
    return (
      <div className="animate-fade-in bg-rose-950/40 border border-rose-800 text-rose-300 p-5 rounded-xl text-center font-mono">
        ⚠️ {result.message || "An error occurred while analyzing the target."}
      </div>
    );
  }

  const score = result?.risk?.score ?? result?.risk_score ?? 0;
  const threatLevel = score >= 75 ? "CRITICAL THREAT" : score >= 50 ? "SUSPICIOUS" : "LOW RISK";

  const statusColor =
    score >= 75
      ? "text-rose-500 border-rose-500/30 bg-rose-500/10"
      : score >= 50
      ? "text-amber-400 border-amber-400/30 bg-amber-400/10"
      : "text-emerald-400 border-emerald-400/30 bg-emerald-400/10";

  // Safely extract API vendor statuses from response
  const vtStatus = result?.threat_intel?.virustotal ?? result?.virustotal ?? "Clean (0/90)";
  const gsbStatus = result?.threat_intel?.google_safe_browsing ?? result?.google_safe_browsing ?? "Passed";
  const urlScanStatus = result?.threat_intel?.urlscan ?? result?.urlscan ?? "No Malicious Indicators";

  return (
    <div className="animate-fade-in bg-slate-900/80 border border-slate-800 rounded-xl p-6 shadow-xl flex flex-col gap-6 font-mono">
      <div className="flex justify-between items-start border-b border-slate-800 pb-4">
        <div>
          <span className="text-slate-400 text-xs uppercase tracking-widest">Scan Report</span>
          <h3 className="text-slate-100 font-semibold text-lg break-all mt-1">{url}</h3>
        </div>
        <div className={`px-3 py-1 rounded-full border text-xs font-bold ${statusColor}`}>
          {threatLevel}
        </div>
      </div>

      {/* Replaced static score box with Risk Meter Gauge */}
      <div className="bg-slate-950/50 p-6 rounded-lg border border-slate-800/80 flex flex-col items-center justify-center">
        <RiskMeter score={score} />

        <p className={`text-xs mt-3 text-center font-bold ${statusColor.split(" ")[0]}`}>
          {score < 50
            ? "✅ SAFE: No major suspicious indicators detected."
            : "⚠️ WARNING: Potential threat activity flagged."}
        </p>
      </div>

      <div className="border-t border-slate-800 pt-4">
        <span className="text-slate-400 text-xs uppercase tracking-wider block mb-3">
          API Threat Intelligence
        </span>
        <div className="flex flex-col gap-2 text-xs">
          <div className="flex justify-between py-1 border-b border-slate-800/50">
            <span className="text-slate-400">VirusTotal:</span>
            <span className="text-slate-200">{vtStatus}</span>
          </div>
          <div className="flex justify-between py-1 border-b border-slate-800/50">
            <span className="text-slate-400">Google Safe Browsing:</span>
            <span className="text-slate-200">{gsbStatus}</span>
          </div>
          <div className="flex justify-between py-1">
            <span className="text-slate-400">URLScan:</span>
            <span className="text-slate-200">{urlScanStatus}</span>
          </div>
        </div>
      </div>
    </div>
  );
}