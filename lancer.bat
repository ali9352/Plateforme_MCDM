@echo off
REM ===== Lanceur Windows : double-cliquez sur ce fichier =====
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
    echo Python n'est pas installe. Installez-le depuis https://www.python.org/downloads/
    echo ^(cochez "Add Python to PATH" pendant l'installation^)
    pause
    exit /b 1
)

if not exist venv (
    echo Creation de l'environnement virtuel...
    python -m venv venv
)

call venv\Scripts\activate
echo Installation des dependances...
python -m pip install -q -r requirements.txt

echo Lancement de l'application...
python -m streamlit run app.py
pause
