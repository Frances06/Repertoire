import os
import sqlite3
from flask import Flask, url_for, redirect, render_template, jsonify, request, send_from_directory, flash
from flask_login import LoginManager, login_user, login_required, logout_user
from models.user import User
from projects import get_db
import argon2
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)

# Secret key for session management (used for cookies and security purposes)
app.config['SECRET_KEY'] = '{}'.format(os.urandom(24))

# Set up Flask-Login for user authentication and session management
login_manager = LoginManager(app)
login_manager.login_view = "login"  # Redirect to login view if not authenticated
login_manager.login_message = None  # Disable default login message

# Set the upload folder and allowed file extensions for uploaded files
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"mp3", "wav", "ogg"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure that the upload directory exists

# Load user function to get the user by their ID (for authentication)
@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

# Function to check if uploaded file is allowed (checks extension)
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Home page route (accessible without authentication)
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

# Contact page route (accessible without authentication)
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Route to handle form submission for adding a message (from the contact page)
@app.route('/contact/add_message', methods=['POST'])
def add_message():
    # Get form data (name, email, message)
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    try:
        # Connect to SQLite database
        conn = sqlite3.connect('messages.db')
        c = conn.cursor()

        # Create messages table if it doesn't exist
        c.execute('''CREATE TABLE IF NOT EXISTS messages
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    message TEXT NOT NULL)''')

        # Insert the new message into the table
        c.execute('INSERT INTO messages (name, email, message) VALUES (?, ?, ?)', (name, email, message))
        conn.commit()

        # Fetch all messages (for debugging purposes)
        rows = c.execute('SELECT * FROM messages').fetchall()
        print(rows)  # Debugging

        conn.close()  # Close connection

        status = "Message sent successfully!"  # Success status

    except:
        status = "Sorry, there was an error sending your message./nPlease try again."  # Error handling

    # Return the status as a JSON response
    return { "status": status }

# Route to view messages (only accessible to logged-in users)
@app.route('/view-messages')
@login_required  # Ensure only logged-in users can access this page
def view_messages():
    # Connect to the database and fetch all messages
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    rows = c.execute('SELECT * FROM messages').fetchall()
    conn.close()

    # Render the view_messages template with the fetched messages
    return render_template('view_messages.html', messages=rows)

# About page route (accessible without authentication)
@app.route('/about')
def about():
    return render_template('about.html')

# Projects page route (fetches project data from the database and renders the template)
@app.route('/projects')
def projects():
    db = get_db  # Fetch the database object
    cards = db.execute('SELECT * FROM projects').fetchall()  # Fetch all projects from the DB
    conn.close()  # Close the database connection
    return render_template('projects.html', projects=cards)

# API route to get a list of uploaded music files as a playlist
@app.route("/api/playlist")
def playlist():
    files = []

    # Loop through the files in the upload folder
    for filename in os.listdir(app.config["UPLOAD_FOLDER"]):
        # Check if the file extension is allowed
        if allowed_file(filename):
            files.append({
                "title": filename.rsplit(".", 1)[0],  # Extract the file name without the extension
                "src": f"/uploads/{filename}",  # Generate the file's URL
                "filename": filename  # Include the full filename
            })

    # Return the list of files as a JSON response
    return jsonify(files)

# Route to handle file uploads (limit of 15 tracks)
@app.route("/upload", methods=["POST"])
def upload_file():
    # Check if the upload limit is reached (15 files max)
    if len(os.listdir(app.config["UPLOAD_FOLDER"])) >= 15:
        return jsonify({"error": "Track limit reached (15 songs max)."}), 400

    # Check if the file is part of the request
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]

    # Check if the file has a valid filename
    if file.filename == "":
        return jsonify({"error": "No filename"}), 400

    # Check if the file has a valid extension
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400

    filename = secure_filename(file.filename)  # Secure the filename
    file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))  # Save the file to the upload folder

    # Return a JSON response with the file's title and URL
    return jsonify({
        "title": filename.rsplit(".", 1)[0],
        "src": f"/uploads/{filename}"
    })

# Route to serve uploaded files
@app.route("/uploads/<path:filename>")
def uploads(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

# Route to handle track deletion (used for removing files from the server)
@app.route("/delete", methods=["POST"])
def delete_track():
    data = request.json
    filename = data.get("filename")

    # Check if the filename is provided
    if not filename:
        return jsonify({"error": "No filename provided"}), 400

    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    # Check if the file exists
    if not os.path.exists(path):
        return jsonify({"error": "File not found"}), 404

    # Delete the file
    os.remove(path)
    return jsonify({"success": True})

# Login route (GET displays the login form, POST processes the login)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    # Get form data (username and password)
    username = request.form.get('username')
    password = request.form.get('password')

    # Connect to the admin database to verify login credentials
    conn = sqlite3.connect('admin.db')
    c = conn.cursor()
    c.execute('SELECT * FROM admin WHERE username = ?', (username,))
    admin = c.fetchone()
    conn.close()

    # Check if the admin exists and if the password is correct
    if admin:
        ph = argon2.PasswordHasher()  # Password hashing library
        try:
            # Verify the provided password matches the hashed password in the DB
            ph.verify(admin[2], password)  # admin[2] is the hashed password column
            user = User(id=admin[0], username=admin[1])  # Create a User object
            login_user(user)  # Log the user in
            return redirect(url_for('view_messages'))  # Redirect to the messages view
        except argon2.exceptions.VerifyMismatchError:
            flash("Invalid credentials", "error")
            return redirect(url_for('login'))  # Redirect back to the login page on failure
    else:
        flash("Invalid credentials", "error")
        return redirect(url_for('login'))  # Redirect back to login page if user not found

# Logout route (logs out the user and redirects to the home page)
@app.route('/logout')
def logout():
    logout_user()  # Log out the current user
    return redirect(url_for('home'))  # Redirect to the home page

# Run the app in debug mode if the script is run directly
if __name__ == '__main__':
    app.run(debug=True)