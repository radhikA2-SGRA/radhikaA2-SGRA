-- PostgreSQL reference schema. The FastAPI startup creates the initial tables for local development.
CREATE TABLE users (id SERIAL PRIMARY KEY, name VARCHAR(120) NOT NULL, email VARCHAR(255) UNIQUE NOT NULL, password_hash VARCHAR(255) NOT NULL, role VARCHAR(20) NOT NULL DEFAULT 'student', created_at TIMESTAMP NOT NULL DEFAULT now());
CREATE TABLE student_profiles (id SERIAL PRIMARY KEY, user_id INTEGER UNIQUE REFERENCES users(id), state VARCHAR(80), city VARCHAR(80), education_level VARCHAR(80), tenth_percentage NUMERIC, twelfth_percentage NUMERIC, career_goal VARCHAR(160), interests TEXT, updated_at TIMESTAMP NOT NULL DEFAULT now());
CREATE TABLE opportunities (id SERIAL PRIMARY KEY, kind VARCHAR(30) NOT NULL, name VARCHAR(200) NOT NULL, provider VARCHAR(200) NOT NULL, description TEXT NOT NULL, source_url VARCHAR(500), verification_status VARCHAR(30) NOT NULL, is_demo BOOLEAN NOT NULL DEFAULT true, last_verified_date TIMESTAMP);
CREATE INDEX opportunities_kind_idx ON opportunities(kind);
CREATE TABLE questions (id SERIAL PRIMARY KEY, text TEXT NOT NULL, category VARCHAR(50) NOT NULL, options TEXT NOT NULL, answer VARCHAR(100) NOT NULL, marks INTEGER NOT NULL DEFAULT 1);
