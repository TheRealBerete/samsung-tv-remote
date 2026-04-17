# 📺 Samsung TV Remote Control

Une application web moderne pour contrôler votre TV Samsung à distance via une API WebSocket sécurisée.

## 🎯 Fonctionnalités

- ✅ Contrôle complet de la TV (navigation, volume, chaînes)
- ✅ Lancement d'applications directement depuis l'interface
- ✅ Authentification tokenisée (sauvegarde automatique)
- ✅ Interface web responsive et intuitive
- ✅ Support HTTPS/WSS pour sécurité maximale
- ✅ Token persistent entre les redémarrages

## 📋 Prérequis

- **Python 3.8+**
- **pip** (gestionnaire de paquets Python)
- **Une TV Samsung compatible** (modèles récents avec port 8002)
- Réseau local avec connexion à la TV

## 🚀 Installation rapide

### 1️⃣ Cloner le projet

```bash
git clone https://github.com/TheRealBerete/samsung-tv-remote.git
cd samsung-tv-remote
```

### 2️⃣ Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3️⃣ Configurer votre TV

Modifiez `config/settings.py` avec l'adresse IP de votre TV :

```python
TV_IP = "192.168.1.XX"  # 👈 Votre adresse IP locale
```

### 4️⃣ Lancer le serveur

```bash
python backend/app.py
```

L'application sera accessible à :
- **Interface web** : http://localhost:5000
- **API REST** : http://localhost:5000/api/

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
