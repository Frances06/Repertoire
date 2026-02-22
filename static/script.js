function getCurrentYear() {
    document.getElementById("current-year").innerHTML = new Date().getFullYear();
}
window.onload = getCurrentYear;

    let tracks = [];
    let currentTrack = 0;
    let loopSong = false;

    const audio = document.getElementById("audio");
    const trackTitle = document.getElementById("track-title");
    const playlistEl = document.getElementById("playlist");
    const playBtn = document.getElementById("play");
    const prevBtn = document.getElementById("prev");
    const nextBtn = document.getElementById("next");

    // Fetch playlist from Flask
    fetch("/api/playlist")
        .then(res => res.json())
        .then(data => {
            tracks = data;

            if (tracks.length === 0) {
                trackTitle.textContent = "No tracks available";
                return;
            }

            buildPlaylist();
            loadTrack(0);
        })
        .catch(err => {
            console.error("Failed to load playlist:", err);
            trackTitle.textContent = "Error loading playlist";
        });

    function buildPlaylist() {
    playlistEl.innerHTML = "";

    tracks.forEach((track, index) => {
        const li = document.createElement("li");

        const titleSpan = document.createElement("span");
        titleSpan.textContent = track.title;
        titleSpan.style.width = "95%";
        titleSpan.style.display = "inline-block";
        li.appendChild(titleSpan);

        const del = document.createElement("button");
        del.innerHTML = '<i class="fa-solid fa-trash-can"></i>';
        del.addEventListener("click", (e) => {
            e.stopPropagation();
            deleteTrack(track);
        });

        li.appendChild(del);
        li.addEventListener("click", () => loadTrack(index, true));
        playlistEl.appendChild(li);
    });
}

function deleteTrack(track) {
    fetch("/delete", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ filename: track.filename })
    })
    .then(res => res.json())
    .then(() => {
        // Reload playlist from server
        refreshPlaylist();
    })
    .catch(err => console.error("Delete failed:", err));
}

function refreshPlaylist() {
    fetch("/api/playlist")
        .then(res => res.json())
        .then(data => {
            tracks = data;
            buildPlaylist();

            if (tracks.length === 0) {
                trackTitle.textContent = "No tracks available";
                audio.src = "";
                return;
            }

            // Ensure currentTrack is valid after delete
            currentTrack = Math.min(currentTrack, tracks.length - 1);
            loadTrack(currentTrack);
        });
}

    // Load a track
    function loadTrack(index, playNow = false) {
        currentTrack = index;
        audio.src = tracks[index].src;
        trackTitle.textContent = tracks[index].title;
        updateActiveTrack();

        if (playNow) {
            audio.play();
            playBtn.innerHTML = '<i class="fa-solid fa-pause"></i>';
        }
    }

    // Update active track highlight
    function updateActiveTrack() {
        [...playlistEl.children].forEach((li, i) => {
            li.classList.toggle("active", i === currentTrack);
        });
    }

    // Play / Pause toggle
    playBtn.addEventListener("click", () => {
        if (!tracks.length) return;

        if (audio.paused) {
            audio.play();
            playBtn.innerHTML = '<i class="fa-solid fa-pause"></i>';
        } else {
            audio.pause();
            playBtn.innerHTML = '<i class="fa-solid fa-play"></i>';
        }
    });

    // Previous track
    prevBtn.addEventListener("click", () => {
        if (!tracks.length) return;

        currentTrack = (currentTrack - 1 + tracks.length) % tracks.length;
        loadTrack(currentTrack, true);
    });

    // Next track
    nextBtn.addEventListener("click", () => {
        if (!tracks.length) return;

        currentTrack = (currentTrack + 1) % tracks.length;
        loadTrack(currentTrack, true);
    });

    // Play next track or loop when current ends
    audio.addEventListener("ended", () => {
        if (loopSong) {
            audio.currentTime = 0;
            audio.play();
        } else {
            nextBtn.click();
        }
    });

    // Loop button functionality
    const loopBtn = document.getElementById("loop");

    loopBtn.addEventListener("click", () => {
        loopSong = !loopSong;
        loopBtn.classList.toggle("active", loopSong);
    });


const uploadInput = document.getElementById("upload");

uploadInput.addEventListener("change", () => {
    const file = uploadInput.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    fetch("/upload", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(() => {
        return fetch("/api/playlist");
    })
    .then(res => res.json())
    .then(data => {
        tracks = data;
        buildPlaylist();
        loadTrack(tracks.length - 1, true); // auto-play new track
    })
    .catch(err => console.error("Upload failed:", err));
});

const progressContainer = document.getElementById("progress-container");
const progress = document.getElementById("progress");

audio.addEventListener("timeupdate", () => {
    const percent = (audio.currentTime / audio.duration) * 100;
    progress.style.width = percent + "%";
});

progressContainer.addEventListener("click", (e) => {
    const width = progressContainer.clientWidth;
    const clickX = e.offsetX;
    const duration = audio.duration;

    audio.currentTime = (clickX / width) * duration;
});

progressContainer.addEventListener("keydown", (e) => {
    if (!tracks.length) return;

    const stepSize = 5; // seconds
    const duration = audio.duration;

    switch(e.key) {
        case "ArrowRight":
            e.preventDefault();
            audio.currentTime = Math.min(audio.currentTime + stepSize, duration);
            break;
        case "ArrowLeft":
            e.preventDefault();
            audio.currentTime = Math.max(audio.currentTime - stepSize, 0);
            break;
        case " ":
            e.preventDefault();
            playBtn.click();
            break;
    }
});

progressContainer.setAttribute("tabindex", "0");
progressContainer.setAttribute("role", "slider");
progressContainer.setAttribute("aria-label", "Audio progress");

  function toggleList() {
    const el = document.getElementById("playlist");
    el.style.display = el.style.display === "none" ? "block" : "none";
  }

function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
}

document.addEventListener("DOMContentLoaded", () => {
    const savedTheme = localStorage.getItem("theme") || "light";
    document.documentElement.setAttribute("data-theme", savedTheme);
});

const form = document.getElementById("contact-form");

form.addEventListener("submit", function (e) {
  e.preventDefault();

  fetch(form.dataset.url, {
    method: "POST",
    body: new FormData(form)
  })
  .then(res => res.json())
  .then(data => {
    alert(data.status);
  });
});

const textarea = document.getElementById("message");
const counter = document.getElementById("char-count");

counter.textContent = textarea.value.length;

textarea.addEventListener("input", () => {
  counter.textContent = textarea.value.length;
});