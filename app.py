import os
import sqlite3

from flask import Flask, jsonify, render_template, send_from_directory

app = Flask(__name__)

# Audio is curated by the site owner and stored in static/audio.
AUDIO_FOLDER = os.path.join(app.static_folder, "audio")
ALLOWED_AUDIO_EXTENSIONS = {".mp3", ".wav", ".ogg"}
os.makedirs(AUDIO_FOLDER, exist_ok=True)


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/projects")
def projects():
    conn = sqlite3.connect("projects.db")
    try:
        cards = conn.execute("SELECT * FROM projects").fetchall()
    finally:
        conn.close()
    return render_template("projects.html", projects=cards)


@app.route("/project-files/<path:filename>")
def download_project(filename):
    return send_from_directory(os.path.join(app.root_path, "projects"), filename, as_attachment=True)


@app.route("/api/playlist")
def playlist():
    tracks = []
    for filename in sorted(os.listdir(AUDIO_FOLDER)):
        if os.path.splitext(filename)[1].lower() in ALLOWED_AUDIO_EXTENSIONS:
            tracks.append({
                "title": os.path.splitext(filename)[0].replace("_", " "),
                "src": f"/static/audio/{filename}",
            })
    return jsonify(tracks)


if __name__ == "__main__":
    app.run()
