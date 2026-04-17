#!/usr/bin/env python3
"""
Script de lancement du serveur Samsung TV Remote Control
À exécuter depuis la racine du projet : python run.py
"""

import sys
import os

# Ajouter le chemin du backend au sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Importer et lancer l'application
if __name__ == '__main__':
    from backend.app import app
    print("\n" + "="*50)
    print("🎮 Samsung TV Remote Control")
    print("="*50)
    print("\n✅ Serveur en cours de démarrage...")
    print("   Ouvrez http://localhost:5000 dans votre navigateur\n")
    app.run(host='0.0.0.0', port=5000, debug=True)
