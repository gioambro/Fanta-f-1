import sqlite3
from werkzeug.security import generate_password_hash

DB_NAME = "fanta.db"

conn = sqlite3.connect(DB_NAME)
cur = conn.cursor()

# Creazione tabella utenti
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    driver1 TEXT,
    driver2 TEXT,
    driver3 TEXT
)
""")

# Utente di test (username: admin / password: admin)
try:
    cur.execute("INSERT INTO users (username, password, driver1, driver2, driver3) VALUES (?, ?, ?, ?, ?)", 
                ("admin", generate_password_hash("admin"), "Leclerc", "Verstappen", "Hamilton"))
except sqlite3.IntegrityError:
    print("Utente admin già presente")

conn.commit()
conn.close()

print("Database inizializzato con successo.")
