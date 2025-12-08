/**
 * Error message component with retry button.
 */
import React from 'react';

export const ErrorMessage = ({ message, onClose, onRetry }) => {
    if (!message) return null;

    return (
        <div className="error-message">
            <div className="error-content">
                <span className="error-icon">!</span>
                <p>{message}</p>
                <div className="error-actions">
                    {onRetry && (
                        <button className="btn-retry" onClick={onRetry}>
                            Retry
                        </button>
                    )}
                    {onClose && (
                        <button className="error-close" onClick={onClose}>
                            ✕
                        </button>
                    )}
                </div>
            </div>
        </div>
    );
};
