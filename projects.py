import sqlite3

conn = sqlite3.connect('projects.db')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    short_desc TEXT NOT NULL,
    image_path TEXT NOT NULL,
    download_path TEXT NOT NULL
)''')

cur.execute('INSERT INTO projects (name, type, short_desc, image_path, download_path) VALUES (?, ?, ?,  ?, ?)',
            ("Cows and Bulls", "game", "A game where the player has to guess the number based on the given hints.", "Bulls & Cows.png", "Bulls & Cows.zip"))

cur.execute('INSERT INTO projects (name, type, short_desc, image_path, download_path) VALUES (?, ?, ?, ?, ?)',
            ("To-do List Manager", "tool", "A command-line To-Do List Manager", "To-Do.png", "todo.sh"))

conn.commit()
conn.close()

def get_db():
    conn = sqlite3.connect("projects.db")
    return conn