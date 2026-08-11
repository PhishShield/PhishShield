import React from "react";

export default function HistoryHUD({ items = [], onClearHistory }) {
  return (
    <div className="font-mono p-4 flex flex-col gap-3">
      {/* Log Header Bar with Clear Action */}
      <div className="flex items-center justify-between pb-2 border-b border-slate-800/80">
        <span className="text-slate-400 text-xs uppercase tracking-widest font-bold">
          LOG ENTRIES ({items.length})
        </span>
        {items.length > 0 && (
          <button
            onClick={onClearHistory}
            className="text-xs text-rose-400 hover:text-rose-300 bg-rose-500/10 hover:bg-rose-500/20 border border-rose-500/30 px-3 py-1 rounded transition-all font-bold tracking-wider"
          >
            CLEAR LOGS
          </button>
        )}
      </div>

      {items.length === 0 ? (
        <div className="text-center py-14 text-slate-600 text-sm flex flex-col items-center gap-3">
          <span className="text-4xl">🗄️</span>
          <span className="font-bold tracking-wider">SESSION ACTIVITY LOG EMPTY</span>
        </div>
      ) : (
        <div className="flex flex-col gap-3">
          {items.map((item, index) => {
            const isThreat = item?.isThreat || (item?.score ?? 0) >= 50;
            const statusColor = isThreat
              ? "text-rose-400 border-rose-500/30 bg-rose-500/10"
              : "text-emerald-400 border-emerald-500/30 bg-emerald-500/10";
            
            const logId = String(item?.id || index).slice(-6);

            return (
              <div
                key={item?.id || index}
                className="flex items-center justify-between p-4 bg-slate-950/70 border border-slate-800/80 hover:border-sky-500/40 rounded-lg transition-all text-sm"
              >
                <div className="flex items-center gap-3 max-w-[70%]">
                  <span className="text-slate-600 text-xs font-bold">#{logId}</span>
                  <div className="flex flex-col truncate">
                    <span className="text-slate-100 truncate font-bold text-sm">{item?.url || "N/A"}</span>
                    <span className="text-slate-500 text-xs mt-1">{item?.timestamp || ""}</span>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <span className={`px-3 py-1 rounded border text-xs font-bold ${statusColor}`}>
                    {isThreat ? "THREAT" : "CLEAN"}
                  </span>
                  <span className="text-slate-200 font-extrabold text-base tracking-tight">{item?.score ?? 0}</span>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}