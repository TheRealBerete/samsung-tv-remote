# 🐛 Troubleshooting - Samsung TV Remote

Solutions aux problèmes courants.

## 🔴 Erreurs de connexion

### "No route to host" / "Connection refused"

```
❌ Exception: [Errno 113] No route to host
```

**Causes possibles:**
- L'adresse IP est incorrecte
- La TV n'est pas allumée
- La TV n'est pas sur le même réseau
- Le port 8002 n'est pas accessible

**Solutions:**
```bash
# 1. Vérifier l'IP correcte
ping 192.168.1.XX

# 2. Vérifier que la TV est accessible sur le port 8002
nmap -p 8002 192.168.1.XX
# Doit afficher "open"

# 3. Mettre à jour l'IP dans config/settings.py
# TV_IP = "192.168.1.XX"

# 4. Redémarrer l'application
python backend/app.py
```

---

## 🔴 Erreurs d'authentification

### "Token expired" / "Unauthorized"

```
❌ Exception: Connection closed
```

**Solution:**
```bash
# Supprimer le token expiré
rm token.txt

# Redémarrer l'application (génère un nouveau token)
python backend/app.py

# Approuver l'accès sur la TV quand la notification apparaît
```

---

## 🔴 Port déjà utilisé

```
OSError: [Errno 10048] Address already in use
```

**Solutions:**

**Option 1 : Changer le port Flask**
```python
# config/settings.py
FLASK_PORT = 5001  # Au lieu de 5000
```

**Option 2 : Tuer le processus qui utilise le port**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS / Linux
lsof -i :5000
kill -9 <PID>
```

---

## 🔴 Module non trouvé

### "No module named 'flask'"

```
ModuleNotFoundError: No module named 'flask'
```

**Solution:**
```bash
# Réinstaller les dépendances
pip install -r requirements.txt

# Ou installer le module spécifique
pip install flask
```

---

## 🔴 La TV ne répond pas

### Les commandes sont envoyées mais la TV n'en tient pas compte

**Vérifications:**
1. La TV doit être allumée
2. Aller dans **Paramètres → Sécurité → Gestion des appareils**
3. Vérifier que **"Autoriser les appareils externes"** est activé
4. L'appareil doit être approuvé dans la liste

**Solution complète:**
```bash
# 1. Supprimer le token
rm token.txt

# 2. Redémarrer l'application
python backend/app.py

# 3. À la première connexion, approuver sur la TV
# Une notification doit apparître : "Autorisez cet appareil ?"

# 4. Approuvez, puis testez
curl http://localhost:5000/key/KEY_HOME
```

---

## 🔴 Erreur CORS

```
Access to XMLHttpRequest blocked by CORS policy
```

**Solution:**
C'est normal en développement. La solution est déjà appliquée dans le backend :
```python
from flask_cors import CORS
CORS(app)  # ✅ Déjà configuré
```

Si vous avez toujours le problème :
```bash
# Réinstaller flask-cors
pip install --upgrade flask-cors
```

---

## 🔴 Application n'apparaît pas

### Netflix, YouTube, etc. n'existent pas sur la TV

**Cause:** Les IDs d'applications varient selon les modèles de TV et les régions.

**Solution:**
Essayez les alternatives :
```bash
# YouTube
curl http://localhost:5000/app/YOUTUBE_ALT
```

Ou modifiez l'ID dans `config/settings.py` :
```python
APPS = {
    "YOUTUBE": "org.tizen.youtube-app"  # Essayer cet ID
}
```

---

## 🔴 Pas de réaction aux touches

### Les boutons sont cliqués mais la TV ne réagit pas

**Vérifications:**
1. Vérifier que la TV est connectée : `curl http://localhost:5000/status`
2. Vérifier les logs du serveur (chercher les erreurs en rouge)
3. S'assurer que le token est valide (supprimer et régénérer si besoin)

**Debug:**
```bash
# Tester directement une commande
curl http://localhost:5000/key/KEY_VOLUP

# Regarder la réponse
# {"success": true, "cmd": "KEY_VOLUP"}

# Si success=false, il y a un problème de connexion
```

---

## 🔴 Interface web ne charge pas

```
Cannot GET /
```

**Cause:** Le fichier `frontend/index.html` n'existe pas ou le chemin est incorrect.

**Solution:**
```bash
# Vérifier que le fichier existe
ls frontend/index.html

# Vérifier le chemin dans backend/app.py
# Doit être : return send_from_directory(FRONTEND_DIR, 'index.html')

# Redémarrer l'application
python backend/app.py
```

---

## ⚠️ Avertissements (non-bloquants)

### "DeprecationWarning"

```
DeprecationWarning: ...
```

Cela peut être ignoré. C'est juste un avertissement des dépendances.

---

## ✅ Checklist de diagnostic

Si rien ne marche, vérifiez cela dans l'ordre :

- [ ] Python 3.8+ installé : `python --version`
- [ ] Flask installé : `python -c "import flask"`
- [ ] websocket-client installé : `python -c "import websocket"`
- [ ] IP correcte dans `config/settings.py`
- [ ] TV allumée et sur le même réseau
- [ ] Port 8002 accessible : `ping 192.168.X.X`
- [ ] Pas de processus bloquant le port 5000
- [ ] Token valide ou supprimé (génération auto)
- [ ] Navigateur à jour (Chrome, Edge, Safari...)
- [ ] Pas de VPN/proxy bloquant les connexions locales

---

## 📞 Besoin d'aide ?

- **Issues GitHub** : [Signaler le problème](https://github.com/TheRealBerete/samsung-tv-remote/issues)
- **Logs** : Regardez la console du serveur pour les erreurs en rouge
- **API Status** : `curl http://localhost:5000/status`

---

**Dernière mise à jour** : April 2026
