import sqlite3
from werkzeug.security import generate_password_hash

DB_FILE = "users.db"

conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

# Crea tabella utenti
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
)
""")

# Inserisci admin
cur.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
            ("admin", generate_password_hash("1234"), "admin"))

# Inserisci i giocatori
giocatori = [
    ("Alfarumeno", "1111"),
    ("Stalloni", "2222"),
    ("WC in Geriatria", "3333"),
    ("Strolling Around", "4444"),
    ("Spartaboyz", "5555"),
    ("Vodkaredbull", "6666")
]

for username, pwd in giocatori:
    cur.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, generate_password_hash(pwd), "player"))

conn.commit()
conn.close()

print("✅ Database inizializzato con admin e giocatori!")
