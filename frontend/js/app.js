/**
 * TV Remote — frontend
 * Envoie les touches au backend Flask et reflète l'état de la TV.
 */
(() => {
  const API = "";
  const led = document.getElementById("led");
  const statusEl = document.getElementById("status");
  const statusLabel = statusEl.querySelector(".label");
  const toastEl = document.getElementById("toast");

  let state = { tv_reachable: null, wol_enabled: false };
  let toastTimer, ledTimer;

  // ---------- Retours visuels ----------
  function flash(ok = true) {
    clearTimeout(ledTimer);
    led.classList.remove("flash", "err");
    void led.offsetWidth; // relance l'animation
    led.classList.add(ok ? "flash" : "err");
    ledTimer = setTimeout(() => led.classList.remove("flash", "err"), ok ? 90 : 600);
  }

  function haptic() {
    if (navigator.vibrate) navigator.vibrate(8);
  }

  function toast(msg) {
    toastEl.textContent = msg;
    toastEl.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toastEl.classList.remove("show"), 3200);
  }

  function setStatus(kind, text) {
    statusEl.className = "status is-" + kind;
    statusLabel.textContent = text;
  }

  // ---------- API ----------
  async function call(path) {
    try {
      const res = await fetch(API + path, { method: "POST" });
      const data = await res.json().catch(() => ({}));
      if (!res.ok || !data.success) throw new Error(data.error || `Erreur ${res.status}`);
      flash(true);
      return true;
    } catch (e) {
      flash(false);
      toast(e.message === "Failed to fetch" ? "Serveur injoignable. Le PC est-il allumé ?" : e.message);
      refreshStatus();
      return false;
    }
  }

  const sendKey = (key) => call(`/key/${key}`);
  const launchApp = (name) => call(`/app/${name}`);

  async function power() {
    // TV éteinte (pas de réponse réseau) → Wake-on-LAN, sinon KEY_POWER
    if (state.tv_reachable === false && state.wol_enabled) {
      flash(true);
      await call("/power/on");
      toast("Allumage en cours…");
      setTimeout(refreshStatus, 6000);
      return;
    }
    await sendKey("KEY_POWER");
    setTimeout(refreshStatus, 4000);
  }

  async function refreshStatus() {
    try {
      const res = await fetch(API + "/status");
      state = await res.json();
      if (state.tv_reachable) {
        const name = state.tv && (state.tv.model || state.tv.name);
        setStatus("ok", name ? `Connecté · ${name}` : "TV connectée");
      } else if (state.wol_enabled) {
        setStatus("warn", "TV en veille · appuie sur ⏻");
      } else {
        setStatus("off", `TV introuvable (${state.tv_ip})`);
      }
    } catch {
      setStatus("off", "Serveur hors ligne");
    }
  }

  // ---------- Appui / maintien ----------
  function bindPress(el, action, repeat) {
    let timer = null;
    let holding = false;
    const rocker = el.closest(".rocker");
    const tilt = rocker && (el === rocker.firstElementChild ? "tilt-up" : "tilt-down");

    const loop = async () => {
      if (!holding) return;
      await action();
      if (holding) timer = setTimeout(loop, 110);
    };

    const down = (e) => {
      e.preventDefault();
      el.setPointerCapture?.(e.pointerId);
      holding = true;
      el.classList.add("is-down");
      if (tilt) rocker.classList.add(tilt);
      haptic();
      action();
      if (repeat) timer = setTimeout(loop, 420);
    };
    const up = () => {
      holding = false;
      clearTimeout(timer);
      el.classList.remove("is-down");
      if (tilt) rocker.classList.remove(tilt);
    };

    el.addEventListener("pointerdown", down);
    el.addEventListener("pointerup", up);
    el.addEventListener("pointercancel", up);
    el.addEventListener("lostpointercapture", up);
    el.addEventListener("contextmenu", (e) => e.preventDefault());
  }

  document.querySelectorAll("[data-key]").forEach((el) => {
    const key = el.dataset.key;
    const action = key === "KEY_POWER" ? power : () => sendKey(key);
    bindPress(el, action, el.hasAttribute("data-repeat"));
  });

  document.querySelectorAll("[data-app]").forEach((el) => {
    bindPress(el, () => launchApp(el.dataset.app), false);
  });

  statusEl.addEventListener("click", refreshStatus);

  // ---------- Clavier (pratique sur ordinateur) ----------
  const KEYMAP = {
    ArrowUp: "KEY_UP", ArrowDown: "KEY_DOWN", ArrowLeft: "KEY_LEFT", ArrowRight: "KEY_RIGHT",
    Enter: "KEY_ENTER", Backspace: "KEY_RETURN", Escape: "KEY_EXIT", h: "KEY_HOME",
    "+": "KEY_VOLUP", "-": "KEY_VOLDOWN", m: "KEY_MUTE", " ": "KEY_PLAY",
  };
  document.addEventListener("keydown", (e) => {
    const key = KEYMAP[e.key];
    if (key) { e.preventDefault(); sendKey(key); }
  });

  // ---------- Démarrage ----------
  refreshStatus();
  setInterval(() => { if (!document.hidden) refreshStatus(); }, 15000);
  document.addEventListener("visibilitychange", () => { if (!document.hidden) refreshStatus(); });
})();
