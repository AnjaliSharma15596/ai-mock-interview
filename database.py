import sqlite3
import hashlib
import os

DB_PATH = "interview_app.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    c = conn.cursor()

    # Users table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Interviews table
    c.execute("""
        CREATE TABLE IF NOT EXISTS interviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            job_role TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            overall_score REAL,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Interview questions + answers table
    c.execute("""
        CREATE TABLE IF NOT EXISTS interview_answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            interview_id INTEGER NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            feedback TEXT,
            score INTEGER,
            FOREIGN KEY (interview_id) REFERENCES interviews(id)
        )
    """)

    conn.commit()
    conn.close()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(name, email, password):
    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, hash_password(password))
        )
        conn.commit()
        conn.close()
        return True, "Registration successful!"
    except sqlite3.IntegrityError:
        return False, "Email already exists. Please login."


def login_user(email, password):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "SELECT * FROM users WHERE email = ? AND password = ?",
        (email, hash_password(password))
    )
    user = c.fetchone()
    conn.close()
    if user:
        return True, dict(user)
    return False, "Invalid email or password."


def save_interview(user_id, job_role, difficulty, overall_score, questions, answers, feedbacks, scores):
    conn = get_connection()
    c = conn.cursor()

    c.execute(
        "INSERT INTO interviews (user_id, job_role, difficulty, overall_score) VALUES (?, ?, ?, ?)",
        (user_id, job_role, difficulty, overall_score)
    )
    interview_id = c.lastrowid

    for q, a, f, s in zip(questions, answers, feedbacks, scores):
        c.execute(
            "INSERT INTO interview_answers (interview_id, question, answer, feedback, score) VALUES (?, ?, ?, ?, ?)",
            (interview_id, q, a, f, s)
        )

    conn.commit()
    conn.close()
    return interview_id


def get_user_interviews(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "SELECT * FROM interviews WHERE user_id = ? ORDER BY completed_at DESC",
        (user_id,)
    )
    interviews = [dict(row) for row in c.fetchall()]
    conn.close()
    return interviews


def get_interview_details(interview_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM interview_answers WHERE interview_id = ?", (interview_id,))
    details = [dict(row) for row in c.fetchall()]
    conn.close()
    return details
