/**
 * Analysis history component - shows recent analyses from localStorage.
 */
import React, { useState, useEffect } from 'react';

const HISTORY_KEY = 'hybrid-analyzer-history';
const MAX_HISTORY = 10;

export const AnalysisHistory = ({ onSelect }) => {
    const [history, setHistory] = useState([]);
    const [isOpen, setIsOpen] = useState(true);

    useEffect(() => {
        const stored = localStorage.getItem(HISTORY_KEY);
        if (stored) {
            try {
                setHistory(JSON.parse(stored));
            } catch (e) {
                console.error('Failed to parse history:', e);
            }
        }
    }, []);

    const clearHistory = () => {
        localStorage.removeItem(HISTORY_KEY);
        setHistory([]);
    };

    const formatTime = (timestamp) => {
        const date = new Date(timestamp);
        const now = new Date();
        const diff = now - date;

        if (diff < 60000) return 'Just now';
        if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`;
        if (diff < 86400000) return `${Math.floor(diff / 3600000)}h ago`;
        return date.toLocaleDateString();
    };

    if (history.length === 0) return null;

    return (
        <div className="history-panel">
            <div className="history-header">
                <h4>Recent Analyses ({history.length})</h4>
                <button className="history-clear" onClick={clearHistory}>
                    Clear all
                </button>
            </div>
            <div className="history-list">
                {history.map((item, index) => (
                    <div
                        key={item.timestamp}
                        className="history-item"
                        onClick={() => onSelect(item)}
                    >
                        <div className="history-item-header">
                            <span className="history-category">{item.category}</span>
                            <span className="history-time">{formatTime(item.timestamp)}</span>
                        </div>
                        <div className="history-preview">
                            {item.summary?.substring(0, 80)}...
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

// Utility function to save analysis to history
export const saveToHistory = (results) => {
    const stored = localStorage.getItem(HISTORY_KEY);
    let history = [];

    try {
        history = stored ? JSON.parse(stored) : [];
    } catch (e) {
        history = [];
    }

    const entry = {
        ...results,
        timestamp: Date.now()
    };

    history.unshift(entry);
    if (history.length > MAX_HISTORY) {
        history = history.slice(0, MAX_HISTORY);
    }

    localStorage.setItem(HISTORY_KEY, JSON.stringify(history));
};
