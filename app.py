import os
import sqlite3
from flask import Flask, url_for, redirect, render_template, jsonify, request, send_from_directory, flash
from flask_login import LoginManager, login_user, login_required, logout_user
from models.user import User
import argon2
from werkzeug.utils import secure_filename
from flask import flash, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = '{}'.format(os.urandom(24)) # Secret key for session management
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = None

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"mp3", "wav", "ogg"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/home')
def home():
    return render_template('base.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/contact/add_message', methods=['POST'])
def add_message():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    try:
        conn = sqlite3.connect('messages.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS messages
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    message TEXT NOT NULL)''')
        
        c.execute('INSERT INTO messages (name, email, message) VALUES (?, ?, ?)', (name, email, message))
        conn.commit()
        rows = c.execute('SELECT * FROM messages').fetchall()
        print(rows)  # For debugging purposes
        conn.close()

        status = "Message sent successfully!"

    except:
        status = "Sorry, there was an error sending your message./nPlease try again."

    return { "status": status }
    
@app.route('/view-messages')
@login_required # Ensure only logged-in admin can view messages
def view_messages():
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    rows = c.execute('SELECT * FROM messages').fetchall()
    conn.close()
    return render_template('view_messages.html', messages=rows)

@app.route('/')
def redirect_to_home():
    return redirect(url_for('home'))



'''@app.route("/api/playlist")
def playlist():
    return jsonify([
        {"title": "User Song 1", "src": "/uploads/song1.mp3"},
        {"title": "User Song 2", "src": "/uploads/song2.mp3"},
        {"title": "User Song 3", "src": "/uploads/song3.mp3"}
    ])'''

@app.route("/api/playlist")
def playlist():
    files = []

    for filename in os.listdir(app.config["UPLOAD_FOLDER"]):
        if allowed_file(filename):
            files.append({
                "title": filename.rsplit(".", 1)[0],
                "src": f"/uploads/{filename}",
                "filename": filename
            })

    return jsonify(files)


@app.route("/upload", methods=["POST"])
def upload_file():
    # limit to 15 tracks
    if len(os.listdir(app.config["UPLOAD_FOLDER"])) >= 15:
        return jsonify({"error": "Track limit reached (15 songs max)."}), 400
    
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No filename"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400

    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

    return jsonify({
        "title": filename.rsplit(".", 1)[0],
        "src": f"/uploads/{filename}"
    })

@app.route("/uploads/<path:filename>")
def uploads(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/delete", methods=["POST"])
def delete_track():
    data = request.json
    filename = data.get("filename")

    if not filename:
        return jsonify({"error": "No filename provided"}), 400

    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    if not os.path.exists(path):
        return jsonify({"error": "File not found"}), 404

    os.remove(path)
    return jsonify({"success": True})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form.get('username')
    password = request.form.get('password')

    conn = sqlite3.connect('admin.db')
    c = conn.cursor()
    c.execute('SELECT * FROM admin WHERE username = ?', (username,))
    admin = c.fetchone()
    conn.close()

    if admin:
        ph = argon2.PasswordHasher()
        try:
            ph.verify(admin[2], password)  # admin[3] is the password_hash column
            user = User(id=admin[0], username=admin[1])
            login_user(user)  # admin[1] is the username column
            flash("Login successful!", "success")
            return redirect(url_for('view_messages'))
        except argon2.exceptions.VerifyMismatchError:
            flash("Invalid credentials", "error")
            return redirect(url_for('login'))
    else:
        flash("Invalid credentials", "error")
        return redirect(url_for('login'))
            
@app.route('/logout')
def logout():
    logout_user()
    return 'Logged out'

if __name__ == '__main__':
    app.run(debug=True)