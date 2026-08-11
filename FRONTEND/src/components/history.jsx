import React from "react";

export default function History({ items = [], history = [] }) {
  const scanList = Array.isArray(items) && items.length > 0 
    ? items 
    : Array.isArray(history) 
    ? history 
    : [];

  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-6 shadow-xl font-mono">
      <h3 className="text-slate-200 font-semibold text-sm uppercase tracking-wider mb-4">
        Scan History
      </h3>

      {scanList.length === 0 ? (
        <div className="text-center py-6 text-slate-500 text-xs">
          No scans recorded in this session.
        </div>
      ) : (
        <div className="flex flex-col gap-3">
          {scanList.map((item, index) => {
            const isThreat = item?.isThreat || (item?.score ?? 0) >= 50;
            const badgeColor = isThreat
              ? "bg-rose-500/10 text-rose-400 border-rose-500/30"
              : "bg-emerald-500/10 text-emerald-400 border-emerald-500/30";

            return (
              <div
                key={item?.id || index}
                className="flex items-center justify-between p-3 bg-slate-950/60 border border-slate-800 rounded-lg text-xs"
              >
                <div className="flex flex-col max-w-[70%]">
                  <span className="text-slate-200 truncate font-medium">{item?.url || "N/A"}</span>
                  <span className="text-slate-500 text-[10px] mt-0.5">{item?.timestamp || ""}</span>
                </div>

                <div className="flex items-center gap-3">
                  <span className="text-slate-400 font-bold">{item?.score ?? 0}/100</span>
                  <span className={`px-2 py-0.5 rounded border text-[10px] font-bold ${badgeColor}`}>
                    {isThreat ? "THREAT" : "SAFE"}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}