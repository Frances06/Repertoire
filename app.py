import os
import json

from flask import Flask, jsonify, render_template, request, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Uploaded audio stays outside the public Git repository.
UPLOAD_FOLDER = os.path.join(app.root_path, "uploads")
AUDIO_FOLDER = os.path.join(app.static_folder, "audio")
ALLOWED_AUDIO_EXTENSIONS = {".mp3", ".wav", ".ogg"}
MAX_UPLOADED_TRACKS = 15

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)


def is_allowed_audio(filename):
    return os.path.splitext(filename)[1].lower() in ALLOWED_AUDIO_EXTENSIONS


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
    with open(os.path.join(app.root_path, "projects.json"), encoding="utf-8") as project_file:
        cards = json.load(project_file)
    return render_template("projects.html", projects=cards)


@app.route("/project-files/<path:filename>")
def download_project(filename):
    return send_from_directory(os.path.join(app.root_path, "projects"), filename, as_attachment=True)


@app.route("/api/playlist")
def playlist():
    tracks = []

    # Curated tracks are shipped with the site.
    for filename in sorted(os.listdir(AUDIO_FOLDER)):
        if is_allowed_audio(filename):
            tracks.append({
                "title": os.path.splitext(filename)[0].replace("_", " "),
                "src": f"/static/audio/{filename}",
                "uploaded": False,
            })

    # Visitor/owner uploads are stored separately and are git-ignored.
    for filename in sorted(os.listdir(UPLOAD_FOLDER)):
        if is_allowed_audio(filename) and os.path.isfile(os.path.join(UPLOAD_FOLDER, filename)):
            tracks.append({
                "title": os.path.splitext(filename)[0].replace("_", " "),
                "src": f"/uploads/{filename}",
                "filename": filename,
                "uploaded": True,
            })

    return jsonify(tracks)


@app.route("/upload", methods=["POST"])
def upload_file():
    uploaded_tracks = [
        name for name in os.listdir(UPLOAD_FOLDER)
        if is_allowed_audio(name) and os.path.isfile(os.path.join(UPLOAD_FOLDER, name))
    ]
    if len(uploaded_tracks) >= MAX_UPLOADED_TRACKS:
        return jsonify({"error": "Track limit reached (15 uploaded tracks maximum)."}), 400

    audio_file = request.files.get("file")
    if audio_file is None:
        return jsonify({"error": "No audio file was provided."}), 400
    if not audio_file.filename:
        return jsonify({"error": "Please choose an audio file."}), 400
    if not is_allowed_audio(audio_file.filename):
        return jsonify({"error": "Unsupported file type. Please choose an MP3, WAV or OGG file."}), 400

    filename = secure_filename(audio_file.filename)
    if not filename:
        return jsonify({"error": "That filename is not valid."}), 400
    destination = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(destination):
        return jsonify({"error": "A track with that filename has already been uploaded."}), 409

    audio_file.save(destination)
    return jsonify({
        "title": os.path.splitext(filename)[0].replace("_", " "),
        "src": f"/uploads/{filename}",
        "filename": filename,
        "uploaded": True,
    }), 201


@app.route("/uploads/<path:filename>")
def uploaded_audio(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


if __name__ == "__main__":
    app.run()
