import sqlite3
from werkzeug.security import generate_password_hash

DB_FILE = "users.db"

# Cancella e ricrea il DB
conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS users")
cur.execute("DROP TABLE IF EXISTS formazioni")

cur.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
""")

cur.execute("""
    CREATE TABLE formazioni (
        username TEXT PRIMARY KEY,
        pilota1 TEXT,
        pilota2 TEXT
    )
""")

# Lista utenti iniziali
utenti = [
    ("admin", generate_password_hash("1234"), "admin"),
    ("Alfarumeno", generate_password_hash("1234"), "player"),
    ("Stalloni", generate_password_hash("1234"), "player"),
    ("WC in Geriatria", generate_password_hash("1234"), "player"),
    ("Strolling Around", generate_password_hash("1234"), "player"),
    ("Spartaboyz", generate_password_hash("1234"), "player"),
    ("Vodkaredbull", generate_password_hash("1234"), "player"),
]

cur.executemany("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", utenti)
conn.commit()
conn.close()

print("✅ Database users.db creato con utenti iniziali e tabella formazioni!")
