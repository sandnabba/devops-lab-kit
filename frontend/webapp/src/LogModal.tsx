import React, { useState } from 'react';
import './Modal.css';

interface LogModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (level: string, message: string) => Promise<void>;
}

const LogModal: React.FC<LogModalProps> = ({ isOpen, onClose, onSubmit }) => {
  const [level, setLevel] = useState('info');
  const [message, setMessage] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setError(null);

    if (!message.trim()) {
      setError('Please enter a log message.');
      return;
    }

    setIsSubmitting(true);
    try {
      await onSubmit(level, message);
    } catch (err) {
      console.error("Error submitting log:", err);
      setError(err instanceof Error ? err.message : 'An unexpected error occurred.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleReset = () => {
    setLevel('info');
    setMessage('');
    setError(null);
  };

  if (!isOpen) {
    return null;
  }

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h2>Create Log Message</h2>
        {error && <p className="error-message">{error}</p>}
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="logLevel">Log Level:</label>
            <select
              id="logLevel"
              value={level}
              onChange={(e) => setLevel(e.target.value)}
              disabled={isSubmitting}
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
              disabled={isSubmitting}
              style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}
            />
          </div>
          <div className="modal-actions">
            <button 
              type="button" 
              onClick={handleReset} 
              disabled={isSubmitting}
              style={{ backgroundColor: '#6c757d', color: 'white' }}
            >
              Reset
            </button>
            <button type="submit" disabled={isSubmitting || !message.trim()}>
              {isSubmitting ? 'Submitting...' : 'Create Log'}
            </button>
            <button type="button" onClick={onClose} disabled={isSubmitting}>
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default LogModal;
