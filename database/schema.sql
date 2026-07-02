
-- Cyber Defense & Threat Correlation Platform Database Schema

CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    source TEXT NOT NULL,
    event_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    raw_log TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS iocs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    indicator TEXT NOT NULL,
    type TEXT NOT NULL,
    confidence INTEGER,
    detected_at TEXT
);

CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    severity TEXT NOT NULL,
    status TEXT DEFAULT 'Open',
    created_at TEXT
);

CREATE TABLE IF NOT EXISTS mitre_mapping (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    technique_id TEXT,
    technique_name TEXT,
    tactic TEXT,
    alert_id INTEGER
);

CREATE TABLE IF NOT EXISTS risk_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name TEXT,
    score INTEGER,
    risk_level TEXT
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password_hash TEXT,
    role TEXT
);
