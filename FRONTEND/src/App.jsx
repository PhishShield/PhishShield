import React, { useState } from "react";
import Navbar from "./components/Navbar";
import RadarScanner from "./components/RadarScanner";
import StatsHUD from "./components/StatsHUD";
import ResultHUD from "./components/ResultHUD";
import HistoryHUD from "./components/HistoryHUD";
import { scanUrl } from "./api";

function App() {
  const [targetUrl, setTargetUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [scanResult, setScanResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [stats, setStats] = useState({
    totalScans: 0,
    threatsBlocked: 0,
    safeUrls: 0,
  });

  const handleScan = async (e) => {
    e.preventDefault();
    if (!targetUrl.trim() || loading) return;

    const cleanUrl = targetUrl.replace(/\[.*?\]\((.*?)\)/, "$1").replace(/[\[\]]/g, "").trim();

    setLoading(true);
    setScanResult(null);

    const minAnimationTime = new Promise((resolve) => setTimeout(resolve, 3500));

    try {
      const [data] = await Promise.all([
        scanUrl(cleanUrl),
        minAnimationTime,
      ]);

      setScanResult(data);

      const riskScore = data?.risk?.score ?? data?.risk_score ?? 0;
      const isThreat = riskScore >= 50;

      setStats((prev) => ({
        totalScans: prev.totalScans + 1,
        threatsBlocked: isThreat ? prev.threatsBlocked + 1 : prev.threatsBlocked,
        safeUrls: !isThreat ? prev.safeUrls + 1 : prev.safeUrls,
      }));

      const newHistoryItem = {
        id: Date.now(),
        url: cleanUrl,
        score: riskScore,
        isThreat: isThreat,
        timestamp: new Date().toLocaleTimeString(),
      };

      setHistory((prev) => [newHistoryItem, ...prev]);
    } catch (error) {
      await minAnimationTime;
      setScanResult({
        error: true,
        message: "Threat database connection timed out.",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleClearHistory = () => {
    setHistory([]);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-mono relative">
      <Navbar />

      <main className="flex-1 max-w-6xl w-full mx-auto px-6 py-8 flex flex-col gap-6">
        
        {/* Top Input Form */}
        <form onSubmit={handleScan} className="hud-panel p-6 hud-panel-active">
          <label className="block text-slate-300 text-sm font-bold uppercase tracking-widest mb-3">
            INITIALIZE TARGET SCAN VECTOR
          </label>
          <div className="flex gap-3 w-full">
            <input
              type="text"
              placeholder="ENTER PROTOCOL + DOMAIN (e.g., https://...)"
              value={targetUrl}
              onChange={(e) => setTargetUrl(e.target.value)}
              className="flex-1 bg-slate-950/80 border border-slate-700/80 focus:border-sky-500 focus:ring-1 focus:ring-sky-500 text-sky-200 px-4 py-3.5 rounded-lg outline-none text-base placeholder:text-slate-600 font-bold transition-all"
              required
            />
            <button
              type="submit"
              disabled={loading}
              className="bg-sky-500 hover:bg-sky-400 disabled:bg-slate-800 text-slate-950 font-extrabold px-8 py-3.5 rounded-lg text-base tracking-tight transition-all flex items-center gap-2 whitespace-nowrap cursor-pointer"
            >
              {loading ? "PROCESSING..." : "EXECUTE"}
              <span className="text-sm">▶</span>
            </button>
          </div>
        </form>

        {/* Stats Section */}
        <StatsHUD stats={stats} />

        {/* 2-Column Dashboard Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          
          {/* Active Threat Vector Column */}
          <div className="hud-panel flex flex-col min-h-[440px]">
            <div className="p-4 border-b border-slate-800/80 flex items-center justify-between">
              <span className="text-slate-200 text-base font-bold tracking-wide">ACTIVE THREAT VECTOR</span>
              <div className={`w-3.5 h-3.5 rounded-full ${loading ? 'bg-amber-400 animate-pulse' : 'bg-emerald-500'}`} />
            </div>
            
            <div className="flex-1 flex items-center justify-center p-6 relative">
              {loading ? (
                <RadarScanner targetUrl={targetUrl} />
              ) : scanResult ? (
                <ResultHUD result={scanResult} url={targetUrl} />
              ) : (
                <div className="text-center text-slate-500 flex flex-col items-center gap-4 py-12">
                  <span className="text-5xl">🛡️</span>
                  <span className="text-sm font-bold tracking-widest">SYSTEM READY. INITIATE SCAN SEQUENCE.</span>
                </div>
              )}
            </div>
          </div>

          {/* Session Activity Logs Column */}
          <div className="hud-panel flex flex-col min-h-[440px]">
            <div className="p-4 border-b border-slate-800/80 flex items-center justify-between">
              <span className="text-slate-200 text-base font-bold tracking-wide">SESSION ACTIVITY LOGS</span>
              <span className="text-xs text-sky-400 bg-sky-500/10 px-2.5 py-1 rounded border border-sky-500/30 font-bold">
                SECURE_CHANNEL://{history.length}
              </span>
            </div>
            
            <div className="flex-1 overflow-y-auto max-h-[400px]">
              <HistoryHUD items={history} onClearHistory={handleClearHistory} />
            </div>
          </div>

        </div>
      </main>
    </div>
  );
}

export default App;