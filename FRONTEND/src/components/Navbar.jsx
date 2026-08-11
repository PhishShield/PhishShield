import React, { useState, useEffect } from 'react';

export default function Navbar() {
  const [apiOnline, setApiOnline] = useState(false);

  useEffect(() => {
    // Ping backend root health check
    fetch('http://127.0.0.1:8000/')
      .then((res) => {
        if (res.ok) setApiOnline(true);
        else setApiOnline(false);
      })
      .catch(() => setApiOnline(false));
  }, []);

  return (
    <nav className="w-full bg-slate-900 border-b border-slate-800 px-6 py-4 flex justify-between items-center">
      <h2 className="text-sky-400 font-mono font-bold text-xl flex items-center gap-2">
        🛡️ PhishShield
      </h2>
      <div className="flex items-center gap-2 font-mono text-xs">
        <span
          className={`h-2.5 w-2.5 rounded-full ${
            apiOnline ? 'bg-emerald-400 shadow-[0_0_8px_#34d399]' : 'bg-rose-500 shadow-[0_0_8px_#f43f5e]'
          }`}
        ></span>
        <span className={apiOnline ? 'text-emerald-400' : 'text-rose-500'}>
          {apiOnline ? 'SYSTEM ONLINE' : 'OFFLINE'}
        </span>
      </div>
    </nav>
  );
}