# Repertoire
Welcome to my personal portfolio web application!
This project is built with Flask and showcases my work — with additional features such as message management and an audio player.<br><br>

## Table of Contents
* [About](#about)
* [Features](#features)
* [Installation](#installation)
* [Usage](#usage)
* [Project Structure](#project-structure)
* [Technologies](#technologies)
* [Asset Log](#asset-log)

<br>

---

## About
This Flask-based web application serves as my online portfolio. It includes a homepage, with previews of the different webpages; a "Projects" page, to showcase my work; an "About" page, containing more information about me;  and a "Contact" page where users can send messages. Only logged-in admin users can view the submitted messages.

Additionally, the website includes an audio player, allowing users to upload audio files (in MP3, AWV or OGG format) to listen to music directly from the browser.

<br>

---

## Features
* **Homepage**: Introduction to the web application and what the user can expect from it.
* **About Page**: Detailed information about my background, experience, and skills.
* **Projects Page**: A showcase of my work and technical projects.
* **Contact Me Page**: My email and phone number, as well as a form where users can send messages to me. Messages are stored in a database.
* **Alternative Themes**: Using the button on the top rightm users can switch between light, dark and high contrast (for better color )
* **Admin View**: Logged-in admins can see submitted messages from the contact form.
* **Audio Player**: An embedded audio player to upload and listen to MP3, WAV, and OGG audio files.

<br>

---

## Installation
1. Download the ZIP file

2. Create a virtual environment in the chosen IDE (optional but recommended)

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```
<br>

---

## Usage
1. Start the Flask development server:

   ```bash
   flask run
   ```

2. Visit the application in your browser:

   ```
   http://127.0.0.1:5000
   ```

3. The app will be accessible locally. You can navigate through the various homepages.

4. To try the admin-view, you can use the admin credentials in the file 'admin.txt'.

<br>

---

## Project Structure
An overview of the project's structure:

```
Reportoire/
│
├── app.py                 # Main application file
├── templates/             # HTML templates
│   ├── base.html          # Base template for shared layout
│   ├── index.html         # Homepage
│   ├── about.html         # About page
│   ├── projects.html      # Projects page
│   ├── contact.html       # Contact form
│   ├── admin_messages.html # Admin messages view
│   └── audio_player.html  # Audio player page (if needed)
├── static/                # Static files (CSS, JavaScript, images)
│   ├── css/
│   ├── js/
│   └── audio/             # Uploaded audio files
├── models.py              # Database models (e.g., messages)
├── forms.py               # WTForms for forms (e.g., contact form)
├── requirements.txt       # Python dependencies
└── README.md              # This file
```
<br>

---

## Technologies

* **Flask**: Python web framework for building the application.
* **HTML/CSS**: Frontend structure and styling.
* **JavaScript**: Interactivity and dynamic behaviour.
* **Jinja2**: Templating.
* **SQLite**: Databases.
* **OS**: Interaction with the operating system (files, directories, etc.).

<br>

---

## Asset Log
| **Type**          | **Name**                 | **Version** | **Source**   | **URL**                                                                                                           | **License**         |
| ----------------- | ------------------------ | ----------- | ------------ | ----------------------------------------------------------------------------------------------------------------- | ------------------- |
| **CSS Framework** | Bootstrap Grid           | 5.3.8       | Bootstrap    | [Grid on Bootstrap](https://getbootstrap.com/docs/4.0/layout/grid/)                                               | MIT License         |
| **CSS Framework** | W3.CSS Slideshow         | 5.0         | W3Schools    | [Slideshow on W3.CSS](https://www.w3schools.com/w3css/w3css_slideshow.asp)                                        | W3Schools License   |
| **Font**          | Birthstone               | N/A         | Google Fonts | [Birthstone on Google Fonts](https://fonts.google.com/specimen/Birthstone)                                        | Open Font License   |
| **Font**          | Nunito                   | N/A         | Google Fonts | [Nunito on Google Fonts](https://fonts.google.com/specimen/Nunito)                                                | Open Font License   |
| **Font**          | Playwrite England Joined | N/A         | Google Fonts | [Playwrite England Joined on Google Fonts](https://fonts.google.com/specimen/Playwrite+GB+J?query=playwrite+gb+j) | Open Font License   |
| **Font**          | Poetsen One              | N/A         | Google Fonts | [Poetsen One on Google Fonts](https://fonts.google.com/specimen/Poetsen+One)                                      | Open Font License   |
| **Icon**          | backward-fast            | 7.0.0       | Font Awesome | [backward-fast on Font Awesome](https://fontawesome.com/icons/backward-fast?f=classic&s=solid)                    | Free (Font Awesome) |
| **Icon**          | envelope                 | 7.2.0       | Font Awesome | [envelope on Font Awesome](https://fontawesome.com/icons/envelope?f=classic&s=solid)                              | Free (Font Awesome) |
| **Icon**          | forward-fast             | 7.0.0       | Font Awesome | [forward-fast on Font Awesome](https://fontawesome.com/icons/forward-fast?f=classic&s=solid)                      | Free (Font Awesome) |
| **Icon**          | download                 | 7.0.0       | Font Awesome | [download on Font Awesome](https://fontawesome.com/icons/download?f=classic&s=solid)                              | Free (Font Awesome) |
| **Icon**          | list-ul                  | 7.1.0       | Font Awesome | [list-ul on Font Awesome](https://fontawesome.com/icons/list-ul?f=classic&s=solid)                                | Free (Font Awesome) |
| **Icon**          | pause                    | 7.2.0       | Font Awesome | [pause on Font Awesome](https://fontawesome.com/icons/pause?f=classic&s=solid)                                    | Free (Font Awesome) |
| **Icon**          | phone                    | 7.2.0       | Font Awesome | [phone on Font Awesome](https://fontawesome.com/icons/phone?f=classic&s=solid)                                    | Free (Font Awesome) |
| **Icon**          | play                     | 7.2.0       | Font Awesome | [play on Font Awesome](https://fontawesome.com/icons/play?f=classic&s=solid)                                      | Free (Font Awesome) |
| **Icon**          | repeat                   | 7.0.0       | Font Awesome | [repeat on Font Awesome](https://fontawesome.com/icons/repeat?f=classic&s=solid)                                  | Free (Font Awesome) |
| **Icon**          | trash-can                | 7.0.0       | Font Awesome | [trash-can on Font Awesome](https://fontawesome.com/icons/trash-can?f=classic&s=solid)                            | Free (Font Awesome) |
| **Icon**          | upload                   | 7.0.0       | Font Awesome | [upload on Font Awesome](https://fontawesome.com/icons/upload?f=classic&s=solid)                                  | Free (Font Awesome) |

