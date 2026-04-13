import sqlite3

conn = sqlite3.connect("arcade.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT    UNIQUE NOT NULL,
    password TEXT    NOT NULL,
    score    INTEGER DEFAULT 0
)
""")

conn.commit()
conn.close()
print("✅ arcade.db ready.")
