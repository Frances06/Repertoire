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
            ("Project Nova", ""))