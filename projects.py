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

cur.execute('INSERT INTO projects (name, type, image_path, short_desc, download_path) VALUES (?, ?, ?, ?, ?)',
            ("Project Nova", "game", "A battleships-esque game where the player, as either the explorer or hunter, attempts to rescue/save some marine creatures.",
            "project-nova.png", ""))

cur.execute('INSERT INTO projects (name, image_path, short_desc, download_path) VALUES (?, ?, ?,  ?, ?)',
            ("Cows and Bulls", "game", "A game where the player has to guess the number based on the given hints.", "", ""))

cur.execute('INSERT INTO projects (name, type, image_path, short_desc, download_path) VALUES (?, ?, ?, ?, ?)',
            ("To-do List Manager", "tool", "A command-line To-Do List Manager", "", ""))

cur.execute('INSERT INTO projects (name, type, image_path, short_desc, download_path) VALUES (?, ?, ?, ?, ?)',
            ("Britannia Air ", "tool", "A program usedd to analyse the performance of a fictional airline", "", ""))

#conn.commit()
conn.close()

def get_db():
    conn = sqlite3.connect("projects.db")
    conn.row_factory = sqlite3.Row
    return conn