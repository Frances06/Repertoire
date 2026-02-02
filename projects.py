import sqlite3

conn = sqlite3.connect('projects.db')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    image_url TEXT NOT NULL,
    short_desc TEXT NOT NULL
)''')


# Note: Might need to edit my upload functions to reuse them to upload images for this)