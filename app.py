from flask import Flask, send_from_directory, jsonify
import websocket
import ssl
import json
import base64

app = Flask(__name__)

TV_IP = "192.168.18.49"
NAME_B64 = base64.b64encode(b"TheRealBerete").decode('utf-8')
TV_TOKEN = None

# Dictionnaire des applications avec leurs IDs officiels [citation:1][citation:5]
APPS = {
    "NETFLIX": "org.tizen.netflix-app",
    "YOUTUBE": "111299001912",        # parfois OK
    "YOUTUBE_ALT": "org.tizen.youtube-app",  # 👈 très important
    "PRIME_VIDEO": "org.tizen.ignition",
    "DISNEY_PLUS": "3201901019170",   # parfois KO selon région
    "APPLE_TV": "3201807016597",      # 👈 autre version plus récente
    "SPOTIFY": "3201606009684",
    "BROWSER": "org.tizen.browser",
    "PLEX": "3201512006963"
}

# Toutes les commandes de navigation qui fonctionnent [citation:4]
KEYS = {
    "UP": "KEY_UP",
    "DOWN": "KEY_DOWN",
    "LEFT": "KEY_LEFT",
    "RIGHT": "KEY_RIGHT",
    "ENTER": "KEY_ENTER",
    "RETURN": "KEY_RETURN",
    "HOME": "KEY_HOME",
    "VOLUP": "KEY_VOLUP",
    "VOLDOWN": "KEY_VOLDOWN",
    "MUTE": "KEY_MUTE",
    "CHUP": "KEY_CHUP",
    "CHDOWN": "KEY_CHDOWN",
    "GUIDE": "KEY_GUIDE",
    "SOURCE": "KEY_SOURCE",
    "INFO": "KEY_INFO",
    "MENU": "KEY_MENU",
    "EXIT": "KEY_EXIT"
}

def get_ws_url():
    url = f"wss://{TV_IP}:8002/api/v2/channels/samsung.remote.control?name={NAME_B64}"
    if TV_TOKEN:
        url += f"&token={TV_TOKEN}"
    return url

def send_command(method, params):
    """Fonction générique pour envoyer des commandes à la TV"""
    global TV_TOKEN
    try:
        ws_url = get_ws_url()
        ws = websocket.create_connection(
            ws_url,
            sslopt={"cert_reqs": ssl.CERT_NONE, "check_hostname": False}
        )
        
        payload = {
            "method": method,
            "params": params
        }
        
        ws.send(json.dumps(payload))
        response = json.loads(ws.recv())
        
        if not TV_TOKEN and "data" in response and "token" in response["data"]:
            TV_TOKEN = response["data"]["token"]
            print(f"✅ Token sauvegardé : {TV_TOKEN}")
            with open("token.txt", "w") as f:
                f.write(TV_TOKEN)
        
        ws.close()
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def send_key(key):
    """Envoie une touche de télécommande"""
    return send_command("ms.remote.control", {
        "Cmd": "Click",
        "DataOfCmd": key,
        "Option": "false",
        "TypeOfRemote": "SendRemoteKey"
    })

def launch_app(app_id):
    """Lance une application sur la TV [citation:10]"""
    return send_command("ms.channel.emit", {
        "event": "ed.apps.launch",
        "to": "host",
        "data": {
            "appId": app_id,
            "action_type": "NATIVE_LAUNCH"
        }
    })

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/key/<cmd>')
def key(cmd):
    if cmd in KEYS.values():
        success = send_key(cmd)
    else:
        success = False
    return jsonify({"success": success, "cmd": cmd})

@app.route('/app/<app_name>')
def launch_app_route(app_name):
    app_id = APPS.get(app_name.upper())
    if app_id:
        success = launch_app(app_id)
        return jsonify({"success": success, "app": app_name, "app_id": app_id})
    return jsonify({"success": False, "error": "App non trouvée"})

# Charger un token existant au démarrage
try:
    with open("token.txt", "r") as f:
        TV_TOKEN = f.read().strip()
        print(f"📁 Token chargé : {TV_TOKEN}")
except:
    print("📁 Pas de token sauvegardé")

if __name__ == '__main__':
    print(f"🎮 Remote TV - {TV_IP}:8002")
    print(f"📱 http://192.168.18.12:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)