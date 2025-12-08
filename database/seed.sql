-- Seed data for testing
-- Example users and analysis logs

-- Insert test users (passwords are hashed version of 'testpassword123')
INSERT INTO users (username, email, password_hash) VALUES
('testuser1', 'test1@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzS.sC'),
('testuser2', 'test2@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzS.sC')
ON CONFLICT (username) DO NOTHING;

-- Insert sample analysis logs
INSERT INTO analysis_logs (user_id, input_text, category, confidence_score, summary, tone) VALUES
(1, 'Artificial intelligence is transforming the technology industry...', 'technology', 0.95, 'This article discusses AI advancements in tech.', 'positive'),
(1, 'The political landscape is changing rapidly...', 'politics', 0.88, 'Analysis of current political trends.', 'neutral'),
(2, 'New breakthrough in cancer research shows promise...', 'health', 0.92, 'Scientists discover new cancer treatment approach.', 'positive')
ON CONFLICT DO NOTHING;
