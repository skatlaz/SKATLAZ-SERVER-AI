import sqlite3
from pathlib import Path

DB_NAME = "bd.sqlite3"

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER,
            source TEXT,
            content TEXT,
            score REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS training_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            answer TEXT,
            source TEXT,
            embedding TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        self.conn.commit()

    def save_question(self, prompt):
        self.cursor.execute(
            "INSERT INTO questions (prompt) VALUES (?)", (prompt,)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def save_response(self, question_id, source, content, score=0):
        self.cursor.execute(
            "INSERT INTO responses (question_id, source, content, score) VALUES (?, ?, ?, ?)",
            (question_id, source, content, score)
        )
        self.conn.commit()
