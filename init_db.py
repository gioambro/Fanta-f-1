import sqlite3
from werkzeug.security import generate_password_hash

# Connessione al database (verrà creato se non esiste)
conn = sqlite3.connect('users.db')
cur = conn.cursor()

# Creazione tabella utenti se non esiste
cur.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

# Inserimento utenti di prova
cur.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)",
            ("player1", generate_password_hash("password1")))
cur.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)",
            ("player2", generate_password_hash("password2")))

conn.commit()
conn.close()
