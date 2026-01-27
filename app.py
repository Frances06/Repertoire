import os
from flask import Flask, url_for, redirect, render_template, jsonify, request, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"mp3", "wav", "ogg"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('base.html')

@app.route('/redirect')
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
                "src": f"/uploads/{filename}"
            })

    return jsonify(files)


@app.route("/upload", methods=["POST"])
def upload_file():
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



if __name__ == '__main__':
    app.run(debug=True)