#!/usr/bin/env python3
"""
Chronosense v0.1 - Assistant d'Investigation DFIR
Point d'entrée principal de l'application

Auteur: Généré automatiquement
Version: 0.1 (Preuve de Concept)
"""

import sys
import os

# Ajouter le répertoire src au path pour les imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from chronosense_app import ChronosenseApp

def main():
    """
    Fonction principale pour lancer l'application Chronosense
    """
    try:
        print("Démarrage de Chronosense v0.1...")
        print("Assistant d'Investigation DFIR avec IA Locale")
        print("-" * 50)
        
        # Créer et lancer l'application
        app = ChronosenseApp()
        app.run()
        
    except KeyboardInterrupt:
        print("\nArrêt de l'application demandé par l'utilisateur.")
    except Exception as e:
        print(f"Erreur lors du démarrage de l'application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
