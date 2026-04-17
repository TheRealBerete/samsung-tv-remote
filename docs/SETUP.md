# 🔧 Guide d'installation détaillé

Guide complet pour mettre en place l'application Samsung TV Remote.

## 📋 Table des matières

1. [Prérequis](#-prérequis)
2. [Installation étape par étape](#-installation-étape-par-étape)
3. [Configuration](#-configuration)
4. [Premiers pas](#-premiers-pas)
5. [Troubleshooting](#-troubleshooting)

---

## ✅ Prérequis

### Système d'exploitation
- Windows 10+ / macOS 10.14+ / Linux (Ubuntu 18.04+)

### Logiciels requis
- **Python 3.8 ou supérieur**
  - [Télécharger Python](https://www.python.org/downloads/)
  - ✅ Cochez "Add Python to PATH" lors de l'installation

- **Git** (optionnel mais recommandé)
  - [Télécharger Git](https://git-scm.com/downloads)

### Matériel
- **TV Samsung** compatible (modèles 2015+)
  - Port WebSocket 8002 accessible
  - Connectée au même réseau que votre PC

### Vérifier la compatibilité

```bash
# Vérifier la version de Python
python --version
# Doit afficher 3.8.0 ou plus

# Vérifier que pip est installé
pip --version
```

---

## 📦 Installation étape par étape

### Étape 1 : Cloner le projet

#### Avec Git (recommandé)
```bash
git clone https://github.com/TheRealBerete/samsung-tv-remote.git
cd samsung-tv-remote
```

#### Ou télécharger en ZIP
- Aller sur [GitHub](https://github.com/TheRealBerete/samsung-tv-remote)
- Cliquer "Code" → "Download ZIP"
- Extraire le fichier ZIP
- Ouvrir le terminal dans ce dossier

### Étape 2 : Créer un environnement virtuel (recommandé)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

Vous verrez `(venv)` au début de votre terminal si c'est bon.

### Étape 3 : Installer les dépendances

```bash
pip install -r requirements.txt
```

Attendez que tous les paquets soient installés. Vous verrez :
```
Successfully installed Flask-2.3.2 websocket-client-1.5.1 ...
```

### Étape 4 : Vérifier l'installation

```bash
# Vérifier que Flask est installé
python -c "import flask; print(flask.__version__)"
# Doit afficher 2.3.2 ou similaire
```

---

## ⚙️ Configuration

### 1. Trouver l'IP de votre TV Samsung

#### Sur Windows
```bash
# Scanner le réseau
arp -a | findstr "samsung"

# Ou vérifier manuellement sur la TV
# Menu → Paramètres → Général → À propos de ce téléviseur → État réseau
```

#### Sur macOS / Linux
```bash
arp -a | grep samsung
# Ou utiliser nmap
nmap -p 8002 192.168.1.0/24
```

#### Méthode simple
- Appuyez sur le bouton **Menu** de la télécommande
- Allez dans **Paramètres**
- Sélectionnez **Réseau**
- Sélectionnez **État réseau**
- Notez l'adresse IP (format: `192.168.X.X`)

### 2. Configurer l'application

Ouvrez `config/settings.py` et modifiez l'IP :

```python
# Avant
TV_IP = "192.168.18.49"

# Après (remplacer par votre IP)
TV_IP = "192.168.1.100"  # ← Votre IP locale
```

**Autres paramètres optionnels** :

```python
# Port Flask (par défaut: 5000)
FLASK_PORT = 5000

# Mode debug (True pour développement)
FLASK_DEBUG = True

# Votre nom (pour l'authentification)
TV_NAME = "TheRealBerete"
```

### 3. Vérifier la connectivité (optionnel)

```bash
# Tester la connexion à la TV
ping 192.168.1.100  # Remplacer par votre IP

# Doit afficher "Reply from 192.168.1.100" (Windows)
# Ou "64 bytes from 192.168.1.100" (macOS/Linux)
```

---

## 🚀 Premiers pas

### Lancer l'application

```bash
# Assurez-vous que (venv) est activé
python backend/app.py
```

Vous verrez :
```
🎮 Remote TV - 192.168.1.100:8002
📱 http://localhost:5000
```

### Accéder à l'interface

1. Ouvrez votre navigateur
2. Allez à http://localhost:5000
3. Vous verrez l'interface de contrôle

### Premier appairage

À la première connexion :
- Un token est généré automatiquement
- Vous devez **approuver l'accès sur la TV** (une notification apparat)
- Le token est sauvegardé dans `token.txt`

**S'il n'y a pas de notification** :
- Allez dans Paramètres → Sécurité → Gestion des appareils
- Approuvez manuellement

---

## 📁 Structure du projet

```
samsung-tv-remote/
│
├── backend/
│   ├── app.py                 # Application principale
│   └── __init__.py
│
├── frontend/
│   ├── index.html            # Interface web
│   ├── css/
│   │   └── style.css         # Styles
│   └── js/
│       └── app.js            # Logique JS
│
├── config/
│   └── settings.py           # Configuration
│
├── docs/
│   ├── API.md                # Documentation API
│   ├── SETUP.md              # Ce fichier
│   └── TROUBLESHOOTING.md    # Dépannage
│
├── README.md                 # Page d'accueil
├── requirements.txt          # Dépendances Python
├── .gitignore                # Fichiers à ignorer
└── token.txt                 # Token (généré automatiquement)
```

---

## 🧪 Tests basiques

### Test 1 : Navigation

```bash
# Ouvrir un nouveau terminal
# (Ne pas fermer le serveur)

# Naviguer vers le haut
curl http://localhost:5000/key/KEY_UP

# Vous devriez voir la TV répondre
```

### Test 2 : Lancer une app

```bash
# Lancer Netflix
curl http://localhost:5000/app/NETFLIX

# Netflix doit s'ouvrir sur la TV
```

### Test 3 : Contrôle du volume

```bash
# Augmenter le volume
curl http://localhost:5000/key/KEY_VOLUP

# Baisser le volume
curl http://localhost:5000/key/KEY_VOLDOWN

# Couper le son
curl http://localhost:5000/key/KEY_MUTE
```

---

## 🔧 Commandes utiles

### Arrêter l'application
```bash
# Appuyer sur Ctrl+C
```

### Réactiver l'environnement virtuel
```bash
# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### Mettre à jour les dépendances
```bash
pip install --upgrade -r requirements.txt
```

### Réinitialiser le token
```bash
# Supprimer le fichier
rm token.txt  # macOS/Linux
del token.txt  # Windows

# Redémarrer l'application
python backend/app.py
```

---

## 🐛 Troubleshooting

### ❌ "No module named 'flask'"

**Cause** : Flask n'est pas installé

**Solution** :
```bash
pip install flask
# Ou réinstaller tout
pip install -r requirements.txt
```

### ❌ "No route to host" ou "Connection refused"

**Cause** : L'IP de la TV est incorrecte ou la TV n'est pas accessible

**Solution** :
1. Vérifiez que l'IP est correcte dans `config/settings.py`
2. Vérifiez que la TV est allumée
3. Vérifiez que vous êtes sur le même réseau (Wi-Fi ou Ethernet)
4. Testez : `ping 192.168.X.X`

### ❌ "Address already in use"

**Cause** : Le port 5000 est déjà utilisé

**Solution** :
1. Modifiez le port dans `config/settings.py` :
   ```python
   FLASK_PORT = 5001  # Utiliser 5001 au lieu de 5000
   ```
2. Accédez à http://localhost:5001

### ❌ "Token expired"

**Cause** : Le token a expiré après plusieurs jours

**Solution** :
```bash
# Supprimer le token et redémarrer
rm token.txt
python backend/app.py
```

### ❌ La TV ne répond pas

**Cause** : La TV ne supporte pas l'API ou le port 8002 n'est pas accessible

**Solution** :
1. Vérifiez que c'est une TV Samsung (modèles 2015+)
2. Allez dans Paramètres → Sécurité → Gestion des appareils
3. Activez "Autoriser les appareils externes"
4. Redémarrez la TV

---

## ✅ Vérification finale

Avant de dire "C'est bon !", vérifiez que :

- ✅ Python 3.8+ est installé
- ✅ Les dépendances sont installées (`pip list` doit montrer flask, websocket-client, etc.)
- ✅ L'IP de la TV est correcte dans `config/settings.py`
- ✅ La TV est connectée au réseau
- ✅ Le serveur démarre sans erreur : `python backend/app.py`
- ✅ Vous pouvez accéder à http://localhost:5000
- ✅ Les commandes fonctionnent : `curl http://localhost:5000/key/KEY_HOME`

---

## 📞 Support et ressources

- **Issues GitHub** : [Signaler un bug](https://github.com/TheRealBerete/samsung-tv-remote/issues)
- **Documentation API** : [API.md](API.md)
- **Dépannage** : [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

**Dernière mise à jour** : April 2026
