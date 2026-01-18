import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Dashboard = () => {
  const [history, setHistory] = useState([]);
  const [metrics, setMetrics] = useState(null);

  useEffect(() => {
    fetchHistory();
    fetchMetrics();
  }, []);

  const fetchHistory = async () => {
    try {
      const response = await axios.get('/api/v1/history');
      setHistory(response.data.history);
    } catch (error) {
      console.error('Failed to fetch history:', error);
    }
  };

  const fetchMetrics = async () => {
    try {
      const response = await axios.get('/api/v1/metrics');
      setMetrics(response.data);
    } catch (error) {
      console.error('Failed to fetch metrics:', error);
    }
  };

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem' }}>
      {/* System Metrics */}
      <div className="card">
        <h2>System Metrics</h2>
        {metrics ? (
          <div>
            <div className="metrics-row">
              <span>Total Datasets</span>
              <strong>{metrics.total_datasets}</strong>
            </div>
            <div className="metrics-row">
              <span>Total Analyses</span>
              <strong>{metrics.total_analyses}</strong>
            </div>
            <div className="metrics-row">
              <span>Avg Processing Time</span>
              <strong>{metrics.avg_processing_time}s</strong>
            </div>
          </div>
        ) : (
          <div className="loading">Loading metrics...</div>
        )}
      </div>

      {/* Recent History */}
      <div className="card">
        <h2>Recent Activity</h2>
        {history.length > 0 ? (
          <div style={{ maxHeight: '300px', overflowY: 'auto' }}>
            {history.map((item, index) => (
              <div key={index} className="history-item">
                <div style={{ fontWeight: '400', marginBottom: '0.5rem', fontSize: '1.1rem' }}>
                  {item.dataset_name}
                </div>
                <div className="history-date">
                  {new Date(item.timestamp).toLocaleString()}
                </div>
                <div style={{ fontSize: '0.95rem', color: '#888', marginTop: '0.75rem', fontWeight: 300 }}>
                  {item.summary.substring(0, 120)}...
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div style={{ textAlign: 'center', color: '#666', padding: '3rem', fontWeight: 300 }}>
            No activity yet
            <div style={{ fontSize: '0.9rem', marginTop: '0.5rem', opacity: 0.7 }}>
              Upload your first dataset to begin
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;