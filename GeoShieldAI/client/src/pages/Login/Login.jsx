import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  FiMail,
  FiLock,
  FiUser,
  FiAlertCircle,
  FiCheckCircle,
  FiShield,
  FiActivity,
  FiCpu,
} from 'react-icons/fi';
import { AuthContext } from '../../context/AuthContext';
import './Login.css';

export default function Login() {
  const navigate = useNavigate();
  const { login, register } = useContext(AuthContext);

  const [isLogin, setIsLogin] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const [formData, setFormData] = useState({
    email: '',
    password: '',
    name: '',
  });

  const resetMessages = () => {
    setError('');
    setSuccess('');
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
    resetMessages();
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    resetMessages();

    try {
      if (isLogin) {
        const result = await login(formData.email, formData.password);
        if (result.success) {
          setSuccess('Login successful! Redirecting...');
          setTimeout(() => navigate('/dashboard'), 1000);
        } else {
          setError(result.message || 'Login failed');
        }
      } else {
        if (formData.password.length < 6) {
          setError('Password must be at least 6 characters');
          setLoading(false);
          return;
        }

        if (!formData.name) {
          setError('Name is required');
          setLoading(false);
          return;
        }

        const result = await register(formData.email, formData.password, formData.name);
        if (result.success) {
          setSuccess(result.message);
          setFormData({ email: '', password: '', name: '' });
          setTimeout(() => setIsLogin(true), 1800);
        } else {
          setError(result.message || 'Registration failed');
        }
      }
    } catch (err) {
      setError('An error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-video-background" aria-hidden="true">
        <video autoPlay muted loop playsInline className="background-video">
          <source src="https://cdn.prod.website-files.com/603e56f6ed7c98040f01288b/60ac8928d7825ac8d0f9ce57_cyberhub-home-bg-video-transcode.mp4" type="video/mp4" />
        </video>
        <div className="video-overlay"></div>
      </div>

      <motion.div
        className="auth-shell"
        initial={{ opacity: 0, y: 24 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.55, ease: 'easeOut' }}
      >
        <motion.div
          className="auth-panel auth-panel-visual"
          key={isLogin ? 'login-visual' : 'signup-visual'}
          initial={{ x: isLogin ? -24 : 24, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ duration: 0.45 }}
        >
          <div className="panel-glow"></div>
          <div className="visual-content">
            <div className="brand-pill">
              <FiShield size={16} />
              <span>GeoAstra AI</span>
            </div>
            <h2>{isLogin ? 'Secure every signal' : 'Join the defense layer'}</h2>
            <p>
              {isLogin
                ? ''
                : ''}
            </p>

            <ul className="benefit-list">
              <li>
                <FiActivity size={16} /> Live threat monitoring
              </li>
              <li>
                <FiCpu size={16} /> AI-powered insights
              </li>
              <li>
                <FiShield size={16} /> Protected asset visibility
              </li>
            </ul>

            <div className="mini-metrics">
              <div className="metric-card">
                <strong>24/7</strong>
                <span>Coverage</span>
              </div>
              <div className="metric-card">
                <strong>AI</strong>
                <span>Analysis</span>
              </div>
              <div className="metric-card">
                <strong>Live</strong>
                <span>Alerts</span>
              </div>
            </div>
          </div>
        </motion.div>

        <div className="auth-panel auth-panel-form">
          <motion.div
            className="form-shell"
            key={isLogin ? 'login-form' : 'signup-form'}
            initial={{ x: isLogin ? 24 : -24, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ duration: 0.4 }}
          >
            <div className="form-switch" role="tablist" aria-label="Authentication mode">
              <button
                type="button"
                className={`switch-button ${isLogin ? 'active' : ''}`}
                onClick={() => {
                  setIsLogin(true);
                  resetMessages();
                }}
              >
                Sign In
              </button>
              <button
                type="button"
                className={`switch-button ${!isLogin ? 'active' : ''}`}
                onClick={() => {
                  setIsLogin(false);
                  resetMessages();
                }}
              >
                Sign Up
              </button>
            </div>

            <div className="form-header">
              <h3>{isLogin ? 'Welcome back' : 'Create your account'}</h3>
              <p>
                {isLogin
                  ? 'Sign in to continue protecting your network.'
                  : 'Start with a secure account and unlock the full platform.'}
              </p>
            </div>

            <form onSubmit={handleSubmit} className="login-form">
              {error && (
                <motion.div
                  className="alert alert-error"
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                >
                  <FiAlertCircle size={18} />
                  <span>{error}</span>
                </motion.div>
              )}

              {success && (
                <motion.div
                  className="alert alert-success"
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                >
                  <FiCheckCircle size={18} />
                  <span>{success}</span>
                </motion.div>
              )}

              {!isLogin && (
                <motion.div
                  className="form-group"
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  transition={{ duration: 0.3 }}
                >
                  <label htmlFor="name">Full Name</label>
                  <div className="input-wrapper">
                    <FiUser size={18} className="input-icon" />
                    <input
                      id="name"
                      type="text"
                      name="name"
                      value={formData.name}
                      onChange={handleChange}
                      placeholder="Your full name"
                      required
                      disabled={loading}
                    />
                  </div>
                </motion.div>
              )}

              <div className="form-group">
                <label htmlFor="email">Email Address</label>
                <div className="input-wrapper">
                  <FiMail size={18} className="input-icon" />
                  <input
                    id="email"
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    placeholder="your@email.com"
                    required
                    disabled={loading}
                  />
                </div>
              </div>

              <div className="form-group">
                <label htmlFor="password">Password</label>
                <div className="input-wrapper">
                  <FiLock size={18} className="input-icon" />
                  <input
                    id="password"
                    type="password"
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    placeholder="••••••••"
                    required
                    disabled={loading}
                  />
                </div>
              </div>

              <motion.button
                type="submit"
                className="submit-button"
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                disabled={loading}
              >
                {loading ? (
                  <span className="loading-spinner"></span>
                ) : isLogin ? (
                  'Sign In'
                ) : (
                  'Create Account'
                )}
              </motion.button>
            </form>

            <div className="login-footer">
              <p>
                {isLogin ? "Don't have an account? " : 'Already have an account? '}
                <button
                  className="toggle-button"
                  type="button"
                  onClick={() => {
                    setIsLogin(!isLogin);
                    resetMessages();
                  }}
                >
                  {isLogin ? 'Sign Up' : 'Sign In'}
                </button>
              </p>
            </div>

            <div className="demo-credentials">
              <p className="demo-label">Demo Account</p>

            </div>
          </motion.div>
        </div>
      </motion.div>
    </div>
  );
}
