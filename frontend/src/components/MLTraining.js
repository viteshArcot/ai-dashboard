import React, { useState } from 'react';
import axios from 'axios';

const MLTraining = ({ datasetId, columns }) => {
  const [targetColumn, setTargetColumn] = useState('');
  const [training, setTraining] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleTrain = async () => {
    if (!targetColumn) {
      setError('Please select a target column');
      return;
    }

    setTraining(true);
    setError(null);
    
    try {
      const formData = new FormData();
      const response = await axios.post(
        `/api/v1/train?dataset_id=${datasetId}&target_column=${targetColumn}`,
        formData,
        { headers: { 'Content-Type': 'multipart/form-data' } }
      );
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Training failed');
    } finally {
      setTraining(false);
    }
  };

  if (!datasetId || !columns) return null;

  return (
    <div className="card">
      <h2>Machine Learning</h2>
      
      <div style={{ marginBottom: '2rem' }}>
        <label style={{ display: 'block', marginBottom: '1rem', color: '#ccc', fontSize: '0.95rem' }}>
          Select Target Column:
        </label>
        <select
          value={targetColumn}
          onChange={(e) => setTargetColumn(e.target.value)}
          style={{
            width: '100%',
            padding: '0.75rem',
            borderRadius: '12px',
            border: '1px solid rgba(255, 255, 255, 0.2)',
            background: 'rgba(255, 255, 255, 0.05)',
            color: '#fff',
            fontSize: '0.95rem'
          }}
        >
          <option value="">Choose target column...</option>
          {columns.map(col => (
            <option key={col} value={col} style={{ background: '#1a1a1a' }}>{col}</option>
          ))}
        </select>
      </div>

      <button
        className="btn"
        onClick={handleTrain}
        disabled={training || !targetColumn}
        style={{ marginBottom: '2rem' }}
      >
        {training ? 'Training Model...' : 'Train Model'}
      </button>

      {error && (
        <div className="error" style={{ marginBottom: '2rem' }}>
          {error}
        </div>
      )}

      {result && (
        <div>
          <div className="success" style={{ marginBottom: '2rem' }}>
            ✨ Model trained successfully!
          </div>
          
          <div className="stats-grid">
            <div className="stat-item">
              <div className="stat-value" style={{ fontSize: '1.2rem', wordBreak: 'break-word' }}>{result.algorithm}</div>
              <div className="stat-label">Algorithm</div>
            </div>
            <div className="stat-item">
              <div className="stat-value">{(result.score * 100).toFixed(1)}%</div>
              <div className="stat-label">{result.score_name}</div>
            </div>
            <div className="stat-item">
              <div className="stat-value">{Object.keys(result.feature_importance).length}</div>
              <div className="stat-label">Features</div>
            </div>
            <div className="stat-item">
              <div className="stat-value">{result.processing_time.toFixed(2)}s</div>
              <div className="stat-label">Training Time</div>
            </div>
          </div>

          {result.chart_url && (
            <div style={{ marginTop: '2rem' }}>
              <h3 style={{ marginBottom: '1rem', color: '#fff', fontWeight: 300 }}>Feature Importance</h3>
              <div className="chart-item">
                <img 
                  src={result.chart_url} 
                  alt="Feature Importance" 
                  style={{ cursor: 'pointer' }}
                />
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default MLTraining;