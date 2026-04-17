# Contributing to Samsung TV Remote

Merci de votre intérêt pour contribuer à ce projet ! 🎉

## 📋 Comment contribuer

### 1. Reporter un bug

Créez une [issue GitHub](https://github.com/TheRealBerete/samsung-tv-remote/issues) avec :
- Une description claire du problème
- Vos étapes de reproduction
- La version de Python et votre OS
- Les logs d'erreur

### 2. Proposer une amélioration

- Ouvrez une [discussion](https://github.com/TheRealBerete/samsung-tv-remote/discussions)
- Décrivez votre idée
- Expliquez pourquoi c'est utile

### 3. Soumettre du code

#### Fork et cloner
```bash
git clone https://github.com/YOUR_USERNAME/samsung-tv-remote.git
cd samsung-tv-remote
```

#### Créer une branche
```bash
git checkout -b feature/ma-nouvelle-fonctionnalite
```

#### Faire vos changements
- Respectez le style de code existant
- Ajoutez des docstrings aux fonctions
- Testez votre code

#### Committer et pousser
```bash
git add .
git commit -m "feat: description de ma fonctionnalité"
git push origin feature/ma-nouvelle-fonctionnalite
```

#### Ouvrir une Pull Request
- Allez sur GitHub
- Cliquez "Create Pull Request"
- Décrivez vos changements

---

## 🎨 Style de code

### Python
```python
# ✅ BON
def send_key(key: str) -> bool:
    """
    Envoyer une touche de télécommande.
    
    Args:
        key: Code de la touche (ex: KEY_UP)
    
    Returns:
        True si succès, False sinon
    """
    pass

# ❌ MAUVAIS
def sendkey(key):
    pass
```

### JavaScript
```javascript
// ✅ BON
async function launchApp(appName) {
    // Commentaires clairs
    const response = await fetch(`/app/${appName}`);
    const data = await response.json();
    return data.success;
}

// ❌ MAUVAIS
async function launchApp(a) {
    let res = await fetch(`/app/${a}`);
    let data = await res.json();
}
```

---

## 🧪 Tests

```bash
# Test manuel rapide
python backend/app.py

# Puis dans un autre terminal
curl http://localhost:5000/status
curl http://localhost:5000/key/KEY_UP
curl http://localhost:5000/app/NETFLIX
```

---

## 📝 Messages de commit

Format [Conventional Commits](https://www.conventionalcommits.org/fr/):

```
feat: ajouter une nouvelle fonctionnalité
fix: corriger un bug
docs: mettre à jour la documentation
refactor: restructurer du code
test: ajouter des tests
```

Exemples:
```
feat: support des commandes personnalisées
fix: résoudre le problème du token expirant
docs: ajouter guide d'installation pour macOS
```

---

## 🔄 Processus de révision

1. Votre PR est testée automatiquement
2. Révision par un mainteneur
3. Retours/changements demandés si nécessaire
4. Fusion une fois approuvée

---

## 📚 Ressources

- [GitHub Guides](https://guides.github.com/)
- [Python PEP8](https://www.python.org/dev/peps/pep-0008/)
- [Documentation Flask](https://flask.palletsprojects.com/)

---

Merci encore pour votre contribution ! ⭐
