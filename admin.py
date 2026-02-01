import sqlite3
import argon2

db = sqlite3.connect('admin.db')
cur = db.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
)''')

cur.execute('''CREATE TRIGGER IF NOT EXISTS admin_limit
    BEFORE INSERT ON admin
    WHEN (SELECT COUNT(*) FROM admin) >= 1
    BEGIN
        SELECT RAISE(ABORT, 'Only one admin allowed');
    END;
''')

def create_admin(username, password):
    ph = argon2.PasswordHasher()
    password_hash = ph.hash(password)
    try:
        cur.execute('INSERT INTO admin (username, password_hash) VALUES (?, ?)', (username, password_hash))
        db.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    
create_admin('admin', 'StrongPassword123!')