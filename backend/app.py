"""
Samsung TV Remote Control - Backend Flask
Contrôle une TV Samsung (Tizen) via son API WebSocket locale.

Author: TheRealBerete
License: MIT
"""

import json
import os
import socket
import ssl
import sys
import threading
import time
import urllib.request

import websocket
from flask import Flask, jsonify, request, send_from_directory

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from config.settings import (  # noqa: E402
    APPS, FLASK_DEBUG, FLASK_HOST, FLASK_PORT, FRONTEND_DIR, KEYS,
    TOKEN_FILE, TV_IP, TV_MAC, TV_NAME_B64, TV_PORT, TV_TIMEOUT,
)

app = Flask(__name__, static_folder=None)
VALID_KEYS = set(KEYS.values())


# ==================== Connexion à la TV ====================

class TVConnection:
    """
    Connexion WebSocket persistante vers la TV.

    - Attend l'événement `ms.channel.connect` avant d'envoyer quoi que ce soit
      (sinon la TV ignore les commandes).
    - Réutilise la même connexion entre les appuis (plus rapide, et la TV ne
      redemande pas l'autorisation à chaque touche).
    - Essaie le port configuré puis l'autre (8002 wss ↔ 8001 ws).
    - Sauvegarde / renouvelle le token renvoyé par la TV.
    """

    def __init__(self, ip, port, name_b64, token_file, timeout):
        self.ip = ip
        self.ports = [port] + [p for p in (8002, 8001) if p != port]
        self.name_b64 = name_b64
        self.token_file = token_file
        self.timeout = timeout
        self.ws = None
        self.port = None
        self.lock = threading.Lock()
        self.last_error = None
        self.token = self._load_token()

    # ---------- Token ----------
    def _load_token(self):
        try:
            with open(self.token_file) as f:
                token = f.read().strip()
                if token:
                    print(f"📁 Token chargé : {token[:8]}…")
                return token or None
        except FileNotFoundError:
            return None
        except OSError as e:
            print(f"⚠️  Lecture du token impossible : {e}")
            return None

    def _save_token(self, token):
        if not token or token == self.token:
            return
        self.token = token
        try:
            with open(self.token_file, "w") as f:
                f.write(token)
            print(f"✅ Token sauvegardé : {token[:8]}…")
        except OSError as e:
            print(f"⚠️  Sauvegarde du token impossible : {e}")

    def _clear_token(self):
        self.token = None
        try:
            os.remove(self.token_file)
        except OSError:
            pass

    # ---------- Connexion ----------
    def _url(self, port):
        scheme = "wss" if port == 8002 else "ws"
        url = f"{scheme}://{self.ip}:{port}/api/v2/channels/samsung.remote.control?name={self.name_b64}"
        if self.token and port == 8002:
            url += f"&token={self.token}"
        return url

    def _open(self, port, handshake_timeout):
        ws = websocket.create_connection(
            self._url(port),
            timeout=self.timeout,
            sslopt={"cert_reqs": ssl.CERT_NONE, "check_hostname": False},
        )
        # La 1re fois, la TV affiche « Autoriser ? » : on laisse le temps de répondre.
        ws.settimeout(handshake_timeout)
        try:
            while True:
                msg = json.loads(ws.recv())
                event = msg.get("event")
                if event == "ms.channel.connect":
                    self._save_token((msg.get("data") or {}).get("token"))
                    ws.settimeout(self.timeout)
                    return ws
                if event == "ms.channel.unauthorized":
                    if self.token:
                        self._clear_token()  # token périmé → on en redemandera un
                    raise PermissionError("Connexion refusée sur la TV (choisis « Autoriser »)")
        except Exception:
            ws.close()
            raise

    def _ensure(self):
        if self.ws and self.ws.connected:
            return
        self.ws = None
        errors = []
        handshake = 5 if self.token else 30
        for port in ([self.port] if self.port else self.ports):
            try:
                self.ws = self._open(port, handshake)
                if self.port != port:
                    print(f"🔌 Connecté à la TV sur le port {port}")
                self.port = port
                self.last_error = None
                return
            except PermissionError:
                raise
            except Exception as e:
                errors.append(f"{port}: {e}")
        self.port = None
        raise ConnectionError("TV injoignable (" + " | ".join(errors) + ")")

    def send(self, method, params):
        payload = json.dumps({"method": method, "params": params})
        with self.lock:
            for attempt in range(2):  # 2e essai si la connexion gardée était morte
                try:
                    self._ensure()
                    self.ws.send(payload)
                    return True, None
                except PermissionError as e:
                    self.last_error = str(e)
                    return False, self.last_error
                except Exception as e:
                    self.close()
                    self.last_error = str(e)
                    if attempt == 1:
                        return False, self.last_error
            return False, self.last_error

    def close(self):
        if self.ws:
            try:
                self.ws.close()
            except Exception:
                pass
        self.ws = None

    @property
    def connected(self):
        return bool(self.ws and self.ws.connected)


tv = TVConnection(TV_IP, TV_PORT, TV_NAME_B64, TOKEN_FILE, TV_TIMEOUT)


# ==================== Actions ====================

def send_key(key):
    return tv.send("ms.remote.control", {
        "Cmd": "Click",
        "DataOfCmd": key,
        "Option": "false",
        "TypeOfRemote": "SendRemoteKey",
    })


def launch_app(app_id):
    # 1) API REST (fonctionne sur la plupart des TV 2016+)
    try:
        req = urllib.request.Request(
            f"http://{TV_IP}:8001/api/v2/applications/{app_id}", method="POST", data=b""
        )
        with urllib.request.urlopen(req, timeout=TV_TIMEOUT) as res:
            if res.status < 300:
                return True, None
    except Exception:
        pass
    # 2) Repli WebSocket
    return tv.send("ms.channel.emit", {
        "event": "ed.apps.launch",
        "to": "host",
        "data": {
            "appId": app_id,
            "action_type": "NATIVE_LAUNCH" if "." in app_id else "DEEP_LINK",
        },
    })


def wake_on_lan(mac):
    """Envoie un « magic packet » pour allumer la TV."""
    mac_hex = mac.replace(":", "").replace("-", "").strip()
    if len(mac_hex) != 12:
        raise ValueError("TV_MAC invalide (format attendu 7C:64:56:4A:8B:AA)")
    packet = b"\xff" * 6 + bytes.fromhex(mac_hex) * 16
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        for port in (9, 7):
            s.sendto(packet, ("255.255.255.255", port))


def tv_info():
    """Infos de la TV via l'API REST (sert aussi de test « allumée ? »)."""
    try:
        with urllib.request.urlopen(f"http://{TV_IP}:8001/api/v2/", timeout=2) as res:
            data = json.loads(res.read().decode("utf-8"))
            device = data.get("device", {})
            return {"name": data.get("name") or device.get("name"), "model": device.get("modelName")}
    except Exception:
        return None


# ==================== Routes ====================

def result(ok, error=None, **extra):
    body = {"success": ok, **extra}
    if error:
        body["error"] = error
    return jsonify(body), (200 if ok else 503)


@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(FRONTEND_DIR, filename)


@app.route("/key/<cmd>", methods=["GET", "POST"])
def key_route(cmd):
    if cmd not in VALID_KEYS:
        return jsonify({"success": False, "error": "Touche inconnue", "cmd": cmd}), 400
    ok, err = send_key(cmd)
    return result(ok, err, cmd=cmd)


@app.route("/app/<app_name>", methods=["GET", "POST"])
def app_route(app_name):
    app_id = APPS.get(app_name.upper())
    if not app_id:
        return jsonify({"success": False, "error": "App non trouvée"}), 404
    ok, err = launch_app(app_id)
    return result(ok, err, app=app_name, app_id=app_id)


@app.route("/power/on", methods=["POST"])
def power_on():
    if not TV_MAC:
        return jsonify({"success": False, "error": "TV_MAC non configurée"}), 400
    try:
        wake_on_lan(TV_MAC)
    except Exception as e:
        return result(False, str(e))
    return result(True)


@app.route("/apps")
def list_apps():
    return jsonify({"apps": [{"name": n, "app_id": i} for n, i in APPS.items()]})


@app.route("/keys")
def list_keys():
    return jsonify({"keys": [{"name": n, "code": c} for n, c in KEYS.items()]})


@app.route("/status")
def status():
    info = tv_info()
    return jsonify({
        "status": "online",
        "tv_ip": TV_IP,
        "tv_port": tv.port or TV_PORT,
        "tv_reachable": info is not None,
        "tv": info,
        "connected": tv.connected,
        "token_saved": tv.token is not None,
        "wol_enabled": bool(TV_MAC),
        "last_error": tv.last_error,
    })


@app.route("/health")
def health():
    return jsonify({"ok": True})


@app.errorhandler(404)
def not_found(_):
    return jsonify({"error": "Not Found", "path": request.path}), 404


# ==================== Démarrage ====================

def local_ips():
    ips = set()
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect((TV_IP, 9))
            ips.add(s.getsockname()[0])
    except OSError:
        pass
    return sorted(ips) or ["localhost"]


def main():
    print("\n" + "=" * 50)
    print("🎮 Samsung TV Remote Control")
    print("=" * 50)
    print(f"📡 TV      : {TV_IP} (port {TV_PORT}, repli auto)")
    print(f"⚡ Allumage : {'Wake-on-LAN ' + TV_MAC if TV_MAC else 'désactivé (TV_MAC vide)'}")
    for ip in local_ips():
        print(f"📱 Ouvre sur ton téléphone : http://{ip}:{FLASK_PORT}")
    print("=" * 50 + "\n")
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG,
            use_reloader=FLASK_DEBUG, threaded=True)


if __name__ == "__main__":
    main()
