import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import MainLayout from '../../layouts/MainLayout';
import { FiSend, FiRefreshCw, FiDownload } from 'react-icons/fi';
import './Assistant.css';

const API_BASE_URL = 'http://127.0.0.1:5000/api';

export default function Assistant() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'ai',
      content: 'Hello! I\'m GeoAstra AI Assistant. I can help you with threat analysis, incident response, and security assessments. What would you like to know about your security threats?',
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('chat');
  const [threatDescription, setThreatDescription] = useState('');
  const [incidentDescription, setIncidentDescription] = useState('');
  const [assessmentResult, setAssessmentResult] = useState(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = {
      id: messages.length + 1,
      type: 'user',
      content: input,
      timestamp: new Date()
    };

    setMessages([...messages, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(
        `${API_BASE_URL}/assistant/chat`,
        {
          message: input,
          conversation: messages
        },
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );

      const aiMessage = {
        id: messages.length + 2,
        type: 'ai',
        content: response.data.response,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (err) {
      const errorMessage = {
        id: messages.length + 2,
        type: 'ai',
        content: `Sorry, I encountered an error: ${err.response?.data?.message || 'Unable to process request'}`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const analyzeThreat = async () => {
    if (!threatDescription.trim()) return;
    
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(
        `${API_BASE_URL}/assistant/threat-assessment`,
        { description: threatDescription },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      setAssessmentResult({
        type: 'threat',
        content: response.data.assessment
      });
    } catch (err) {
      setAssessmentResult({
        type: 'threat',
        content: `Error: ${err.response?.data?.message || 'Failed to analyze threat'}`
      });
    } finally {
      setLoading(false);
    }
  };

  const analyzeIncident = async () => {
    if (!incidentDescription.trim()) return;
    
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(
        `${API_BASE_URL}/assistant/incident-response`,
        { description: incidentDescription },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      setAssessmentResult({
        type: 'incident',
        content: response.data.guidance
      });
    } catch (err) {
      setAssessmentResult({
        type: 'incident',
        content: `Error: ${err.response?.data?.message || 'Failed to generate response plan'}`
      });
    } finally {
      setLoading(false);
    }
  };

  const downloadReport = (content, filename) => {
    const element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(content));
    element.setAttribute('download', filename);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  const clearChat = () => {
    setMessages([
      {
        id: 1,
        type: 'ai',
        content: 'Hello! I\'m GeoAstra AI Assistant. How can I help you today?',
        timestamp: new Date()
      }
    ]);
  };

  return (
    <MainLayout>
      <div className="assistant">
        <div className="assistant-header">
          <div>
            <h1>AI Security Assistant</h1>
            <p>Interactive threat analysis and incident response guidance</p>
          </div>
        </div>

        <div className="assistant-tabs">
          <button
            className={`tab-btn ${activeTab === 'chat' ? 'active' : ''}`}
            onClick={() => setActiveTab('chat')}
          >
            💬 Chat
          </button>
          <button
            className={`tab-btn ${activeTab === 'assess' ? 'active' : ''}`}
            onClick={() => setActiveTab('assess')}
          >
            🔍 Threat Assessment
          </button>
          <button
            className={`tab-btn ${activeTab === 'incident' ? 'active' : ''}`}
            onClick={() => setActiveTab('incident')}
          >
            🚨 Incident Response
          </button>
        </div>

        {/* Chat Tab */}
        {activeTab === 'chat' && (
          <div className="assistant-content">
            <div className="chat-container">
              <div className="messages-area">
                {messages.map((msg) => (
                  <div key={msg.id} className={`message ${msg.type}`}>
                    <div className="message-avatar">
                      {msg.type === 'ai' ? '🤖' : '👤'}
                    </div>
                    <div className="message-content">
                      <p>{msg.content}</p>
                      <span className="message-time">
                        {msg.timestamp.toLocaleTimeString()}
                      </span>
                    </div>
                  </div>
                ))}
                {loading && (
                  <div className="message ai">
                    <div className="message-avatar">🤖</div>
                    <div className="message-content typing">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>

              <form onSubmit={sendMessage} className="input-area">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Ask about threats, analysis, recommendations..."
                  disabled={loading}
                />
                <button type="submit" disabled={loading || !input.trim()}>
                  <FiSend />
                </button>
                <button 
                  type="button" 
                  className="clear-btn"
                  onClick={clearChat}
                  title="Clear conversation"
                >
                  <FiRefreshCw />
                </button>
              </form>
            </div>
          </div>
        )}

        {/* Threat Assessment Tab */}
        {activeTab === 'assess' && (
          <div className="assistant-content assessment-content">
            <div className="assessment-container">
              <div className="assessment-input">
                <h3>Threat Description</h3>
                <textarea
                  value={threatDescription}
                  onChange={(e) => setThreatDescription(e.target.value)}
                  placeholder="Describe the threat in detail. Include: threat type, targets, attack vector, observed indicators, etc."
                  rows={6}
                />
                <button 
                  onClick={analyzeThreat} 
                  disabled={loading || !threatDescription.trim()}
                  className="analyze-btn"
                >
                  {loading ? 'Analyzing...' : 'Analyze Threat'}
                </button>
              </div>

              {assessmentResult?.type === 'threat' && (
                <div className="assessment-result">
                  <div className="result-header">
                    <h3>Threat Assessment Report</h3>
                    <button
                      onClick={() => downloadReport(assessmentResult.content, 'threat_assessment.txt')}
                      className="download-btn-small"
                    >
                      <FiDownload /> Download
                    </button>
                  </div>
                  <div className="result-content">
                    {assessmentResult.content.split('\n').map((line, idx) => (
                      <p key={idx}>{line || '\u00A0'}</p>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Incident Response Tab */}
        {activeTab === 'incident' && (
          <div className="assistant-content assessment-content">
            <div className="assessment-container">
              <div className="assessment-input">
                <h3>Incident Description</h3>
                <textarea
                  value={incidentDescription}
                  onChange={(e) => setIncidentDescription(e.target.value)}
                  placeholder="Describe the incident: what was detected, when, what systems are affected, initial impact assessment, etc."
                  rows={6}
                />
                <button 
                  onClick={analyzeIncident} 
                  disabled={loading || !incidentDescription.trim()}
                  className="analyze-btn"
                >
                  {loading ? 'Generating...' : 'Generate Response Plan'}
                </button>
              </div>

              {assessmentResult?.type === 'incident' && (
                <div className="assessment-result">
                  <div className="result-header">
                    <h3>Incident Response Guidance</h3>
                    <button
                      onClick={() => downloadReport(assessmentResult.content, 'incident_response_plan.txt')}
                      className="download-btn-small"
                    >
                      <FiDownload /> Download
                    </button>
                  </div>
                  <div className="result-content">
                    {assessmentResult.content.split('\n').map((line, idx) => (
                      <p key={idx}>{line || '\u00A0'}</p>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </MainLayout>
  );
}
