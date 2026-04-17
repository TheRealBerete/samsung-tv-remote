"""
Samsung TV Remote Control - Backend Flask Application
Application web pour contrôler une TV Samsung via l'API WebSocket

Author: TheRealBerete
License: MIT
"""

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
import websocket
import ssl
import json
import os
import sys

# Ajouter le chemin du projet au sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from config.settings import (
    TV_IP, TV_PORT, TV_NAME_B64, FLASK_HOST, FLASK_PORT, FLASK_DEBUG,
    TOKEN_FILE, FRONTEND_DIR, APPS, KEYS, SSL_VERIFY
)

# Initialiser l'app Flask
app = Flask(__name__)
CORS(app)  # Activer CORS pour les requêtes cross-origin

# Variable globale pour le token
TV_TOKEN = None

# ==================== Fonctions principales ====================

def load_token():
    """Charger le token sauvegardé"""
    global TV_TOKEN
    try:
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, "r") as f:
                TV_TOKEN = f.read().strip()
                print(f"📁 Token chargé : {TV_TOKEN[:20]}...")
                return True
    except Exception as e:
        print(f"⚠️  Impossible de charger le token: {e}")
    return False

def save_token(token):
    """Sauvegarder le token"""
    global TV_TOKEN
    TV_TOKEN = token
    try:
        with open(TOKEN_FILE, "w") as f:
            f.write(token)
        print(f"✅ Token sauvegardé : {token[:20]}...")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde du token: {e}")
        return False

def get_ws_url():
    """Construire l'URL WebSocket pour la TV"""
    url = f"wss://{TV_IP}:{TV_PORT}/api/v2/channels/samsung.remote.control?name={TV_NAME_B64}"
    if TV_TOKEN:
        url += f"&token={TV_TOKEN}"
    return url

def send_command(method, params):
    """
    Fonction générique pour envoyer des commandes à la TV
    
    Args:
        method (str): Méthode de l'API Samsung
        params (dict): Paramètres de la commande
    
    Returns:
        bool: True si succès, False sinon
    """
    global TV_TOKEN
    try:
        ws_url = get_ws_url()
        
        # Créer la connexion WebSocket
        ws = websocket.create_connection(
            ws_url,
            sslopt={"cert_reqs": ssl.CERT_NONE, "check_hostname": False}
        )
        
        # Préparer et envoyer le payload
        payload = {
            "method": method,
            "params": params
        }
        
        ws.send(json.dumps(payload))
        response = json.loads(ws.recv())
        
        # Sauvegarder le token s'il est fourni
        if not TV_TOKEN and "data" in response and "token" in response["data"]:
            save_token(response["data"]["token"])
        
        ws.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def send_key(key):
    """Envoyer une touche de télécommande"""
    return send_command("ms.remote.control", {
        "Cmd": "Click",
        "DataOfCmd": key,
        "Option": "false",
        "TypeOfRemote": "SendRemoteKey"
    })

def launch_app(app_id):
    """Lancer une application sur la TV"""
    return send_command("ms.channel.emit", {
        "event": "ed.apps.launch",
        "to": "host",
        "data": {
            "appId": app_id,
            "action_type": "NATIVE_LAUNCH"
        }
    })

# ==================== Routes Flask ====================

@app.route('/')
def index():
    """Servir l'interface HTML principale"""
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/key/<cmd>')
def key_route(cmd):
    """
    Endpoint pour envoyer une touche de télécommande
    
    Args:
        cmd (str): Code de la touche (ex: KEY_UP, KEY_DOWN, etc.)
    
    Returns:
        JSON: {"success": bool, "cmd": str}
    """
    if cmd in KEYS.values():
        success = send_key(cmd)
    else:
        success = False
    return jsonify({"success": success, "cmd": cmd})

@app.route('/app/<app_name>')
def app_route(app_name):
    """
    Endpoint pour lancer une application
    
    Args:
        app_name (str): Nom de l'application (ex: NETFLIX, YOUTUBE, etc.)
    
    Returns:
        JSON: {"success": bool, "app": str, "app_id": str}
    """
    app_id = APPS.get(app_name.upper())
    if app_id:
        success = launch_app(app_id)
        return jsonify({"success": success, "app": app_name, "app_id": app_id})
    return jsonify({"success": False, "error": "App non trouvée"}), 404

@app.route('/apps')
def list_apps():
    """Lister toutes les applications disponibles"""
    apps_list = [{"name": name, "app_id": app_id} for name, app_id in APPS.items()]
    return jsonify({"apps": apps_list})

@app.route('/keys')
def list_keys():
    """Lister toutes les touches disponibles"""
    keys_list = [{"name": name, "code": code} for name, code in KEYS.items()]
    return jsonify({"keys": keys_list})

@app.route('/status')
def status():
    """État de l'application"""
    return jsonify({
        "status": "online",
        "tv_ip": TV_IP,
        "tv_port": TV_PORT,
        "token_saved": TV_TOKEN is not None
    })

@app.errorhandler(404)
def not_found(error):
    """Gestionnaire d'erreur 404"""
    return jsonify({"error": "Not Found", "message": "L'endpoint n'existe pas"}), 404

@app.errorhandler(500)
def server_error(error):
    """Gestionnaire d'erreur 500"""
    return jsonify({"error": "Server Error", "message": "Une erreur serveur s'est produite"}), 500

# ==================== Démarrage ====================

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🎮 Samsung TV Remote Control")
    print("="*50)
    
    # Charger le token existant
    load_token()
    
    # Afficher les informations de démarrage
    print(f"\n📡 Configuration:")
    print(f"   TV IP : {TV_IP}:{TV_PORT}")
    print(f"   Accès : http://{FLASK_HOST}:{FLASK_PORT}")
    print(f"   Debug : {FLASK_DEBUG}")
    
    print(f"\n✅ Serveur en cours de démarrage...")
    print(f"   Ouvrez http://localhost:{FLASK_PORT} dans votre navigateur")
    print(f"   Appuyez sur Ctrl+C pour arrêter")
    print("\n" + "="*50 + "\n")
    
    # Démarrer l'application Flask
    app.run(
        host=FLASK_HOST,
        port=FLASK_PORT,
        debug=FLASK_DEBUG,
        use_reloader=FLASK_DEBUG
    )
