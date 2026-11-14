#!/usr/bin/env bash
# ===== Lanceur Mac / Linux : ./lancer.sh =====
cd "$(dirname "$0")" || exit 1

if ! command -v python3 >/dev/null 2>&1; then
    echo "Python 3 n'est pas installé. Installez-le depuis https://www.python.org/downloads/"
    exit 1
fi

if [ ! -d venv ]; then
    echo "Création de l'environnement virtuel..."
    python3 -m venv venv
fi

source venv/bin/activate
echo "Installation des dépendances..."
python -m pip install -q -r requirements.txt

echo "Lancement de l'application..."
python -m streamlit run app.py
