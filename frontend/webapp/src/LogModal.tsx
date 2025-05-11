import React, { useState } from 'react';
import './Modal.css';

interface LogModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (level: string, message: string) => Promise<void>;
  isLoading?: boolean;
  error?: string | null;
}

const LogModal: React.FC<LogModalProps> = ({ 
  isOpen, 
  onClose, 
  onSubmit, 
  isLoading = false, 
  error = null 
}) => {
  const [level, setLevel] = useState('info');
  const [message, setMessage] = useState('');
  const [localError, setLocalError] = useState<string | null>(null);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setLocalError(null);

    if (!message.trim()) {
      setLocalError('Please enter a log message.');
      return;
    }

    try {
      await onSubmit(level, message);
    } catch (err) {
      console.error("Error submitting log:", err);
      setLocalError(err instanceof Error ? err.message : 'An unexpected error occurred.');
    }
  };

  const handleReset = () => {
    setLevel('info');
    setMessage('');
    setLocalError(null);
  };

  if (!isOpen) {
    return null;
  }

  // Display either local error or error passed as prop
  const errorToShow = localError || error;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h2>Create Log Message</h2>
        {errorToShow && <p className="error-message">{errorToShow}</p>}
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="logLevel">Log Level:</label>
            <select
              id="logLevel"
              value={level}
              onChange={(e) => setLevel(e.target.value)}
              disabled={isLoading}
              style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}
            >
              <option value="debug">Debug</option>
              <option value="info">Info</option>
              <option value="warning">Warning</option>
              <option value="error">Error</option>
              <option value="critical">Critical</option>
            </select>
          </div>
          <div className="form-group">
            <label htmlFor="logMessage">Message:</label>
            <textarea
              id="logMessage"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              rows={5}
              required
              disabled={isLoading}
              style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}
            />
          </div>
          <div className="modal-actions">
            <button 
              type="button" 
              onClick={handleReset} 
              disabled={isLoading}
              style={{ backgroundColor: '#6c757d', color: 'white' }}
            >
              Reset
            </button>
            <button type="submit" disabled={isLoading || !message.trim()}>
              {isLoading ? 'Submitting...' : 'Create Log'}
            </button>
            <button type="button" onClick={onClose} disabled={isLoading}>
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default LogModal;
