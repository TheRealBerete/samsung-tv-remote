# 📺 Samsung TV Remote Control

Une application web moderne pour contrôler votre TV Samsung à distance via une API WebSocket sécurisée.

## 🎯 Fonctionnalités

- ✅ Télécommande au design réaliste, pensée pour iPhone (ajout à l'écran d'accueil)
- ✅ Navigation, volume, chaînes, lecture, touches couleur, appui long qui répète
- ✅ Lancement d'applications (Netflix, YouTube, Prime Video, Disney+…)
- ✅ Allumage de la TV depuis le téléphone (Wake-on-LAN)
- ✅ Connexion WebSocket persistante (réactive, une seule autorisation sur la TV)
- ✅ Port 8002 (wss + token) avec repli automatique sur 8001 (TV 2016-2017)
- ✅ Statut en direct : TV allumée, en veille ou introuvable
- ✅ Déploiement Docker Compose

## 📋 Prérequis

- Python 3.9+ **ou** Docker
- Une TV Samsung Tizen (2016 et plus récentes) sur le même réseau

## 🚀 Démarrage rapide

### Option A — Docker Compose (recommandé, Linux / Raspberry Pi / NAS)

```bash
git clone https://github.com/TheRealBerete/samsung-tv-remote.git
cd samsung-tv-remote
cp .env.example .env      # puis renseigne TV_IP (et TV_MAC pour l'allumage)
docker compose up -d --build
```

> Le conteneur utilise `network_mode: host` pour joindre la TV et envoyer le
> Wake-on-LAN. Sur Docker Desktop (Windows/macOS), le mode host n'est pas
> toujours disponible : utilise plutôt l'option B.

### Option B — Python

```bash
pip install -r requirements.txt
cp .env.example .env      # ou exporte TV_IP=192.168.x.x
python run.py             # Windows : run.bat
```

Le terminal affiche l'adresse à ouvrir sur le téléphone, par ex. `http://192.168.18.12:5000`.

### Sur l'iPhone

1. Ouvre l'adresse dans Safari (même Wi-Fi que la TV et le serveur).
2. À la première touche, la TV demande l'autorisation : choisis **Autoriser**.
3. Partager → **Sur l'écran d'accueil** pour l'avoir comme une app.

### Configuration (`.env`)

| Variable | Défaut | Rôle |
|---|---|---|
| `TV_IP` | `192.168.18.49` | IP locale de la TV |
| `TV_PORT` | `8002` | `8002` (wss + token) ou `8001` (ws) — repli auto sur l'autre |
| `TV_MAC` | vide | MAC de la TV pour l'allumer (activer aussi « Allumer avec mobile » sur la TV) |
| `FLASK_PORT` | `5000` | Port de l'interface |
| `FLASK_DEBUG` | `false` | Mode debug Flask |

### API

| Méthode | Route | Rôle |
|---|---|---|
| `POST` | `/key/<KEY_*>` | Envoie une touche (`KEY_VOLUP`, `KEY_ENTER`…) |
| `POST` | `/app/<NOM>` | Lance une app (`NETFLIX`, `YOUTUBE`…) |
| `POST` | `/power/on` | Allume la TV (Wake-on-LAN) |
| `GET` | `/status` | État de la TV et de la connexion |
| `GET` | `/keys`, `/apps` | Listes disponibles |

Les erreurs renvoient un code `4xx/5xx` avec `{"success": false, "error": "…"}`.

## 📡 Architecture

```
samsung-tv-remote/
├── backend/
│   ├── app.py              # Application Flask principale
│   └── config.py           # Configuration de l'app
├── frontend/
│   ├── index.html          # Interface web
│   ├── css/
│   │   └── style.css       # Styles
│   └── js/
│       └── app.js          # Logique frontend
├── config/
│   ├── settings.py         # Paramètres globaux
│   └── apps.json           # Liste des apps disponibles
├── docs/
│   ├── API.md              # Documentation API
│   └── SETUP.md            # Guide d'installation détaillé
└── requirements.txt        # Dépendances Python
```

## 🎮 Endpoints API

### Navigation
```
GET  /key/<KEY>              # Envoyer une touche (UP, DOWN, LEFT, RIGHT, ENTER, etc.)
```

### Applications
```
GET  /app/<APP_NAME>         # Lancer une app (NETFLIX, YOUTUBE, SPOTIFY, etc.)
GET  /apps                   # Lister toutes les apps disponibles
```

### Commandes
```
GET  /status                 # État actuel de la TV
POST /command                # Envoyer une commande personnalisée
```

### Exemples d'utilisation

```bash
# Naviguer vers le haut
curl http://localhost:5000/key/KEY_UP

# Lancer Netflix
curl http://localhost:5000/app/NETFLIX

# Monter le volume
curl http://localhost:5000/key/KEY_VOLUP

# Aller à l'accueil
curl http://localhost:5000/key/KEY_HOME
```

## 🔐 Authentification et Token

L'application utilise un système de token automatique :

1. **Premier lancement** : Un token est généré par la TV
2. **Sauvegarde** : Le token est enregistré dans `token.txt`
3. **Reconnexions** : Le token sauvegardé est réutilisé automatiquement
4. **Expiration** : Si le token expire, un nouveau est généré automatiquement

## 🎛️ Touches disponibles

| Touche | Code |
|--------|------|
| Haut | `KEY_UP` |
| Bas | `KEY_DOWN` |
| Gauche | `KEY_LEFT` |
| Droite | `KEY_RIGHT` |
| Entrée | `KEY_ENTER` |
| Home | `KEY_HOME` |
| Volume + | `KEY_VOLUP` |
| Volume - | `KEY_VOLDOWN` |
| Muet | `KEY_MUTE` |
| Chaîne + | `KEY_CHUP` |
| Chaîne - | `KEY_CHDOWN` |
| Menu | `KEY_MENU` |
| Exit | `KEY_EXIT` |
| Guide | `KEY_GUIDE` |
| Source | `KEY_SOURCE` |
| Info | `KEY_INFO` |
| Retour | `KEY_RETURN` |

## 📱 Applications supportées

- Netflix
- YouTube
- Prime Video
- Disney+
- Apple TV
- Spotify
- Navigateur
- Plex
- Et bien d'autres...

## 🛠️ Troubleshooting

### Erreur de connexion
```
❌ Erreur: [Errno 113] No route to host
```
**Solution** : Vérifiez que l'adresse IP de la TV est correcte et qu'elle est sur le même réseau.

### Token invalide
```
❌ Erreur: Connection closed
```
**Solution** : Supprimez `token.txt` et redémarrez l'application.

### Port 8002 déjà utilisé
```
OSError: [Errno 10048] Adresse déjà utilisée
```
**Solution** : Modifiez le port dans `config/settings.py`.

## 📚 Documentation complète

Pour plus de détails :
- 📖 [Guide d'installation détaillé](docs/SETUP.md)
- 🔌 [Documentation API](docs/API.md)
- 🐛 [Troubleshooting](docs/TROUBLESHOOTING.md)

## 🔗 Ressources

- [Samsung Smart TV WebSocket API](https://github.com/xchatter/samsung-tv-ws-api)
- [Documentation officielle Samsung](https://www.samsung.com/us/support/)

## 📄 Licence

Ce projet est sous licence **MIT**. Voir [LICENSE](LICENSE) pour plus de détails.

## 👤 Auteur

**TheRealBerete** - [GitHub Profile](https://github.com/TheRealBerete)

## 🤝 Contribution

Les contributions sont bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## ⭐ Support

Si ce projet vous a aidé, mettez-le en favori ! ⭐

---

**Dernière mise à jour** : April 2026
