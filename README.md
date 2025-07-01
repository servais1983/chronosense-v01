# Chronosense v0.1 - Assistant d'Investigation DFIR

![Chronosense Logo](docs/logo.png)

**Chronosense** est un assistant d'investigation DFIR (Digital Forensics and Incident Response) qui utilise l'intelligence artificielle locale pour augmenter l'intuition de l'analyste. L'outil fonctionne comme un "co-pilote cognitif" qui aide à formuler des hypothèses et à visualiser les liens entre les artéfacts d'investigation.

## 🎯 Philosophie du Projet

Chronosense n'est pas un simple visualiseur de logs. Il incarne le concept de **co-pilote cognitif** pour l'investigation DFIR. L'objectif est d'augmenter l'intuition de l'analyste en l'aidant à :

- Formuler des hypothèses d'attaque basées sur les TTPs MITRE ATT&CK
- Visualiser les liens entre les artéfacts
- Proposer des actions d'investigation concrètes
- Maintenir une vue d'ensemble de l'investigation

## ✨ Fonctionnalités

### 🔍 Gestion d'Artéfacts
- Ajout dynamique d'artéfacts (IP, hash, fichiers, processus, domaines)
- Détection automatique du type d'artéfact
- Création de liens entre artéfacts
- Visualisation en temps réel du graphe d'investigation

### 🧠 Intelligence Artificielle Locale
- Intégration du modèle Microsoft Phi-3 en local
- Génération d'hypothèses d'attaque basées sur MITRE ATT&CK
- Propositions d'actions d'investigation concrètes
- Analyse contextuelle des patterns d'artéfacts

### 📊 Visualisation Interactive
- Graphe d'investigation dynamique avec NetworkX
- Interface graphique intuitive avec Tkinter
- Affichage des détails et hypothèses en temps réel
- Couleurs différenciées par type d'artéfact

## 🛠️ Stack Technique

- **Langage** : Python 3.11+
- **Interface Graphique** : Tkinter (standard Python)
- **Gestion de Graphe** : NetworkX
- **Visualisation** : Matplotlib
- **IA Locale** : Microsoft Phi-3 via Transformers/Ollama
- **Manipulation de Données** : Pandas

## 📋 Prérequis

### Système
- Python 3.11 ou supérieur
- 8 GB RAM minimum (16 GB recommandé pour l'IA)
- 10 GB d'espace disque libre

### Dépendances Python
Toutes les dépendances sont listées dans `requirements.txt` :

```
networkx>=3.0
matplotlib>=3.5.0
pandas>=1.5.0
transformers>=4.30.0
torch>=2.0.0
numpy>=1.21.0
Pillow>=9.0.0
requests>=2.28.0
```

## 🚀 Installation

### Installation Rapide

1. **Cloner le projet**
```bash
git clone https://github.com/servais1983/chronosense-v01.git
cd chronosense-v01
```

2. **Créer un environnement virtuel**
```bash
python -m venv chronosense-env
source chronosense-env/bin/activate  # Linux/Mac
# ou
chronosense-env\Scripts\activate     # Windows
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Lancer l'application**
```bash
python main.py
```

### Installation Windows (Automatique)
```cmd
# Télécharger le projet et double-cliquer sur
install.bat
```

### Configuration du Modèle IA

#### Option 1 : Transformers (Hugging Face)
Le modèle Phi-3 sera téléchargé automatiquement au premier lancement.

#### Option 2 : Ollama (Recommandé)
1. Installer Ollama : https://ollama.ai/
2. Télécharger le modèle Phi-3 :
```bash
ollama pull phi3
```
3. Lancer Ollama en arrière-plan :
```bash
ollama serve
```

#### Option 3 : Mode Simulation
Si aucun modèle n'est disponible, Chronosense fonctionne en mode simulation avec des hypothèses pré-programmées.

## 📖 Guide d'Utilisation

### Démarrage Rapide

1. **Lancer l'application**
```bash
python main.py
```

2. **Ajouter des artéfacts**
   - Saisir un artéfact dans le champ de texte
   - Cliquer sur "Ajouter Artéfact" ou appuyer sur Entrée
   - L'artéfact apparaît dans le graphe avec une couleur selon son type

3. **Créer des liens**
   - Cliquer sur "Lier Nœuds Sélectionnés"
   - Sélectionner deux artéfacts dans la liste déroulante
   - Le lien apparaît dans le graphe

4. **Générer des hypothèses**
   - Cliquer sur "Générer des Hypothèses"
   - L'IA analyse le graphe et propose des hypothèses d'attaque
   - Les résultats s'affichent dans le panneau de droite

### Exemples d'Artéfacts

#### Adresses IP
```
192.168.1.100
8.8.8.8
10.0.0.1
```

#### Hash Cryptographiques
```
d41d8cd98f00b204e9800998ecf8427e
5d41402abc4b2a76b9719d911017c592
```

#### Fichiers
```
evil.exe
malware.dll
suspicious.bat
trojan.ps1
```

#### Processus
```
powershell.exe
cmd.exe
rundll32.exe
svchost.exe
```

#### Domaines
```
malicious-site.com
c2-server.net
phishing-domain.org
```

## 🏗️ Architecture du Code

### Structure des Fichiers
```
chronosense-v01/
├── main.py                 # Point d'entrée principal
├── requirements.txt        # Dépendances Python
├── README.md              # Documentation principale
├── install.bat            # Script d'installation Windows
├── config.json.example    # Exemple de configuration
├── src/                   # Code source
│   ├── chronosense_app.py # Interface principale Tkinter
│   ├── graph_manager.py   # Gestion du graphe NetworkX
│   └── ai_manager.py      # Intégration IA Phi-3
├── docs/                  # Documentation
│   └── installation.md   # Guide d'installation détaillé
├── examples/              # Exemples d'utilisation
│   └── sample_investigation.py
└── tests/                 # Tests unitaires
    └── test_graph_manager.py
```

### Classes Principales

#### ChronosenseApp
- Gère l'interface utilisateur Tkinter
- Coordonne les interactions entre composants
- Gère les événements utilisateur

#### GraphManager
- Gère le graphe NetworkX
- Visualisation avec Matplotlib
- Détection automatique des types d'artéfacts

#### AIManager
- Interface avec le modèle Phi-3
- Génération de prompts structurés
- Post-traitement des réponses IA

## 🔧 Configuration Avancée

### Variables d'Environnement

```bash
# Configuration du modèle IA
CHRONOSENSE_AI_MODEL=microsoft/Phi-3-mini-4k-instruct
CHRONOSENSE_AI_MODE=transformers  # ou "api" ou "simulation"
CHRONOSENSE_API_URL=http://localhost:11434/api/generate

# Configuration de l'interface
CHRONOSENSE_WINDOW_SIZE=1200x800
CHRONOSENSE_THEME=default
```

### Fichier de Configuration

Copier `config.json.example` vers `config.json` et modifier selon vos besoins.

## 🧪 Tests

### Lancer les Tests
```bash
# Tests unitaires
python tests/test_graph_manager.py

# Test d'exemple
python examples/sample_investigation.py
```

## 🐛 Dépannage

### Problèmes Courants

#### Erreur de Modèle IA
```
ModuleNotFoundError: No module named 'transformers'
```
**Solution** : Installer les dépendances manquantes
```bash
pip install transformers torch
```

#### Erreur d'Affichage Graphique
```
TclError: no display name and no $DISPLAY environment variable
```
**Solution** : Configurer l'affichage X11 ou utiliser un environnement graphique

#### Modèle IA Lent
**Solution** : Utiliser Ollama ou réduire la taille du modèle

### Logs de Débogage

Activer les logs détaillés :
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contribution

### Développement

1. Fork le projet
2. Créer une branche feature
3. Commiter les changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

### Standards de Code

- PEP 8 pour le style Python
- Docstrings pour toutes les fonctions
- Tests unitaires pour les nouvelles fonctionnalités
- Type hints recommandés

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🙏 Remerciements

- **Microsoft** pour le modèle Phi-3
- **NetworkX** pour la gestion de graphes
- **Matplotlib** pour la visualisation
- **Hugging Face** pour l'écosystème Transformers
- **MITRE** pour le framework ATT&CK

## 📞 Support

- **Issues** : https://github.com/servais1983/chronosense-v01/issues
- **Discussions** : https://github.com/servais1983/chronosense-v01/discussions

## 🗺️ Roadmap

### Version 0.2 (Prochaine)
- [ ] Import/Export de graphes d'investigation
- [ ] Intégration avec des APIs de threat intelligence
- [ ] Rapports d'investigation automatisés
- [ ] Interface web optionnelle

### Version 0.3 (Future)
- [ ] Analyse de logs automatisée
- [ ] Intégration SIEM
- [ ] Collaboration multi-utilisateurs
- [ ] Plugins personnalisés

---

**Chronosense v0.1** - Développé avec ❤️ pour la communauté DFIR
