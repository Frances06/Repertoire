function getCurrentYear() {
    document.getElementById("current-year").innerHTML = new Date().getFullYear();
}
window.onload = getCurrentYear;

// Playlist array
/*const tracks = [
    { title: "Track 1", src: "audio/track1.mp3" },
    { title: "Track 2", src: "audio/track2.mp3" },
    { title: "Track 3", src: "audio/track3.mp3" }
];

let currentTrack = 0;
const audio = document.getElementById("audio");
const trackTitle = document.getElementById("track-title");
const playlistEl = document.getElementById("playlist");
const playBtn = document.getElementById("play");
const prevBtn = document.getElementById("prev");
const nextBtn = document.getElementById("next");

// Load playlist into UI
tracks.forEach((track, index) => {
    const li = document.createElement("li");
    li.textContent = track.title;
    li.addEventListener("click", () => loadTrack(index, true));
    playlistEl.appendChild(li);
});

// Load a track
function loadTrack(index, playNow = false) {
    currentTrack = index;
    audio.src = tracks[index].src;
    trackTitle.textContent = tracks[index].title;
    updateActiveTrack();
    if (playNow) audio.play();
}

// Update active track highlight
function updateActiveTrack() {
    [...playlistEl.children].forEach((li, i) => {
        li.classList.toggle("active", i === currentTrack);
    });
}

// Play/Pause toggle
playBtn.addEventListener("click", () => {
    if (audio.paused) {
        audio.play();
        playBtn.textContent = "⏸ Pause";
    } else {
        audio.pause();
        playBtn.textContent = "▶ Play";
    }
});

// Previous track
prevBtn.addEventListener("click", () => {
    currentTrack = (currentTrack - 1 + tracks.length) % tracks.length;
    loadTrack(currentTrack, true);
});

// Next track
nextBtn.addEventListener("click", () => {
    currentTrack = (currentTrack + 1) % tracks.length;
    loadTrack(currentTrack, true);
});

// Auto play next track when current ends
audio.addEventListener("ended", () => {
    nextBtn.click();
});

// Initial load
loadTrack(0);*/

    let tracks = [];
    let currentTrack = 0;

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

    // Build playlist UI
    /*function buildPlaylist() {
        playlistEl.innerHTML = "";

        tracks.forEach((track, index) => {
            const li = document.createElement("li");
            li.textContent = track.title;
            li.addEventListener("click", () => loadTrack(index, true));
            playlistEl.appendChild(li);
        });
    }*/

    function buildPlaylist() {
    playlistEl.innerHTML = "";

    tracks.forEach((track, index) => {
        const li = document.createElement("li");

        li.textContent = track.title;

        const del = document.createElement("button");
        del.textContent = "Delete";
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

    // Auto-play next track when current ends
    audio.addEventListener("ended", () => {
        nextBtn.click();
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
