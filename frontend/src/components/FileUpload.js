import React, { useState } from 'react';
import axios from 'axios';

const FileUpload = ({ onUploadSuccess }) => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [dragOver, setDragOver] = useState(false);

  const handleFileSelect = (selectedFile) => {
    if (selectedFile && selectedFile.name.endsWith('.csv')) {
      setFile(selectedFile);
    } else {
      alert('Please select a CSV file');
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    const droppedFile = e.dataTransfer.files[0];
    handleFileSelect(droppedFile);
  };

  const handleUpload = async () => {
    if (!file) return;

    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('/api/v1/upload', formData);
      onUploadSuccess(response.data);
      setFile(null);
    } catch (error) {
      alert('Upload failed: ' + error.response?.data?.detail);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="card">
      <h2>Upload Dataset</h2>
      
      <div
        className={`upload-area ${dragOver ? 'dragover' : ''}`}
        onDrop={handleDrop}
        onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
        onDragLeave={() => setDragOver(false)}
        onClick={() => document.getElementById('file-input').click()}
      >
        <div style={{ fontSize: '4rem', marginBottom: '2rem', opacity: 0.6 }}>📊</div>
        <h3 style={{ marginBottom: '1rem', fontSize: '1.5rem', fontWeight: 300 }}>
          {file ? file.name : 'Drop your dataset here'}
        </h3>
        <p style={{ color: '#666', fontSize: '0.95rem', fontWeight: 300 }}>
          CSV files only • Maximum 10MB
        </p>
      </div>

      <input
        id="file-input"
        type="file"
        accept=".csv"
        onChange={(e) => handleFileSelect(e.target.files[0])}
        style={{ display: 'none' }}
      />

      {file && (
        <div style={{ marginTop: '1rem', textAlign: 'center' }}>
          <button
            className="btn"
            onClick={handleUpload}
            disabled={uploading}
          >
            {uploading ? 'Processing...' : 'Analyze Data'}
          </button>
        </div>
      )}
    </div>
  );
};

export default FileUpload;