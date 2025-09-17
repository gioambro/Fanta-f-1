import sqlite3
from werkzeug.security import generate_password_hash

# Connessione al DB (se non esiste viene creato)
conn = sqlite3.connect("users.db")
c = conn.cursor()

# Cancella la tabella se esiste già
c.execute("DROP TABLE IF EXISTS users")

# Crea la tabella utenti
c.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

# Giocatori e password
users = [
    ("alfarumeno", "1234"),
    ("StrollingAround", "1234"),
    ("Stalloni", "1234"),
    ("WCinGeriatria", "1234"),
    ("Vodkaredbull", "1234"),
    ("Spartaboyz", "1234")
]

# Inserimento utenti con password criptata
for username, pwd in users:
    hashed_pwd = generate_password_hash(pwd)
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pwd))

# Salva e chiudi
conn.commit()
conn.close()

print("Database creato con successo con i 6 giocatori!")
