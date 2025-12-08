/**
 * Authentication page with login/register toggle.
 */
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { LoginForm } from '../components/LoginForm';
import { RegisterForm } from '../components/RegisterForm';
import { useAuth } from '../hooks/useAuth';

export const AuthPage = () => {
    const [isLogin, setIsLogin] = useState(true);
    const { login, register } = useAuth();
    const navigate = useNavigate();

    const handleLogin = async (username, password) => {
        await login(username, password);
        navigate('/analyze');
    };

    const handleRegister = async (username, email, password) => {
        await register(username, email, password);
        navigate('/analyze');
    };

    return (
        <div className="auth-page">
            <div className="auth-container">
                <div className="auth-header">
                    <h1>Hybrid-Analyzer</h1>
                    <p>AI-Powered Text Analysis with Hugging Face & Gemini</p>
                </div>

                {isLogin ? (
                    <LoginForm
                        onLogin={handleLogin}
                        onSwitchToRegister={() => setIsLogin(false)}
                    />
                ) : (
                    <RegisterForm
                        onRegister={handleRegister}
                        onSwitchToLogin={() => setIsLogin(true)}
                    />
                )}
            </div>
        </div>
    );
};
