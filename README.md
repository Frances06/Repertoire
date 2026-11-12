# Repertoire

A personal portfolio built with Flask, HTML, CSS, JavaScript and SQLite. It brings together selected projects, a little information about me, and a small curated music player.

## Features

- Portfolio pages for Home, Projects, About and Contact
- Light, dark and high-contrast colour themes
- Responsive layout and keyboard-friendly controls
- Compact, expandable music player with a dismissible first-visit hint
- Curated audio playlist served from `static/audio/`
- Project catalogue stored in `projects.json`

## Run locally

1. Clone this repository.
2. Create and activate a virtual environment.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start Flask:

   ```bash
   flask --app app run
   ```

5. Open `http://127.0.0.1:5000`.

## Adding music

Place audio files in `static/audio/`. Supported formats are MP3, WAV and OGG. The player lists these files automatically. Visitors can play tracks but cannot upload or delete files.

## Project data

The Projects page reads from the existing `projects.db` SQLite database. This is separate from the retired assignment-only admin and contact-message databases.

## Technologies

- Python and Flask
- HTML, CSS and JavaScript
- SQLite
- Jinja templates
