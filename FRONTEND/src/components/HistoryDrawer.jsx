import React, { useEffect, useState } from 'react';

export default function HistoryDrawer({ onSelectHistory }) {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const res = await fetch('http://127.0.0.1:8000/history/');
      const data = await res.json();
      setHistory(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error("Failed to load history", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  return (
    <div style={{ background: '#0a0f1d', border: '1px solid #1e293b', borderRadius: '10px', padding: '20px', marginTop: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h3 style={{ color: '#00f0ff', margin: 0, fontFamily: 'monospace' }}>📜 Recent Scan History</h3>
        <button 
          onClick={fetchHistory} 
          style={{ background: '#1e293b', color: '#00f0ff', border: 'none', padding: '6px 12px', borderRadius: '6px', cursor: 'pointer' }}
        >
          🔄 Refresh
        </button>
      </div>

      {loading ? (
        <p style={{ color: '#94a3b8', fontFamily: 'monospace' }}>Loading historical logs...</p>
      ) : history.length === 0 ? (
        <p style={{ color: '#64748b', fontFamily: 'monospace', marginTop: '10px' }}>No previous scans recorded.</p>
      ) : (
        <div style={{ marginTop: '15px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
          {history.map((item, index) => (
            <div 
              key={index}
              onClick={() => onSelectHistory && onSelectHistory(item)}
              style={{ 
                display: 'flex', 
                justify: 'space-between', 
                alignItems: 'center', 
                background: '#0f172a', 
                padding: '10px 15px', 
                borderRadius: '6px', 
                border: '1px solid #334155',
                cursor: 'pointer'
              }}
            >
              <span style={{ color: '#e2e8f0', fontFamily: 'monospace', fontSize: '14px' }}>{item.url}</span>
              <span style={{ 
                color: item.risk_score >= 50 ? '#ff0055' : '#00ff88', 
                fontWeight: 'bold', 
                fontFamily: 'monospace' 
              }}>
                {item.risk_score}/100
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}