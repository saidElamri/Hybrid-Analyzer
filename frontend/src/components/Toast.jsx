/**
 * Simple toast notification component.
 */
import React, { useEffect } from 'react';

export const Toast = ({ message, type = 'success', onClose, duration = 3000 }) => {
    useEffect(() => {
        if (message) {
            const timer = setTimeout(onClose, duration);
            return () => clearTimeout(timer);
        }
    }, [message, onClose, duration]);

    if (!message) return null;

    return (
        <div className={`toast toast-${type}`}>
            <span>{message}</span>
            <button className="toast-close" onClick={onClose}>✕</button>
        </div>
    );
};
