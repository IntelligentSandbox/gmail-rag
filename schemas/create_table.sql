CREATE EXTENSION IF NOT EXISTS vector;

-- 384 dimensional dense vector space https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2

CREATE TABLE IF NOT EXISTS email_vectors (
    id SERIAL PRIMARY KEY,
    email_id VARCHAR(255) NOT NULL UNIQUE,
    sender VARCHAR(255),
    recipient VARCHAR(255),
    subject TEXT,
    body TEXT,
    content TEXT,
    date TEXT,
    thread_id VARCHAR(255),
    embedding vector(384),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_email_vectors_email_id ON email_vectors(email_id);
CREATE INDEX IF NOT EXISTS idx_email_vectors_sender ON email_vectors(sender);
CREATE INDEX IF NOT EXISTS idx_email_vectors_thread_id ON email_vectors(thread_id);
CREATE INDEX IF NOT EXISTS idx_email_vectors_date ON email_vectors(date);