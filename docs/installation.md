# Guide d'Installation Détaillé - Chronosense v0.1

Ce guide vous accompagne pas à pas dans l'installation et la configuration de Chronosense v0.1.

## 📋 Prérequis Système

### Configuration Minimale
- **OS** : Windows 10/11, macOS 10.15+, ou Linux Ubuntu 18.04+
- **Python** : Version 3.11 ou supérieure
- **RAM** : 8 GB minimum
- **Stockage** : 10 GB d'espace libre
- **Réseau** : Connexion Internet pour le téléchargement des modèles

### Configuration Recommandée
- **RAM** : 16 GB ou plus
- **CPU** : Processeur multi-cœurs (Intel i5/AMD Ryzen 5 ou supérieur)
- **GPU** : NVIDIA avec CUDA (optionnel, pour accélération IA)

## 🐍 Installation de Python

### Windows
1. Télécharger Python depuis https://python.org/downloads/
2. Cocher "Add Python to PATH" lors de l'installation
3. Vérifier l'installation :
```cmd
python --version
pip --version
```

### macOS
```bash
# Avec Homebrew (recommandé)
brew install python@3.11

# Ou télécharger depuis python.org
```

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3.11 python3.11-pip python3.11-venv
```

## 📦 Installation de Chronosense

### Méthode 1 : Installation Standard

1. **Télécharger le projet**
```bash
# Via Git
git clone https://github.com/servais1983/chronosense-v01.git
cd chronosense-v01

# Ou télécharger le ZIP et extraire
```

2. **Créer un environnement virtuel**
```bash
# Windows
python -m venv chronosense-env
chronosense-env\Scripts\activate

# macOS/Linux
python3 -m venv chronosense-env
source chronosense-env/bin/activate
```

3. **Installer les dépendances**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. **Tester l'installation**
```bash
python main.py
```

### Méthode 2 : Installation avec Conda

1. **Installer Miniconda/Anaconda**
   - Télécharger depuis https://conda.io/miniconda.html

2. **Créer l'environnement**
```bash
conda create -n chronosense python=3.11
conda activate chronosense
```

3. **Installer les dépendances**
```bash
conda install networkx matplotlib pandas numpy pillow requests
pip install transformers torch
```

## 🧠 Configuration de l'IA

### Option 1 : Transformers (Hugging Face)

Cette méthode télécharge automatiquement le modèle Phi-3.

**Avantages :**
- Installation automatique
- Pas de configuration supplémentaire

**Inconvénients :**
- Téléchargement initial long (~2-4 GB)
- Utilisation RAM importante

**Installation :**
```bash
pip install transformers torch
```

Le modèle sera téléchargé au premier lancement.

### Option 2 : Ollama (Recommandé)

Ollama offre de meilleures performances et une gestion simplifiée des modèles.

**Installation d'Ollama :**

**Windows :**
1. Télécharger depuis https://ollama.ai/download
2. Installer l'exécutable
3. Ouvrir un terminal et taper :
```cmd
ollama pull phi3
```

**macOS :**
```bash
# Avec Homebrew
brew install ollama

# Ou télécharger depuis ollama.ai
ollama pull phi3
```

**Linux :**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull phi3
```

**Démarrage d'Ollama :**
```bash
# Démarrer le service
ollama serve

# Dans un autre terminal, tester
ollama run phi3 "Hello, how are you?"
```

### Option 3 : Mode Simulation

Si aucun modèle IA n'est disponible, Chronosense fonctionne en mode simulation.

**Avantages :**
- Aucune configuration requise
- Démarrage instantané
- Idéal pour les tests

**Limitations :**
- Hypothèses pré-programmées
- Pas d'analyse contextuelle réelle

## 🔧 Configuration Avancée

### Variables d'Environnement

Créer un fichier `.env` dans le répertoire du projet :

```bash
# Configuration IA
CHRONOSENSE_AI_MODEL=microsoft/Phi-3-mini-4k-instruct
CHRONOSENSE_AI_MODE=ollama
CHRONOSENSE_API_URL=http://localhost:11434/api/generate

# Configuration Interface
CHRONOSENSE_WINDOW_SIZE=1400x900
CHRONOSENSE_DEBUG=false

# Configuration Logging
CHRONOSENSE_LOG_LEVEL=INFO
CHRONOSENSE_LOG_FILE=logs/chronosense.log
```

### Fichier de Configuration JSON

Créer `config/settings.json` :

```json
{
  "ai": {
    "model_name": "microsoft/Phi-3-mini-4k-instruct",
    "mode": "ollama",
    "max_tokens": 512,
    "temperature": 0.7,
    "api_url": "http://localhost:11434/api/generate",
    "timeout": 60
  },
  "interface": {
    "window_size": "1400x900",
    "theme": "default",
    "font_size": 10,
    "graph_layout": "spring"
  },
  "graph": {
    "node_colors": {
      "ip": "#FF6B6B",
      "hash": "#4ECDC4",
      "file": "#45B7D1",
      "process": "#96CEB4",
      "domain": "#FFEAA7",
      "default": "#DDA0DD"
    },
    "node_size": 1000,
    "edge_width": 2
  },
  "logging": {
    "level": "INFO",
    "file": "logs/chronosense.log",
    "max_size": "10MB",
    "backup_count": 5
  }
}
```

## 🧪 Vérification de l'Installation

### Test Rapide

1. **Lancer l'application**
```bash
python main.py
```

2. **Vérifier l'interface**
   - La fenêtre Chronosense doit s'ouvrir
   - Le graphe vide doit être visible
   - Les contrôles doivent être fonctionnels

3. **Tester l'ajout d'artéfacts**
   - Ajouter une IP : `192.168.1.1`
   - Ajouter un fichier : `malware.exe`
   - Vérifier que les nœuds apparaissent

4. **Tester l'IA**
   - Cliquer sur "Générer des Hypothèses"
   - Vérifier qu'une réponse s'affiche

### Tests Automatisés

```bash
# Tests unitaires
python -m pytest tests/ -v

# Test d'intégration
python tests/test_integration.py

# Test de performance
python tests/test_performance.py
```

## 🐛 Résolution de Problèmes

### Erreurs Courantes

#### 1. ModuleNotFoundError
```
ModuleNotFoundError: No module named 'networkx'
```
**Solution :**
```bash
pip install networkx
# ou
pip install -r requirements.txt
```

#### 2. Erreur d'affichage Tkinter
```
TclError: no display name and no $DISPLAY environment variable
```
**Solution Linux :**
```bash
export DISPLAY=:0
# ou utiliser X11 forwarding pour SSH
ssh -X user@server
```

#### 3. Erreur de modèle IA
```
OSError: [Errno 28] No space left on device
```
**Solution :**
- Libérer de l'espace disque
- Utiliser le mode simulation temporairement

#### 4. Erreur de permissions
```
PermissionError: [Errno 13] Permission denied
```
**Solution :**
```bash
# Changer les permissions
chmod +x main.py

# Ou utiliser sudo (non recommandé)
sudo python main.py
```

### Logs de Débogage

Activer les logs détaillés :

```python
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)
```

### Performance

#### Optimisation Mémoire
```python
# Dans config.json
{
  "ai": {
    "max_tokens": 256,  # Réduire pour économiser la RAM
    "batch_size": 1
  }
}
```

#### Optimisation CPU
```python
# Utiliser moins de threads
import os
os.environ['OMP_NUM_THREADS'] = '2'
```

## 🔄 Mise à Jour

### Mise à jour du Code
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

### Mise à jour des Modèles
```bash
# Ollama
ollama pull phi3

# Transformers (automatique au redémarrage)
```

## 🗑️ Désinstallation

### Suppression Complète
```bash
# Désactiver l'environnement virtuel
deactivate

# Supprimer le répertoire
rm -rf chronosense-v01/
rm -rf chronosense-env/

# Ollama (optionnel)
ollama rm phi3
```

## 📞 Support

Si vous rencontrez des problèmes :

1. Consulter cette documentation
2. Lancer le script de diagnostic
3. Vérifier les logs
4. Ouvrir une issue sur GitHub
5. Contacter le support : support@chronosense.dev

---

**Installation réussie ?** Consultez le [Guide Utilisateur](user_guide.md) pour commencer votre première investigation !
