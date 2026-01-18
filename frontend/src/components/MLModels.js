import React, { useState, useEffect } from 'react';
import axios from 'axios';

const MLModels = () => {
  const [models, setModels] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchModels();
  }, []);

  const fetchModels = async () => {
    try {
      const response = await axios.get('/api/v1/models');
      setModels(response.data.models);
    } catch (error) {
      console.error('Failed to fetch models:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="card">
        <h2>Trained Models</h2>
        <div className="loading">Loading models...</div>
      </div>
    );
  }

  return (
    <div className="card">
      <h2>Trained Models</h2>
      
      {models.length > 0 ? (
        <div style={{ overflowX: 'auto' }}>
          <table>
            <thead>
              <tr>
                <th>Dataset</th>
                <th>Target</th>
                <th>Algorithm</th>
                <th>Score</th>
                <th>Created</th>
              </tr>
            </thead>
            <tbody>
              {models.map((model) => (
                <tr key={model.id}>
                  <td style={{ fontWeight: '400' }}>{model.dataset_name}</td>
                  <td style={{ color: '#4ecdc4' }}>{model.target_column}</td>
                  <td style={{ color: '#888', fontSize: '0.85rem', wordBreak: 'break-word' }}>{model.algorithm}</td>
                  <td style={{ color: model.score > 0.8 ? '#4ade80' : model.score > 0.6 ? '#feca57' : '#ff6b6b' }}>
                    {(model.score * 100).toFixed(1)}%
                  </td>
                  <td style={{ color: '#666', fontSize: '0.85rem' }}>
                    {new Date(model.created_at).toLocaleDateString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div style={{ textAlign: 'center', color: '#666', padding: '3rem', fontWeight: 300 }}>
          No models trained yet
          <div style={{ fontSize: '0.9rem', marginTop: '0.5rem', opacity: 0.7 }}>
            Upload a dataset and train your first model
          </div>
        </div>
      )}
    </div>
  );
};

export default MLModels;