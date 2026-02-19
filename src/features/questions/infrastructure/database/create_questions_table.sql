-- SQL Script to create the 'questions' table in PostgreSQL
-- Each question has a unique UUID and is linked to an apiary.

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE IF NOT EXISTS questions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    apiary_id UUID NOT NULL,
    external_id VARCHAR(255), -- Used to identify default questions
    question_text TEXT NOT NULL,
    question_type VARCHAR(50) NOT NULL, -- e.g., 'texto', 'numero', 'opciones', 'rango'
    category VARCHAR(100),
    is_required BOOLEAN NOT NULL DEFAULT FALSE,
    display_order INTEGER NOT NULL DEFAULT 0,
    min_value INTEGER,
    max_value INTEGER,
    options JSONB, -- For multiple choice options
    depends_on VARCHAR(255), -- ID of another question this one depends on
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_apiary FOREIGN KEY (apiary_id) REFERENCES apiaries(id) ON DELETE CASCADE
);

-- Indices for performance
CREATE INDEX IF NOT EXISTS idx_questions_apiary ON questions (apiary_id);
CREATE INDEX IF NOT EXISTS idx_questions_external_id ON questions (apiary_id, external_id);

-- Trigger to update 'updated_at' column
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_questions_updated_at
BEFORE UPDATE ON questions
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();
