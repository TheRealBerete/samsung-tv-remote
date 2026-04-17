# 🏗️ Architecture du Projet

## Diagramme de l'architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Utilisateur (Browser)                   │
│                   http://localhost:5000                     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ HTTP/REST
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Frontend (HTML/CSS/JavaScript)                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  frontend/                                           │   │
│  │  ├── index.html          (Interface Web)             │   │
│  │  ├── css/                                            │   │
│  │  │   └── style.css       (Styles Modernos)           │   │
│  │  └── js/                                             │   │
│  │      └── app.js          (Logique d'interaction)     │   │
│  └──────────────────────────────────────────────────────┘   │
│                         │                                    │
│                         │ Fetch API (/key, /app)             │
│                         ▼                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         Flask Backend (Python)                       │   │
│  │  ┌──────────────────────────────────────────────┐    │   │
│  │  │  backend/app.py                              │    │   │
│  │  │                                              │    │   │
│  │  │  Routes:                                     │    │   │
│  │  │  • GET  /                (Serve HTML)        │    │   │
│  │  │  • GET  /key/<cmd>        (Navigation)       │    │   │
│  │  │  • GET  /app/<name>       (Launch App)       │    │   │
│  │  │  • GET  /apps            (List Apps)        │    │   │
│  │  │  • GET  /keys            (List Keys)        │    │   │
│  │  │  • GET  /status          (TV Status)        │    │   │
│  │  └──────────────────────────────────────────────┘    │   │
│  │                         │                            │   │
│  │                         │ WebSocket (WSS)             │   │
│  │                         ▼                            │   │
│  │  ┌──────────────────────────────────────────────┐    │   │
│  │  │  config/settings.py (Configuration)          │    │   │
│  │  │  • TV_IP, TV_PORT, APPS, KEYS, etc.         │    │   │
│  │  └──────────────────────────────────────────────┘    │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────┬───────────────────────────┘
                                  │
                                  │ WSS://192.168.X.X:8002
                                  │ /api/v2/channels/samsung.remote.control
                                  ▼
                    ┌─────────────────────────┐
                    │   Samsung Smart TV      │
                    │  (Port 8002 WebSocket)  │
                    │                         │
                    │  • Navigation           │
                    │  • Applications         │
                    │  • Media Control        │
                    │  • Power Management     │
                    └─────────────────────────┘
```

## Stack Technologique

### Backend
- **Framework** : Flask 2.3.2
  - Lightweight Python web framework
  - REST API endpoints
  - File serving (HTML/CSS/JS)

- **Communication** : WebSocket (websocket-client 1.5.1)
  - Real-time bidirectional communication
  - Secure WSS (WebSocket Secure) support
  - Token-based authentication

- **Features** :
  - Flask-CORS pour les requêtes cross-origin
  - SSL/TLS support (certificats auto-signés)
  - Gestion automatique des tokens
  - Configuration externalisée

### Frontend
- **HTML5** : Interface sémantique
- **CSS3** : Design moderne
  - Glassmorphism effects
  - Responsive design
  - Animations fluides
- **Vanilla JavaScript** : Pas de dépendances
  - Fetch API
  - Event handling
  - Haptic feedback

### Infrastructure
- **Python 3.8+** : Runtime
- **pip** : Package management
- **Git** : Version control
- **GitHub** : Code hosting

---

## Flux de données

### 1. Envoi d'une commande (ex: KEY_UP)

```
Utilisateur clique sur ▲
    ↓
JavaScript: fetch('/key/KEY_UP')
    ↓
Flask Backend reçoit la requête
    ↓
send_key('KEY_UP') → send_command()
    ↓
Créer une connexion WebSocket
    ↓
Formater le payload JSON
    ↓
Envoyer via WSS à la TV
    ↓
TV reçoit et exécute la commande
    ↓
Retour : {"success": true, "cmd": "KEY_UP"}
    ↓
Frontend reçoit la réponse
    ↓
Vibration haptique (feedback utilisateur)
```

### 2. Lancement d'une app (ex: NETFLIX)

```
Utilisateur clique sur "Netflix"
    ↓
JavaScript: fetch('/app/NETFLIX')
    ↓
Flask Backend reçoit la requête
    ↓
Lookup l'ID de l'app : "org.tizen.netflix-app"
    ↓
launch_app(app_id) → send_command()
    ↓
Créer une connexion WebSocket
    ↓
Formater le payload JSON (ms.channel.emit)
    ↓
Envoyer via WSS à la TV
    ↓
TV reçoit et lance l'application
    ↓
Retour : {"success": true, "app": "NETFLIX", "app_id": "..."}
    ↓
Frontend reçoit la réponse
    ↓
Vibration haptique (feedback utilisateur)
```

### 3. Gestion des tokens

```
Première connexion
    ↓
Token n'existe pas → génération automatique
    ↓
TV généré un token et le renvoie
    ↓
Backend sauvegarde dans token.txt
    ↓
Affichage : "✅ Token sauvegardé"

Reconnexions suivantes
    ↓
Token chargé depuis token.txt
    ↓
Token ajouté à l'URL WebSocket
    ↓
Authentification automatique
    ↓
Si token expire : nouveau token généré
```

---

## Fichiers importants

### Configuration
- [config/settings.py](../config/settings.py) - Tous les paramètres
- [requirements.txt](../requirements.txt) - Dépendances Python

### Backend
- [backend/app.py](../backend/app.py) - Application principale
- [backend/__init__.py](../backend/__init__.py) - Module init

### Frontend
- [frontend/index.html](../frontend/index.html) - Page web
- [frontend/css/style.css](../frontend/css/style.css) - Styles
- [frontend/js/app.js](../frontend/js/app.js) - Logique

### Documentation
- [README.md](../README.md) - Guide d'accueil
- [docs/SETUP.md](SETUP.md) - Installation détaillée
- [docs/API.md](API.md) - Documentation API
- [docs/TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Dépannage
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution
- [LICENSE](../LICENSE) - Licence MIT

---

## Sécurité

### Token authentication
- Token généré automatiquement par la TV
- Sauvegardé localement dans `token.txt`
- Inclus dans chaque requête WebSocket
- Réexpédition automatique en cas d'expiration

### SSL/TLS
- Certificats auto-signés acceptés
- WSS (WebSocket Secure) par défaut
- Pas de validation du certificat côté client (pour simplicité)

### CORS
- Activé pour les développements locaux
- Peut être configuré pour des domaines spécifiques

---

## Performance

### Latence typique
- **Navigation** : 200-300ms
- **Lancement d'app** : 500-1000ms
- **Requête API** : ~50ms (sans latence réseau)

### Limitations
- Une seule TV à la fois
- Connexion sur le réseau local uniquement
- Rate limiting recommandé en production

---

## Déploiement production

Pour passer en production :

1. **Serveur WSGI** (gunicorn, waitress)
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 backend.app:app
   ```

2. **Variables d'environnement**
   ```bash
   export TV_IP=192.168.1.100
   export FLASK_ENV=production
   export FLASK_DEBUG=False
   ```

3. **HTTPS/SSL**
   - Ajouter reverse proxy (nginx)
   - Certificats SSL valides
   - HSTS headers

4. **Monitoring**
   - Logs structurés
   - Health checks
   - Alertes

---

## Évolutions possibles

- [ ] Support multi-TV
- [ ] Authentification utilisateur
- [ ] Base de données (favoris, historique)
- [ ] Mobile app (React Native)
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Tests unitaires
- [ ] Webhooks
- [ ] Support macros/scripts
- [ ] Web socket pour mises à jour temps réel

---

**Dernière mise à jour** : April 2026
