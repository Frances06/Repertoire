import sqlite3

conn = sqlite3.connect('projects.db')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    image_url TEXT NOT NULL,
    short_desc TEXT NOT NULL
)''')

cur.execute('INSERT INTO projects (name, image_url, short_desc) VALUES (?, ?, ?)',
            ("Project Nova", "project-nova.png", "A battle-ships like game where the player, a seither the explorer or hunter, attempts to rescue/save some marine creatures."))

conn.close()

def get_db():
    conn = sqlite3.connect("projects.db")
    conn.row_factory = sqlite3.Row
    return conn