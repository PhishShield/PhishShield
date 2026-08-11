import React, { useState } from 'react';

export default function UrlScanner({ onScan, loading }) {
  const [url, setUrl] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!url.trim()) return;
    onScan(url.trim());
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-3 mb-6">
      <input
        type="text"
        placeholder="https://example-phishing-link.com"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        className="flex-1 bg-slate-900 border border-slate-800 rounded-lg px-4 py-3 text-slate-100 placeholder-slate-500 focus:outline-none focus:border-sky-500 transition-colors"
      />
      <button
        type="submit"
        disabled={loading}
        className="bg-sky-600 hover:bg-sky-700 text-white font-semibold px-6 py-3 rounded-lg transition-colors disabled:opacity-50 cursor-pointer"
      >
        {loading ? 'Scanning...' : 'Scan URL'}
      </button>
    </form>
  );
}