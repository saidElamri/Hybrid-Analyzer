/**
 * Analysis page for text analysis interface.
 */
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { AnalysisForm } from '../components/AnalysisForm';
import { ResultsDisplay } from '../components/ResultsDisplay';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { ErrorMessage } from '../components/ErrorMessage';
import { Toast } from '../components/Toast';
import { AnalysisHistory, saveToHistory } from '../components/AnalysisHistory';
import { analysisService } from '../services/analysis';
import { useAuth } from '../hooks/useAuth';

export const AnalyzePage = () => {
    const [results, setResults] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [lastRequest, setLastRequest] = useState(null);
    const [toast, setToast] = useState('');
    const [historyKey, setHistoryKey] = useState(0);
    const { user, logout } = useAuth();
    const navigate = useNavigate();

    const handleAnalyze = async (text, customLabels) => {
        setError('');
        setLoading(true);
        setResults(null);
        setToast('');
        setLastRequest({ text, customLabels });

        try {
            const data = await analysisService.analyzeText(text, customLabels);
            setResults(data);
            saveToHistory(data);
            setHistoryKey(k => k + 1); // Force history refresh
            setToast('Analysis complete');
        } catch (err) {
            setError(err.response?.data?.detail || 'Analysis failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const handleRetry = () => {
        if (lastRequest) {
            handleAnalyze(lastRequest.text, lastRequest.customLabels);
        }
    };

    const handleHistorySelect = (item) => {
        setResults(item);
        setToast('Loaded from history');
    };

    const handleLogout = () => {
        logout();
        navigate('/auth');
    };

    return (
        <div className="analyze-page">
            <header className="app-header">
                <div className="header-content">
                    <h1>Hybrid-Analyzer</h1>
                    <div className="user-info">
                        <span>Welcome, {user?.username}</span>
                        <button onClick={handleLogout} className="btn-logout">
                            Logout
                        </button>
                    </div>
                </div>
            </header>

            <main className="main-content">
                <div className="content-container">
                    <div className="page-intro">
                        <h2>Analyze Your Text</h2>
                        <p>
                            Classify content with Hugging Face and generate summaries with Google Gemini.
                        </p>
                    </div>

                    <AnalysisHistory key={historyKey} onSelect={handleHistorySelect} />

                    <ErrorMessage
                        message={error}
                        onClose={() => setError('')}
                        onRetry={lastRequest ? handleRetry : null}
                    />

                    <AnalysisForm onAnalyze={handleAnalyze} loading={loading} />

                    {loading && <LoadingSpinner />}

                    {results && <ResultsDisplay results={results} />}

                    {!loading && !results && !error && (
                        <div className="empty-state">
                            <p>Enter text above to start analyzing</p>
                        </div>
                    )}
                </div>
            </main>

            <footer className="app-footer">
                <p>Hybrid-Analyzer v1.0 • Powered by Hugging Face & Google Gemini</p>
            </footer>

            <Toast message={toast} onClose={() => setToast('')} />
        </div>
    );
};
