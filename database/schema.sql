-- Hybrid-Analyzer Database Schema
-- PostgreSQL database schema for users and analysis logs

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create index on username and email for faster lookups
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Create analysis_logs table
CREATE TABLE IF NOT EXISTS analysis_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    input_text TEXT NOT NULL,
    category VARCHAR(100),
    confidence_score FLOAT,
    summary TEXT,
    tone VARCHAR(20),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create index on user_id for faster queries
CREATE INDEX IF NOT EXISTS idx_analysis_logs_user_id ON analysis_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_analysis_logs_created_at ON analysis_logs(created_at);

-- Add comments for documentation
COMMENT ON TABLE users IS 'Stores user authentication information';
COMMENT ON TABLE analysis_logs IS 'Stores history of text analysis requests and results';
COMMENT ON COLUMN users.password_hash IS 'Bcrypt hashed password';
COMMENT ON COLUMN analysis_logs.confidence_score IS 'Hugging Face classification confidence (0-1)';
COMMENT ON COLUMN analysis_logs.tone IS 'Detected tone: positive, neutral, or negative';
