import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name="gunny_bag.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS detection (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image TEXT,
                count INTEGER,
                date TEXT,
                time TEXT
            )
            """
        )
        self.conn.commit()

    def save_count(self, image_name, count):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")

        cursor.execute(
            "INSERT INTO detection (image, count, date, time) VALUES (?, ?, ?, ?)",
            (image_name, count, date, time),
        )

        conn.commit()
        conn.close()

    def get_history(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT image, count, date, time FROM detection ORDER BY id DESC")
        rows = cursor.fetchall()
        conn.close()
        return rows
