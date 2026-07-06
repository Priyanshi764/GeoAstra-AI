import React, { useState } from 'react';
import { motion } from 'framer-motion';
import MainLayout from '../../layouts/MainLayout';
import api from '../../services/api';
import { FiUpload, FiFileText, FiCheckCircle, FiAlertCircle } from 'react-icons/fi';
import './Upload.css';

export default function Upload() {
  const [dragActive, setDragActive] = useState(false);
  const [files, setFiles] = useState([]);
  const [manualText, setManualText] = useState('');
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('file');

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const droppedFiles = [...e.dataTransfer.files];
    setFiles(droppedFiles);
  };

  const handleFileSelect = (e) => {
    setFiles([...e.target.files]);
  };

  const uploadFile = async () => {
    if (files.length === 0) {
      setError('Please select a file');
      return;
    }

    setUploading(true);
    setError('');
    setResult(null);

    try {
      const formData = new FormData();
      formData.append('file', files[0]);
      formData.append('source', 'file_upload');

      const response = await api.post('/upload/document', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      if (response.data.success) {
        setResult(response.data);
        setFiles([]);
      } else {
        setError(response.data.message || 'Upload failed');
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Upload failed. Please try again.');
      console.error(err);
    } finally {
      setUploading(false);
    }
  };

  const submitManualIntelligence = async () => {
    if (!manualText.trim()) {
      setError('Please enter intelligence text');
      return;
    }

    setUploading(true);
    setError('');
    setResult(null);

    try {
      const response = await api.post('/upload/manual', {
        intelligence_text: manualText
      });

      if (response.data.success) {
        setResult(response.data);
        setManualText('');
      } else {
        setError(response.data.message || 'Processing failed');
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Processing failed. Please try again.');
      console.error(err);
    } finally {
      setUploading(false);
    }
  };

  return (
    <MainLayout>
      <div className="upload-page">
        <motion.div
          className="upload-header"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <h1>Upload Threat Intelligence</h1>
          <p>Upload documents or enter manual intelligence for AI analysis</p>
        </motion.div>

        <div className="upload-tabs">
          <button
            className={`tab ${activeTab === 'file' ? 'active' : ''}`}
            onClick={() => setActiveTab('file')}
          >
            <FiUpload size={18} />
            Upload File
          </button>
          <button
            className={`tab ${activeTab === 'manual' ? 'active' : ''}`}
            onClick={() => setActiveTab('manual')}
          >
            <FiFileText size={18} />
            Manual Entry
          </button>
        </div>

        {error && (
          <motion.div
            className="alert alert-error"
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <FiAlertCircle size={18} />
            <span>{error}</span>
          </motion.div>
        )}

        {result && (
          <motion.div
            className="alert alert-success"
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <FiCheckCircle size={18} />
            <div>
              <p><strong>Intelligence processed successfully!</strong></p>
              <div className="result-details">
                <span>📊 Risk Score: <strong>{result.analysis.risk_score}</strong></span>
                <span>🚨 Severity: <strong>{result.analysis.severity.toUpperCase()}</strong></span>
                <span>🎯 Type: <strong>{result.analysis.threat_type}</strong></span>
                {result.analysis.organizations.length > 0 && (
                  <span>🏢 Targets: <strong>{result.analysis.organizations.join(', ')}</strong></span>
                )}
                {result.analysis.districts.length > 0 && (
                  <span>📍 Districts: <strong>{result.analysis.districts.join(', ')}</strong></span>
                )}
              </div>
            </div>
          </motion.div>
        )}

        <motion.div
          className="upload-container"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
        >
          {activeTab === 'file' && (
            <div className="file-upload">
              <div
                className={`drop-zone ${dragActive ? 'active' : ''}`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
              >
                <div className="drop-icon">📄</div>
                <h3>Drag and drop files here</h3>
                <p>or</p>
                <label className="file-input-label">
                  Browse Files
                  <input
                    type="file"
                    onChange={handleFileSelect}
                    accept=".pdf,.txt,.csv,.json,.docx"
                    disabled={uploading}
                  />
                </label>
                <p className="support-formats">Supported: PDF, TXT, CSV, JSON, DOCX</p>
              </div>

              {files.length > 0 && (
                <div className="files-list">
                  <h4>Selected File:</h4>
                  {files.map((file, idx) => (
                    <div key={idx} className="file-item">
                      <span className="file-name">{file.name}</span>
                      <span className="file-size">
                        {(file.size / 1024 / 1024).toFixed(2)} MB
                      </span>
                    </div>
                  ))}
                  <motion.button
                    className="upload-btn"
                    onClick={uploadFile}
                    disabled={uploading}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                  >
                    {uploading ? 'Processing...' : 'Upload & Analyze'}
                  </motion.button>
                </div>
              )}
            </div>
          )}

          {activeTab === 'manual' && (
            <div className="manual-entry">
              <label>Threat Intelligence Report</label>
              <textarea
                value={manualText}
                onChange={(e) => setManualText(e.target.value)}
                placeholder="Paste or type threat intelligence here... Example: APT28 targeting government offices in MP..."
                rows={12}
                disabled={uploading}
              />
              <motion.button
                className="upload-btn"
                onClick={submitManualIntelligence}
                disabled={uploading || !manualText.trim()}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                {uploading ? 'Analyzing...' : 'Analyze Intelligence'}
              </motion.button>
            </div>
          )}
        </motion.div>
      </div>
    </MainLayout>
  );
}
