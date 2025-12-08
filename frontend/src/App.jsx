/**
 * Main App component with routing.
 */
import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthPage } from './pages/AuthPage';
import { AnalyzePage } from './pages/AnalyzePage';
import { useAuth } from './hooks/useAuth';

const ProtectedRoute = ({ children }) => {
    const { isAuthenticated, loading } = useAuth();

    if (loading) {
        return <div className="loading-page">Loading...</div>;
    }

    return isAuthenticated ? children : <Navigate to="/auth" />;
};

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/auth" element={<AuthPage />} />
                <Route
                    path="/analyze"
                    element={
                        <ProtectedRoute>
                            <AnalyzePage />
                        </ProtectedRoute>
                    }
                />
                <Route path="/" element={<Navigate to="/analyze" />} />
            </Routes>
        </BrowserRouter>
    );
}

export default App;
