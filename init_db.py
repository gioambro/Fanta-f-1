import sqlite3
from werkzeug.security import generate_password_hash

DB_FILE = "users.db"

# Giocatori e i loro piloti
players = {
    "alfarumeno": ["Norris", "Tsunoda", "Colapinto"],
    "StrollingAround": ["Russell", "Gasly", "Antonelli"],
    "Stalloni": ["Piastri", "Lawson", "Ocon"],
    "WCinGeriatria": ["Alonso", "Hamilton", "Hadjar"],
    "Vodkaredbull": ["Verstappen", "Sainz", "Bortoleto"],
    "Spartaboyz": ["Leclerc", "Bearman", "Albon"]
}

# Admin + password di default
users = [
    ("admin", "admin", "admin")
]

# Aggiungiamo i players
for player in players.keys():
    users.append((player, player, "player"))

# Creazione DB
conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

# Creiamo la tabella utenti
cur.execute("DROP TABLE IF EXISTS users")
cur.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
)
""")

# Inseriamo gli utenti
for username, password, role in users:
    cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, generate_password_hash(password), role))

# Creiamo la tabella piloti
cur.execute("DROP TABLE IF EXISTS players")
cur.execute("""
CREATE TABLE players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    driver1 TEXT,
    driver2 TEXT,
    driver3 TEXT
)
""")

# Inseriamo i piloti dei giocatori
for username, drivers in players.items():
    cur.execute("INSERT INTO players (username, driver1, driver2, driver3) VALUES (?, ?, ?, ?)",
                (username, drivers[0], drivers[1], drivers[2]))

conn.commit()
conn.close()

print("✅ Database creato con successo!")
