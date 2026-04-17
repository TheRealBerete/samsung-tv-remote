# 📡 Documentation API - Samsung TV Remote

Référence complète des endpoints API disponibles.

## 🔗 Base URL

```
http://localhost:5000
```

## 🎮 Endpoints Navigation

### Envoyer une touche de navigation

**Endpoint**
```
GET /key/<KEY_CODE>
```

**Paramètres**
- `KEY_CODE` : Code de la touche (voir tableau ci-dessous)

**Exemple**
```bash
curl http://localhost:5000/key/KEY_UP
```

**Réponse**
```json
{
  "success": true,
  "cmd": "KEY_UP"
}
```

**Touches disponibles**
| Code | Fonction |
|------|----------|
| `KEY_UP` | Naviguer vers le haut |
| `KEY_DOWN` | Naviguer vers le bas |
| `KEY_LEFT` | Naviguer vers la gauche |
| `KEY_RIGHT` | Naviguer vers la droite |
| `KEY_ENTER` | Valider / Sélectionner |
| `KEY_RETURN` | Retour arrière |
| `KEY_HOME` | Accueil |
| `KEY_VOLUP` | Augmenter le volume |
| `KEY_VOLDOWN` | Diminuer le volume |
| `KEY_MUTE` | Couper le son |
| `KEY_CHUP` | Chaîne suivante |
| `KEY_CHDOWN` | Chaîne précédente |
| `KEY_MENU` | Afficher le menu |
| `KEY_EXIT` | Quitter |
| `KEY_GUIDE` | Guide EPG |
| `KEY_SOURCE` | Sélecteur de source |
| `KEY_INFO` | Information |

---

## 📱 Endpoints Applications

### Lancer une application

**Endpoint**
```
GET /app/<APP_NAME>
```

**Paramètres**
- `APP_NAME` : Nom de l'application (insensible à la casse)

**Exemple**
```bash
curl http://localhost:5000/app/NETFLIX
```

**Réponse**
```json
{
  "success": true,
  "app": "NETFLIX",
  "app_id": "org.tizen.netflix-app"
}
```

**Applications disponibles**
| Nom | App ID |
|-----|--------|
| `NETFLIX` | org.tizen.netflix-app |
| `YOUTUBE` | org.tizen.youtube-app |
| `YOUTUBE_ALT` | 111299001912 |
| `PRIME_VIDEO` | org.tizen.ignition |
| `DISNEY_PLUS` | 3201901019170 |
| `APPLE_TV` | 3201807016597 |
| `SPOTIFY` | 3201606009684 |
| `BROWSER` | org.tizen.browser |
| `PLEX` | 3201512006963 |

---

## 💾 Gestion des Applications

### Lister toutes les applications disponibles

**Endpoint**
```
GET /apps
```

**Réponse**
```json
{
  "apps": [
    {
      "name": "NETFLIX",
      "app_id": "org.tizen.netflix-app"
    },
    {
      "name": "YOUTUBE",
      "app_id": "org.tizen.youtube-app"
    }
  ]
}
```

---

## ⚙️ Commandes Système

### État de la TV

**Endpoint** (À implémenter)
```
GET /status
```

**Réponse prévue**
```json
{
  "connected": true,
  "tv_ip": "192.168.18.49",
  "token_saved": true
}
```

### Redémarrer l'application

**Endpoint** (À implémenter)
```
POST /restart
```

---

## 📊 Codes de Réponse HTTP

| Code | Signification |
|------|---------------|
| `200` | Succès - Commande exécutée |
| `400` | Erreur - Paramètre invalide |
| `404` | Non trouvé - App/clé inexistante |
| `500` | Erreur serveur - Problème de connexion |

---

## 🔐 Authentification

L'API n'utilise **pas d'authentification directe**, mais la TV elle-même utilise un système de token :

1. La première connexion génère un token automatiquement
2. Le token est sauvegardé dans `token.txt`
3. Les reconnexions utilisent ce token automatiquement
4. Si le token expire, un nouveau est généré

**Aucune clé API requise** pour cette version.

---

## 📝 Exemples complets

### Exemple 1 : Lancer Netflix et naviguer

```bash
# Lancer Netflix
curl http://localhost:5000/app/NETFLIX

# Attendre quelques secondes
sleep 3

# Naviguer vers le haut
curl http://localhost:5000/key/KEY_UP

# Valider la sélection
curl http://localhost:5000/key/KEY_ENTER
```

### Exemple 2 : Augmenter le volume

```bash
# Augmenter le volume 3 fois
for i in {1..3}; do
  curl http://localhost:5000/key/KEY_VOLUP
  sleep 0.5
done
```

### Exemple 3 : Aller à l'accueil

```bash
curl http://localhost:5000/key/KEY_HOME
```

---

## 🔧 Client Python exemple

```python
import requests

BASE_URL = "http://localhost:5000"

def send_key(key):
    response = requests.get(f"{BASE_URL}/key/{key}")
    return response.json()

def launch_app(app_name):
    response = requests.get(f"{BASE_URL}/app/{app_name}")
    return response.json()

# Utilisation
send_key("KEY_UP")
launch_app("NETFLIX")
```

---

## 🔧 Client JavaScript exemple

```javascript
const BASE_URL = "http://localhost:5000";

async function sendKey(key) {
  const response = await fetch(`${BASE_URL}/key/${key}`);
  return await response.json();
}

async function launchApp(appName) {
  const response = await fetch(`${BASE_URL}/app/${appName}`);
  return await response.json();
}

// Utilisation
await sendKey("KEY_VOLUP");
await launchApp("SPOTIFY");
```

---

## ⚡ Limitations et Points importants

1. **Une seule TV** : L'API cible une seule TV (définie dans `config/settings.py`)
2. **Réseau local** : Doit être sur le même réseau que la TV
3. **Port 8002** : La TV doit avoir ce port ouvert
4. **Délai de réponse** : Compter 200-500ms par commande
5. **Token expirant** : Le token peut expirer après plusieurs jours d'inactivité

---

**Dernière mise à jour** : April 2026
