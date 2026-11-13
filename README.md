# Repertoire

A personal portfolio built with Flask, HTML, CSS and JavaScript. It brings together selected projects, a little information about me, and a small music player.

## Features

- Portfolio pages for Home, Projects, About and Contact
- Light, dark and high-contrast colour themes
- Responsive layout and keyboard-friendly controls
- Compact, expandable music player with a dismissible first-visit hint
- Audio uploads (MP3, WAV and OGG), with a maximum of 15 uploaded tracks
- Curated audio can also be placed in `static/audio/`
- Project catalogue loaded from `projects.json`

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

Open the expanded player and use the upload icon to choose an MP3, WAV or OGG file from your computer. Uploaded tracks are saved in the local `uploads/` folder, which is excluded from Git so personal audio files are not committed to the public repository. The upload limit is 15 tracks. To include curated tracks with the site itself, place them in `static/audio/`.

## Project data

The Projects page currently reads its catalogue from `projects.json`.

## Technologies

- Python and Flask
- HTML, CSS and JavaScript
- Jinja templates
