import React, { useState, useEffect } from 'react';
import axios from 'axios';
import MLTraining from './MLTraining';

const ImageModal = ({ src, alt, isOpen, onClose }) => {
  if (!isOpen) return null;
  
  return (
    <div 
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.9)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 1000,
        cursor: 'pointer'
      }}
      onClick={onClose}
    >
      <img 
        src={src} 
        alt={alt} 
        style={{
          maxWidth: '95vw',
          maxHeight: '95vh',
          objectFit: 'contain',
          borderRadius: '12px'
        }}
      />
    </div>
  );
};

const AnalysisResults = ({ datasetId }) => {
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [modalImage, setModalImage] = useState({ src: '', alt: '', isOpen: false });

  useEffect(() => {
    const fetchAnalysis = async () => {
      try {
        setLoading(true);
        const response = await axios.get(`/api/v1/analyze/${datasetId}`);
        setAnalysis(response.data);
      } catch (err) {
        setError(err.response?.data?.detail || 'Analysis failed');
      } finally {
        setLoading(false);
      }
    };

    if (datasetId) {
      fetchAnalysis();
    }
  }, [datasetId]);

  if (loading) {
    return (
      <div className="card">
        <div className="loading">
          <div style={{ fontSize: '3rem', marginBottom: '2rem', opacity: 0.6 }}>📊</div>
          <h3>Analyzing your data</h3>
          <p>Running statistical analysis and building models</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="card">
        <div className="error">
          <strong>Analysis Error:</strong> {error}
        </div>
      </div>
    );
  }

  if (!analysis) return null;

  const { stats, charts, summary, processing_time } = analysis;

  return (
    <div>
      {/* Dataset Overview */}
      <div className="card">
        <h2>Dataset Overview</h2>
        <div className="stats-grid">
          <div className="stat-item">
            <div className="stat-value">{stats.shape[0]}</div>
            <div className="stat-label">Rows</div>
          </div>
          <div className="stat-item">
            <div className="stat-value">{stats.shape[1]}</div>
            <div className="stat-label">Columns</div>
          </div>
          <div className="stat-item">
            <div className="stat-value">{Object.values(stats.missing_values).reduce((a, b) => a + b, 0)}</div>
            <div className="stat-label">Missing Values</div>
          </div>
          <div className="stat-item">
            <div className="stat-value">{processing_time.toFixed(2)}s</div>
            <div className="stat-label">Processing Time</div>
          </div>
        </div>
      </div>

      {/* AI Summary */}
      <div className="card">
        <h2>Key Findings</h2>
        <div className="summary-box">
          <div style={{ 
            display: 'flex', 
            alignItems: 'center', 
            marginBottom: '1.5rem',
            fontSize: '0.9rem',
            color: '#888',
            textTransform: 'uppercase',
            letterSpacing: '2px',
            fontWeight: 300
          }}>
            <div style={{ fontSize: '1.5rem', marginRight: '1rem', opacity: 0.8 }}>🧠</div>
INSIGHTS
          </div>
          <p style={{ fontSize: '1.3rem', lineHeight: '1.8', fontWeight: 300 }}>{summary}</p>
        </div>
      </div>

      {/* Charts */}
      {charts.length > 0 && (
        <div className="card">
          <h2>Visualizations</h2>
          <div className="charts-grid">
            {charts.map((chart, index) => (
              <div key={index} className="chart-item">
                <img 
                  src={chart} 
                  alt={`Chart ${index + 1}`} 
                  onClick={() => setModalImage({ src: chart, alt: `Chart ${index + 1}`, isOpen: true })}
                  style={{ cursor: 'pointer' }}
                />
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Column Details */}
      <div className="card">
        <h2>Data Schema</h2>
        <div style={{ overflowX: 'auto' }}>
          <table>
            <thead>
              <tr>
                <th>Column</th>
                <th>Type</th>
                <th>Missing</th>
              </tr>
            </thead>
            <tbody>
              {stats.columns.map((col, index) => (
                <tr key={index}>
                  <td style={{ fontWeight: '400' }}>{col}</td>
                  <td style={{ color: '#888' }}>{stats.dtypes[col]}</td>
                  <td style={{ color: stats.missing_values[col] > 0 ? '#ff6b6b' : '#4ade80' }}>{stats.missing_values[col]}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
      
      {/* ML Training */}
      <MLTraining datasetId={datasetId} columns={stats.columns} />
      
      <ImageModal 
        src={modalImage.src}
        alt={modalImage.alt}
        isOpen={modalImage.isOpen}
        onClose={() => setModalImage({ src: '', alt: '', isOpen: false })}
      />
    </div>
  );
};

export default AnalysisResults;