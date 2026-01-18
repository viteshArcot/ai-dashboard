import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import AnalysisResults from './components/AnalysisResults';
import Dashboard from './components/Dashboard';
import MLModels from './components/MLModels';

function App() {
  const [currentDataset, setCurrentDataset] = useState(null);
  const [uploadSuccess, setUploadSuccess] = useState(false);

  const handleUploadSuccess = (result) => {
    setCurrentDataset(result.dataset_id);
    setUploadSuccess(true);
    setTimeout(() => setUploadSuccess(false), 3000);
  };

  return (
    <div className="container">
      {/* Header */}
      <div className="header">
        <h1>DataLab</h1>
        <p>Automated data analysis and machine learning</p>
      </div>

      {/* Success Message */}
      {uploadSuccess && (
        <div className="success">
          ✓ Dataset uploaded successfully - analyzing now...
        </div>
      )}

      {/* File Upload */}
      <FileUpload onUploadSuccess={handleUploadSuccess} />

      {/* Analysis Results */}
      {currentDataset && (
        <AnalysisResults datasetId={currentDataset} />
      )}

      {/* ML Models */}
      <MLModels />
      
      {/* Dashboard */}
      <Dashboard />

      {/* Footer */}
      <div style={{ 
        textAlign: 'center', 
        marginTop: '4rem', 
        padding: '3rem',
        color: 'rgba(255, 255, 255, 0.3)',
        fontSize: '0.85rem',
        fontWeight: 300,
        letterSpacing: '1px'
      }}>
DATA SCIENCE • MACHINE LEARNING • AUTOMATION
      </div>
    </div>
  );
}

export default App;