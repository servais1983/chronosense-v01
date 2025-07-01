@echo off
REM Chronosense v0.1 - Script d'installation Windows
REM Auteur: Généré automatiquement
REM Version: 0.1

echo.
echo ========================================
echo  Chronosense v0.1 - Installation
echo  Assistant d'Investigation DFIR
echo ========================================
echo.

REM Vérifier que Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé ou pas dans le PATH
    echo.
    echo 📥 Veuillez installer Python 3.11+ depuis:
    echo    https://python.org/downloads/
    echo.
    echo ⚠️  N'oubliez pas de cocher "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo ✅ Python détecté
python --version

REM Vérifier la version de Python
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Version Python: %PYTHON_VERSION%

REM Créer un environnement virtuel
echo.
echo 📦 Création de l'environnement virtuel...
python -m venv chronosense-env
if errorlevel 1 (
    echo ❌ Erreur lors de la création de l'environnement virtuel
    pause
    exit /b 1
)

echo ✅ Environnement virtuel créé

REM Activer l'environnement virtuel
echo.
echo 🔄 Activation de l'environnement virtuel...
call chronosense-env\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Erreur lors de l'activation de l'environnement virtuel
    pause
    exit /b 1
)

echo ✅ Environnement virtuel activé

REM Mettre à jour pip
echo.
echo 🔄 Mise à jour de pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo ⚠️  Avertissement: Impossible de mettre à jour pip
)

REM Installer les dépendances
echo.
echo 📦 Installation des dépendances...
echo    Cela peut prendre plusieurs minutes...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Erreur lors de l'installation des dépendances
    echo.
    echo 🔧 Tentative d'installation individuelle...
    
    REM Installer les dépendances une par une
    pip install networkx
    pip install matplotlib
    pip install pandas
    pip install numpy
    pip install Pillow
    pip install requests
    
    echo.
    echo ⚠️  Dépendances IA optionnelles (peuvent échouer):
    pip install transformers
    pip install torch
)

echo.
echo ✅ Installation des dépendances terminée

REM Tester l'installation
echo.
echo 🧪 Test de l'installation...
python -c "import sys; sys.path.insert(0, 'src'); from graph_manager import GraphManager; from ai_manager import AIManager; print('✅ Modules importés avec succès')"
if errorlevel 1 (
    echo ❌ Erreur lors du test d'importation
    echo    Vérifiez les erreurs ci-dessus
    pause
    exit /b 1
)

REM Créer le script de lancement
echo.
echo 📝 Création du script de lancement...
(
echo @echo off
echo cd /d "%~dp0"
echo call chronosense-env\Scripts\activate.bat
echo python main.py
echo pause
) > lancer_chronosense.bat

echo ✅ Script de lancement créé: lancer_chronosense.bat

REM Créer le répertoire de logs
if not exist "logs" mkdir logs

echo.
echo ========================================
echo  ✅ Installation terminée avec succès!
echo ========================================
echo.
echo 🚀 Pour lancer Chronosense:
echo    1. Double-cliquez sur "lancer_chronosense.bat"
echo    2. Ou exécutez: python main.py
echo.
echo 📚 Documentation:
echo    • README.md - Guide principal
echo    • docs\installation.md - Guide d'installation
echo    • docs\user_guide.md - Guide utilisateur
echo.
echo 🧪 Exemples:
echo    • python examples\sample_investigation.py
echo.
echo 🔧 Configuration IA:
echo    • Mode simulation activé par défaut
echo    • Pour Phi-3: installez Ollama ou configurez Transformers
echo    • Voir docs\installation.md pour plus de détails
echo.
echo 💡 Conseils:
echo    • Utilisez l'environnement virtuel: chronosense-env
echo    • Consultez les logs dans le dossier "logs"
echo    • Testez avec des exemples avant utilisation réelle
echo.

REM Proposer de lancer l'application
set /p LAUNCH="🚀 Voulez-vous lancer Chronosense maintenant? (o/n): "
if /i "%LAUNCH%"=="o" (
    echo.
    echo 🚀 Lancement de Chronosense...
    python main.py
) else if /i "%LAUNCH%"=="oui" (
    echo.
    echo 🚀 Lancement de Chronosense...
    python main.py
)

echo.
echo 👋 Installation terminée. Merci d'utiliser Chronosense!
pause
