/**
 * Results display component for analysis results.
 */
import React, { useState } from 'react';

export const ResultsDisplay = ({ results }) => {
    const [copied, setCopied] = useState(false);

    if (!results) return null;

    const getToneColor = (tone) => {
        switch (tone?.toLowerCase()) {
            case 'positive':
                return '#059669';
            case 'negative':
                return '#dc2626';
            default:
                return '#64748b';
        }
    };

    const getResultsAsText = () => {
        return `Category: ${results.category}
Confidence: ${(results.score * 100).toFixed(1)}%
Tone: ${results.tone}

Summary:
${results.summary}`;
    };

    const handleCopyResults = async () => {
        try {
            await navigator.clipboard.writeText(getResultsAsText());
            setCopied(true);
            setTimeout(() => setCopied(false), 2000);
        } catch (err) {
            console.error('Failed to copy:', err);
        }
    };

    const handleExportJSON = () => {
        const data = JSON.stringify({
            category: results.category,
            confidence: results.score,
            tone: results.tone,
            summary: results.summary,
            exportedAt: new Date().toISOString()
        }, null, 2);

        downloadFile(data, 'analysis-results.json', 'application/json');
    };

    const handleExportText = () => {
        const text = `Hybrid-Analyzer Results
========================
Date: ${new Date().toLocaleString()}

${getResultsAsText()}`;

        downloadFile(text, 'analysis-results.txt', 'text/plain');
    };

    const downloadFile = (content, filename, type) => {
        const blob = new Blob([content], { type });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    };

    return (
        <div className="results-display">
            <div className="results-header">
                <h3>Analysis Results</h3>
                <div className="results-actions">
                    <button
                        className="btn-copy"
                        onClick={handleCopyResults}
                        title="Copy results to clipboard"
                    >
                        {copied ? 'Copied!' : 'Copy'}
                    </button>
                    <div className="export-dropdown">
                        <button className="btn-export" title="Export results">
                            Export ▾
                        </button>
                        <div className="export-menu">
                            <button onClick={handleExportJSON}>Download JSON</button>
                            <button onClick={handleExportText}>Download Text</button>
                        </div>
                    </div>
                </div>
            </div>

            <div className="results-grid">
                <div className="result-card">
                    <div className="result-label">Category</div>
                    <div className="result-value category">
                        <span className="category-badge">{results.category}</span>
                    </div>
                </div>

                <div className="result-card">
                    <div className="result-label">Confidence Score</div>
                    <div className="result-value">
                        <div className="score-bar">
                            <div
                                className="score-fill"
                                style={{ width: `${results.score * 100}%` }}
                            ></div>
                        </div>
                        <span className="score-text">{(results.score * 100).toFixed(1)}%</span>
                    </div>
                </div>

                <div className="result-card">
                    <div className="result-label">Tone</div>
                    <div className="result-value">
                        <span
                            className="tone-badge"
                            style={{ backgroundColor: getToneColor(results.tone) }}
                        >
                            {results.tone}
                        </span>
                    </div>
                </div>

                <div className="result-card summary-card">
                    <div className="summary-header">
                        <div className="result-label">Summary</div>
                        <button
                            className="btn-copy-small"
                            onClick={() => {
                                navigator.clipboard.writeText(results.summary);
                                setCopied(true);
                                setTimeout(() => setCopied(false), 2000);
                            }}
                            title="Copy summary"
                        >
                            Copy
                        </button>
                    </div>
                    <div className="result-value summary-text">
                        {results.summary}
                    </div>
                </div>
            </div>
        </div>
    );
};
