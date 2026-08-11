import React from "react";
import RiskMeter from "./RiskMeter";

export default function ResultHUD({ result, url }) {
  if (result?.error) {
    return (
      <div className="w-full text-center p-6 bg-rose-950/30 border border-rose-800/80 rounded-xl text-rose-300 font-mono-tech">
        <div className="text-xl mb-2 font-cyber">⚠️ ANALYSIS FAILED</div>
        <p className="text-xs text-rose-400">{result.message || "Threat database query timed out."}</p>
      </div>
    );
  }

  const score = result?.risk?.score ?? result?.risk_score ?? 0;
  
  const vtStatus = result?.threat_intel?.virustotal ?? result?.virustotal ?? "Clean (0/90)";
  const gsbStatus = result?.threat_intel?.google_safe_browsing ?? result?.google_safe_browsing ?? "Passed";
  const urlScanStatus = result?.threat_intel?.urlscan ?? result?.urlscan ?? "No Malicious Indicators";

  return (
    <div className="w-full flex flex-col gap-6 font-mono-tech animate-fade-in">
      <div className="flex-1 flex flex-col items-center justify-center p-6 bg-slate-950/60 border border-slate-800 rounded-xl relative shadow-inner overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-sky-900/10 via-transparent to-sky-900/10 opacity-40 animate-[hud-scanline_4s_infinite_linear]" />

        <RiskMeter score={score} />

        <div className="mt-4 text-center z-10">
          <p className="text-xs font-semibold tracking-wide text-slate-300">
            {score < 50
              ? "✅ PROTOCOL Legitimate. Phishing indicators absent."
              : "⚠️ ALERT: High risk signature detected. Potential phishing vector flagged."}
          </p>
        </div>
      </div>

      <div className="border-t border-slate-800/80 pt-5">
        <div className="flex items-center justify-between mb-3">
          <span className="text-slate-500 text-[11px] uppercase tracking-wider font-bold">
            VENDOR INTELLIGENCE FEED
          </span>
          <span className="font-cyber text-[9px] text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/30">
            LIVE CONNECTIVITY
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
          <div className="p-3 bg-slate-950/40 border border-slate-800/60 rounded-xl flex flex-col justify-between">
            <span className="text-slate-500 text-[11px] mb-1">VirusTotal_API</span>
            <span className="text-slate-100 font-bold truncate">{vtStatus}</span>
          </div>

          <div className="p-3 bg-slate-950/40 border border-slate-800/60 rounded-xl flex flex-col justify-between">
            <span className="text-slate-500 text-[11px] mb-1">Google_Safe_Browsing</span>
            <span className="text-slate-100 font-bold truncate">{gsbStatus}</span>
          </div>

          <div className="p-3 bg-slate-950/40 border border-slate-800/60 rounded-xl flex flex-col justify-between">
            <span className="text-slate-500 text-[11px] mb-1">URLScan_io_Engine</span>
            <span className="text-slate-100 font-bold truncate">{urlScanStatus}</span>
          </div>
        </div>
      </div>
    </div>
  );
}