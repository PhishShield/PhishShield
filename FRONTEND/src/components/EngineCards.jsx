import React from 'react';

export default function EngineCards({ scanData }) {
  // Extract engine outputs safely from backend response
  const vt = scanData?.virustotal || {};
  const gsb = scanData?.google_safebrowsing || {};
  const urlscan = scanData?.urlscan || {};

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '15px', margin: '20px 0' }}>
      
      {/* 🦠 VirusTotal Card */}
      <div style={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: '10px', padding: '15px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h4 style={{ color: '#38bdf8', margin: 0, fontFamily: 'monospace' }}>🦠 VirusTotal</h4>
          <span style={{ 
            fontSize: '11px', 
            padding: '2px 8px', 
            borderRadius: '4px', 
            background: vt.positives > 0 ? 'rgba(255,0,85,0.2)' : 'rgba(0,255,136,0.2)',
            color: vt.positives > 0 ? '#ff0055' : '#00ff88',
            border: `1px solid ${vt.positives > 0 ? '#ff0055' : '#00ff88'}`
          }}>
            {vt.positives > 0 ? 'FLAGGED' : 'CLEAN'}
          </span>
        </div>
        <div style={{ marginTop: '15px', fontFamily: 'monospace' }}>
          <div style={{ fontSize: '24px', color: vt.positives > 0 ? '#ff0055' : '#00ff88', fontWeight: 'bold' }}>
            {vt.positives || 0} / {vt.total || 0}
          </div>
          <small style={{ color: '#94a3b8' }}>Vendor Detections</small>
        </div>
      </div>

      {/* 🛡️ Google Safe Browsing Card */}
      <div style={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: '10px', padding: '15px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h4 style={{ color: '#38bdf8', margin: 0, fontFamily: 'monospace' }}>🛡️ Safe Browsing</h4>
          <span style={{ 
            fontSize: '11px', 
            padding: '2px 8px', 
            borderRadius: '4px', 
            background: gsb.is_malicious ? 'rgba(255,0,85,0.2)' : 'rgba(0,255,136,0.2)',
            color: gsb.is_malicious ? '#ff0055' : '#00ff88',
            border: `1px solid ${gsb.is_malicious ? '#ff0055' : '#00ff88'}`
          }}>
            {gsb.is_malicious ? 'MALICIOUS' : 'SAFE'}
          </span>
        </div>
        <div style={{ marginTop: '15px', fontFamily: 'monospace' }}>
          <div style={{ fontSize: '18px', color: gsb.is_malicious ? '#ff0055' : '#00ff88', fontWeight: 'bold' }}>
            {gsb.threat_type || 'No Threats Listed'}
          </div>
          <small style={{ color: '#94a3b8' }}>Database Threat Classification</small>
        </div>
      </div>

      {/* 🌐 URLScan Card */}
      <div style={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: '10px', padding: '15px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h4 style={{ color: '#38bdf8', margin: 0, fontFamily: 'monospace' }}>🌐 URLScan.io</h4>
          <span style={{ 
            fontSize: '11px', 
            padding: '2px 8px', 
            borderRadius: '4px', 
            background: urlscan.score > 20 ? 'rgba(255,0,85,0.2)' : 'rgba(0,255,136,0.2)',
            color: urlscan.score > 20 ? '#ff0055' : '#00ff88',
            border: `1px solid ${urlscan.score > 20 ? '#ff0055' : '#00ff88'}`
          }}>
            {urlscan.score > 20 ? 'RISK' : 'VERIFIED'}
          </span>
        </div>
        <div style={{ marginTop: '15px', fontFamily: 'monospace' }}>
          <div style={{ fontSize: '18px', color: '#e2e8f0', fontWeight: 'bold' }}>
            {urlscan.domain || 'N/A'}
          </div>
          <small style={{ color: '#94a3b8' }}>Target Domain Metadata</small>
        </div>
      </div>

    </div>
  );
}