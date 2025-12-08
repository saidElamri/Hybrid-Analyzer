/**
 * Analysis form component for text input and submission.
 */
import React, { useState, useEffect, useRef, useMemo } from 'react';

const STORAGE_KEY = 'hybrid-analyzer-draft';

// Sample texts for quick demo
const SAMPLE_TEXTS = [
    {
        label: 'Tech Article',
        text: `Artificial intelligence continues to reshape industries across the globe. From healthcare diagnostics to autonomous vehicles, AI systems are becoming increasingly sophisticated. Machine learning algorithms can now process vast amounts of data to identify patterns that would take humans years to discover. However, concerns about job displacement and ethical implications remain at the forefront of public discourse. Experts emphasize the importance of developing AI responsibly, with proper oversight and transparent decision-making processes.`
    },
    {
        label: 'Business News',
        text: `Global markets showed mixed results today as investors weighed economic data against geopolitical concerns. Tech stocks led gains in early trading, with major indices climbing 1.2% before settling. Analysts noted increased volatility as quarterly earnings reports continue to influence trading patterns. Central banks remain cautious about interest rate policies, with most economists predicting steady rates through the next quarter. Small-cap stocks showed resilience despite broader market uncertainty.`
    },
    {
        label: 'Science Report',
        text: `Researchers at the university have made a breakthrough discovery in quantum computing. The team successfully demonstrated quantum entanglement at room temperature, a feat previously thought impossible. This advancement could accelerate the development of practical quantum computers by several years. The implications for cryptography, drug discovery, and climate modeling are significant. Further research is needed to scale the technology for commercial applications.`
    }
];

// Text statistics calculator
const calculateStats = (text) => {
    const words = text.trim().split(/\s+/).filter(w => w.length > 0);
    const sentences = text.split(/[.!?]+/).filter(s => s.trim().length > 0);
    const paragraphs = text.split(/\n\n+/).filter(p => p.trim().length > 0);
    const avgWordLength = words.length > 0
        ? (words.reduce((sum, w) => sum + w.length, 0) / words.length).toFixed(1)
        : 0;
    const readingTime = Math.ceil(words.length / 200); // ~200 wpm

    return {
        characters: text.length,
        words: words.length,
        sentences: sentences.length,
        paragraphs: paragraphs.length,
        avgWordLength,
        readingTime
    };
};

// Character progress bar component
const CharacterProgress = ({ current, max }) => {
    const percentage = (current / max) * 100;
    const getStatus = () => {
        if (percentage >= 90) return 'danger';
        if (percentage >= 70) return 'warning';
        return '';
    };

    return (
        <div className="char-progress">
            <div className="char-progress-bar">
                <div
                    className={`char-progress-fill ${getStatus()}`}
                    style={{ width: `${Math.min(percentage, 100)}%` }}
                />
            </div>
            <span className="char-progress-text">
                {current.toLocaleString()} / {max.toLocaleString()}
            </span>
        </div>
    );
};

// Text statistics display
const TextStats = ({ stats }) => {
    if (stats.words === 0) return null;

    return (
        <div className="text-stats">
            <span>{stats.words} words</span>
            <span className="stat-divider">•</span>
            <span>{stats.sentences} sentences</span>
            <span className="stat-divider">•</span>
            <span>~{stats.readingTime} min read</span>
        </div>
    );
};

export const AnalysisForm = ({ onAnalyze, loading }) => {
    const [text, setText] = useState(() => {
        return localStorage.getItem(STORAGE_KEY) || '';
    });
    const [customLabels, setCustomLabels] = useState('');
    const [useCustomLabels, setUseCustomLabels] = useState(false);
    const [showSamples, setShowSamples] = useState(false);
    const textareaRef = useRef(null);

    const stats = useMemo(() => calculateStats(text), [text]);

    // Save to localStorage when text changes
    useEffect(() => {
        localStorage.setItem(STORAGE_KEY, text);
    }, [text]);

    const handleSubmit = (e) => {
        if (e) e.preventDefault();

        const labels = useCustomLabels && customLabels
            ? customLabels.split(',').map(l => l.trim()).filter(l => l)
            : null;

        onAnalyze(text, labels);
    };

    const handleClear = () => {
        setText('');
        setCustomLabels('');
        localStorage.removeItem(STORAGE_KEY);
        textareaRef.current?.focus();
    };

    const handleSampleSelect = (sample) => {
        setText(sample.text);
        setShowSamples(false);
        textareaRef.current?.focus();
    };

    // Keyboard shortcuts
    useEffect(() => {
        const handleKeyDown = (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                if (text.length >= 10 && !loading) {
                    e.preventDefault();
                    handleSubmit();
                }
            }
            if (e.key === 'Escape') {
                setShowSamples(false);
                if (!showSamples) handleClear();
            }
        };

        document.addEventListener('keydown', handleKeyDown);
        return () => document.removeEventListener('keydown', handleKeyDown);
    }, [text, loading, customLabels, useCustomLabels, showSamples]);

    const getValidationMessage = () => {
        if (text.length === 0) return null;
        if (text.length < 10) return `Need ${10 - text.length} more characters`;
        return null;
    };

    return (
        <form onSubmit={handleSubmit} className="analysis-form">
            <div className="form-group">
                <div className="label-row">
                    <label htmlFor="text">Text to Analyze</label>
                    <div className="label-actions">
                        <button
                            type="button"
                            className="btn-sample"
                            onClick={() => setShowSamples(!showSamples)}
                        >
                            Try Sample
                        </button>
                        <span className="keyboard-hint">Ctrl+Enter to submit</span>
                    </div>
                </div>

                {showSamples && (
                    <div className="sample-menu">
                        {SAMPLE_TEXTS.map((sample, i) => (
                            <button
                                key={i}
                                type="button"
                                onClick={() => handleSampleSelect(sample)}
                            >
                                {sample.label}
                            </button>
                        ))}
                    </div>
                )}

                <textarea
                    ref={textareaRef}
                    id="text"
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    placeholder="Paste your article, paragraph, or note here..."
                    rows={10}
                    required
                    minLength={10}
                    maxLength={50000}
                    className={getValidationMessage() ? 'has-warning' : ''}
                />

                <div className="form-footer">
                    <TextStats stats={stats} />
                    <CharacterProgress current={text.length} max={50000} />
                </div>

                {getValidationMessage() && (
                    <div className="validation-hint">{getValidationMessage()}</div>
                )}
            </div>

            <div className="form-group checkbox-group">
                <label>
                    <input
                        type="checkbox"
                        checked={useCustomLabels}
                        onChange={(e) => setUseCustomLabels(e.target.checked)}
                    />
                    Use custom categories
                </label>
            </div>

            {useCustomLabels && (
                <div className="form-group">
                    <label htmlFor="labels">Custom Categories (comma-separated)</label>
                    <input
                        id="labels"
                        type="text"
                        value={customLabels}
                        onChange={(e) => setCustomLabels(e.target.value)}
                        placeholder="e.g., technology, politics, sports"
                    />
                    <small>Default: technology, politics, sports, entertainment, business, health, science</small>
                </div>
            )}

            <div className="button-group">
                <button type="submit" className="btn-primary" disabled={loading || text.length < 10}>
                    {loading ? 'Analyzing...' : 'Analyze Text'}
                </button>
                <button type="button" className="btn-secondary" onClick={handleClear} disabled={loading}>
                    Clear
                </button>
            </div>
        </form>
    );
};
