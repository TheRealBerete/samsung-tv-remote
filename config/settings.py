"""
Configuration globale de l'application Samsung TV Remote.

Toutes les valeurs peuvent être surchargées par des variables d'environnement
ou un fichier .env à la racine du projet (voir .env.example).
"""
import os
import base64

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Charger .env si python-dotenv est installé (optionnel)
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(BASE_DIR, ".env"))
except ImportError:
    pass


def _env_bool(name, default=False):
    """Lit un booléen depuis l'environnement ("1", "true", "yes", "on")."""
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in ("1", "true", "yes", "on")


# ==================== Configuration TV ====================
TV_IP = os.getenv("TV_IP", "192.168.18.49")       # IP locale de la TV
# 8002 = wss + token (TV récentes), 8001 = ws simple (TV 2016-2017).
# Si le port choisi ne répond pas, l'autre est essayé automatiquement.
TV_PORT = int(os.getenv("TV_PORT", 8002))
TV_MAC = os.getenv("TV_MAC", "")                  # Adresse MAC pour allumer la TV (Wake-on-LAN)
TV_NAME = os.getenv("TV_NAME", "TheRealBerete Remote")
TV_NAME_B64 = base64.b64encode(TV_NAME.encode("utf-8")).decode("utf-8")
TV_TIMEOUT = float(os.getenv("TV_TIMEOUT", 5))     # secondes

# ==================== Configuration Flask ====================
FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))
FLASK_DEBUG = _env_bool("FLASK_DEBUG", False)

# ==================== Chemins ====================
TOKEN_FILE = os.getenv("TOKEN_FILE", os.path.join(BASE_DIR, "token.txt"))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

# ==================== Applications TV ====================
# IDs Tizen courants. Ils peuvent varier selon la région / l'année de la TV :
# GET /apps/installed renvoie la liste réelle quand la TV le permet.
APPS = {
    "NETFLIX": "11101200001",
    "YOUTUBE": "111299001912",
    "PRIME_VIDEO": "3201512006785",
    "DISNEY_PLUS": "3201901017640",
    "APPLE_TV": "3201807016597",
    "SPOTIFY": "3201606009684",
    "PLEX": "3201512006963",
    "BROWSER": "org.tizen.browser",
}

# ==================== Touches de télécommande ====================
KEYS = {
    "POWER": "KEY_POWER",
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
    "EXIT": "KEY_EXIT",
    "PLAY": "KEY_PLAY",
    "PAUSE": "KEY_PAUSE",
    "STOP": "KEY_STOP",
    "REWIND": "KEY_REWIND",
    "FF": "KEY_FF",
    "RED": "KEY_RED",
    "GREEN": "KEY_GREEN",
    "YELLOW": "KEY_YELLOW",
    "BLUE": "KEY_CYAN",
    **{f"NUM{i}": f"KEY_{i}" for i in range(10)},
}
