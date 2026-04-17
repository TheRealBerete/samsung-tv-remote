"""
Configuration globale de l'application Samsung TV Remote
"""
import os
import base64

# ==================== Configuration TV ====================
TV_IP = os.getenv("TV_IP", "192.168.18.49")  # À modifier avec votre IP locale
TV_PORT = 8002
TV_NAME = "TheRealBerete"
TV_NAME_B64 = base64.b64encode(TV_NAME.encode('utf-8')).decode('utf-8')

# ==================== Configuration Flask ====================
FLASK_HOST = "0.0.0.0"
FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))
FLASK_DEBUG = os.getenv("FLASK_DEBUG", True)

# ==================== Chemins ====================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN_FILE = os.path.join(BASE_DIR, "token.txt")
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

# ==================== Applications TV ====================
APPS = {
    "NETFLIX": "org.tizen.netflix-app",
    "YOUTUBE": "org.tizen.youtube-app",
    "YOUTUBE_ALT": "111299001912",
    "PRIME_VIDEO": "org.tizen.ignition",
    "DISNEY_PLUS": "3201901019170",
    "APPLE_TV": "3201807016597",
    "SPOTIFY": "3201606009684",
    "BROWSER": "org.tizen.browser",
    "PLEX": "3201512006963"
}

# ==================== Touches de télécommande ====================
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

# ==================== Configuration SSL ====================
SSL_VERIFY = False  # Accepte les certificats auto-signés (TV Samsung)
