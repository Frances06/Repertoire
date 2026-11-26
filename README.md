<div align="center">

# Repertoire

### Projects, ideas and a little music.

A Flask-powered portfolio bringing together selected software projects, a little information about me, and a built-in music player.

[![Python](https://img.shields.io/badge/Python-Flask-1f425f?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-web%20app-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![JavaScript](https://img.shields.io/badge/JavaScript-interactive-f7df1e?logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

</div>

---

## Overview

This is a personal portfolio built with **Python, Flask, HTML, CSS and JavaScript**. It is designed to be simple to explore, responsive across screen sizes, and comfortable to use with a keyboard.

## Highlights

| Portfolio | Personalisation | Music player |
|---|---|---|
| Home, Projects, About and Contact pages | Light, dark and high-contrast themes | Compact player that expands when needed |
| Project catalogue managed through `projects.json` | Responsive layout and keyboard-friendly controls | Upload MP3, WAV and OGG files |
| A place to showcase selected work | Clear focus indicators and accessible controls | Supports up to 15 uploaded tracks |

Curated audio files can also be included in `static/audio/`.

## Getting started

### Requirements

- Python
- pip

### Run locally

1. Clone the repository:

   ```bash
   git clone https://github.com/Frances06/Repertoire.git
   cd Repertoire
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   ```

   **Windows (PowerShell):**
   ```powershell
   .venv\Scripts\Activate.ps1
   ```

   **macOS / Linux:**
   ```bash
   source .venv/bin/activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the Flask development server:

   ```bash
   flask --app app run
   ```

5. Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

## Adding music

Open the expanded music player and select the upload icon to choose an MP3, WAV or OGG file.

- Uploaded tracks are stored locally in the `uploads/` folder.
- The upload limit is 15 tracks.
- The `uploads/` folder is excluded from Git, so personal audio files are not committed to the repository.
- To include curated tracks with the site, place them in `static/audio/`.

## Project catalogue

The Projects page loads its catalogue from `projects.json`. Update that file to add or edit the projects displayed on the portfolio.

## Built with

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript
- **Templates:** Jinja

---

<div align="center">
  <sub>Built as a personal space to share projects and keep learning.</sub>
</div>
