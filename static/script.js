(() => {
  const $ = (selector) => document.querySelector(selector);
  const player = $("[data-player]");
  const audio = $("[data-audio]");
  const title = $("[data-track-title]");
  const playlist = $("[data-playlist]");
  const details = $("[data-player-details]");
  const expand = $("[data-expand-player]");
  const hint = $("[data-player-hint]");
  const playButtons = [$("[data-play]"), $("[data-play-large]")].filter(Boolean);
  let tracks = [];
  let current = 0;
  let repeat = false;

  const year = $("[data-current-year]");
  if (year) year.textContent = new Date().getFullYear();

  // Theme selection is keyboard accessible and remembered between visits.
  const themeToggle = $(".theme-toggle");
  const themeMenu = $(".contrast-dropdown");
  const applyTheme = (theme) => {
    document.documentElement.dataset.theme = theme;
    try { localStorage.setItem("theme", theme); } catch (_) {}
  };
  let savedTheme = "light";
  try { savedTheme = localStorage.getItem("theme") || "light"; } catch (_) {}
  applyTheme(savedTheme);
  themeToggle?.addEventListener("click", () => {
    const open = themeToggle.getAttribute("aria-expanded") === "true";
    themeToggle.setAttribute("aria-expanded", String(!open));
    themeMenu.hidden = open;
  });
  themeMenu?.querySelectorAll("[data-theme-choice]").forEach((button) => {
    button.addEventListener("click", () => {
      applyTheme(button.dataset.themeChoice);
      themeMenu.hidden = true;
      themeToggle.setAttribute("aria-expanded", "false");
    });
  });
  document.addEventListener("click", (event) => {
    if (themeMenu && !event.target.closest(".theme-picker")) {
      themeMenu.hidden = true;
      themeToggle?.setAttribute("aria-expanded", "false");
    }
  });

  if (!player || !audio || !playlist) return;

  const setExpanded = (expanded) => {
    details.hidden = !expanded;
    expand.setAttribute("aria-expanded", String(expanded));
    player.classList.toggle("is-expanded", expanded);
  };
  expand?.addEventListener("click", () => setExpanded(details.hidden));

  // A one-time, dismissible hint — no modal or interruption.
  let hintDismissed = false;
  try { hintDismissed = localStorage.getItem("playerHintDismissed") === "yes"; } catch (_) {}
  if (!hintDismissed && hint) {
    hint.hidden = false;
    window.setTimeout(() => hint?.classList.add("is-visible"), 350);
  }
  $("[data-dismiss-hint]")?.addEventListener("click", () => {
    hint.hidden = true;
    try { localStorage.setItem("playerHintDismissed", "yes"); } catch (_) {}
  });
  expand?.addEventListener("click", () => {
    if (hint) hint.hidden = true;
    try { localStorage.setItem("playerHintDismissed", "yes"); } catch (_) {}
  }, { once: true });

  const setPlayIcon = (playing) => playButtons.forEach((button) => {
    button.innerHTML = playing
      ? '<i class="fa-solid fa-pause" aria-hidden="true"></i>'
      : '<i class="fa-solid fa-play" aria-hidden="true"></i>';
    button.setAttribute("aria-label", playing ? "Pause" : "Play");
  });
  const renderPlaylist = () => {
    playlist.replaceChildren();
    tracks.forEach((track, index) => {
      const item = document.createElement("li");
      const button = document.createElement("button");
      button.type = "button";
      button.textContent = track.title;
      button.setAttribute("aria-current", index === current ? "true" : "false");
      button.addEventListener("click", () => loadTrack(index, true));
      item.append(button);
      playlist.append(item);
    });
  };
  const loadTrack = (index, autoplay = false) => {
    if (!tracks.length) return;
    current = (index + tracks.length) % tracks.length;
    audio.src = tracks[current].src;
    title.textContent = tracks[current].title;
    renderPlaylist();
    if (autoplay) audio.play().then(() => setPlayIcon(true)).catch(() => setPlayIcon(false));
  };
  const play = () => {
    if (!tracks.length) return;
    if (audio.paused) audio.play().then(() => setPlayIcon(true)).catch(() => setPlayIcon(false));
    else { audio.pause(); setPlayIcon(false); }
  };
  playButtons.forEach((button) => button.addEventListener("click", play));
  $("[data-prev]")?.addEventListener("click", () => loadTrack(current - 1, true));
  $("[data-next]")?.addEventListener("click", () => loadTrack(current + 1, true));
  $("[data-loop]")?.addEventListener("click", (event) => {
    repeat = !repeat;
    event.currentTarget.setAttribute("aria-pressed", String(repeat));
    event.currentTarget.classList.toggle("is-active", repeat);
  });
  $("[data-toggle-list]")?.addEventListener("click", (event) => {
    const button = event.currentTarget;
    const open = playlist.hidden;
    playlist.hidden = !open;
    button.setAttribute("aria-expanded", String(open));
  });
  audio.addEventListener("play", () => setPlayIcon(true));
  audio.addEventListener("pause", () => setPlayIcon(false));
  audio.addEventListener("ended", () => {
    if (repeat) loadTrack(current, true);
    else if (current < tracks.length - 1) loadTrack(current + 1, true);
    else setPlayIcon(false);
  });
  audio.addEventListener("timeupdate", () => {
    const percent = Number.isFinite(audio.duration) && audio.duration > 0 ? audio.currentTime / audio.duration * 100 : 0;
    $("[data-progress]").style.width = percent + "%";
    const bar = $("[data-progress-container]");
    bar?.setAttribute("aria-valuenow", String(Math.round(percent)));
  });
  const seek = (event) => {
    if (!Number.isFinite(audio.duration) || audio.duration <= 0) return;
    const bounds = event.currentTarget.getBoundingClientRect();
    audio.currentTime = Math.max(0, Math.min(1, (event.clientX - bounds.left) / bounds.width)) * audio.duration;
  };
  $("[data-progress-container]")?.addEventListener("click", seek);
  $("[data-progress-container]")?.addEventListener("keydown", (event) => {
    if (!Number.isFinite(audio.duration)) return;
    if (event.key === "ArrowRight" || event.key === "ArrowLeft") {
      event.preventDefault();
      audio.currentTime = Math.max(0, Math.min(audio.duration, audio.currentTime + (event.key === "ArrowRight" ? 5 : -5)));
    }
  });

  fetch("/api/playlist")
    .then((response) => { if (!response.ok) throw new Error("Playlist unavailable"); return response.json(); })
    .then((data) => {
      tracks = Array.isArray(data) ? data : [];
      const hasTracks = tracks.length > 0;
      playButtons.forEach((button) => { button.disabled = !hasTracks; });
      $("[data-prev]")?.toggleAttribute("disabled", !hasTracks);
      $("[data-next]")?.toggleAttribute("disabled", !hasTracks);
      if (!hasTracks) {
        title.textContent = "A playlist is coming soon";
        renderPlaylist();
        return;
      }
      loadTrack(0);
    })
    .catch(() => { title.textContent = "Music is taking a little break"; });
})();