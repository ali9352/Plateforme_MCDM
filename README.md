# Aide à la décision multicritère (Streamlit)

Application web d'aide à la décision multicritère (MCDM).

- **Pondération des critères** : Entropie, CRITIC, AHP, BWM
- **Classement des alternatives** : WASPAS, TOPSIS, TOPSIS floue (Chen, 2000)

## Lancer l'application

Prérequis : [Python 3.9+](https://www.python.org/downloads/) installé.

### Méthode rapide (recommandée)

1. Télécharger le projet (bouton vert **Code** → **Download ZIP**) puis le décompresser.
2. Lancer le fichier de démarrage :
   - **Windows** : double-clic sur `lancer.bat`
   - **Mac / Linux** : dans un terminal, `./lancer.sh`

Le script crée un environnement virtuel, installe les dépendances et ouvre l'application dans le navigateur (par défaut : http://localhost:8501).

### Méthode manuelle

```bash
python -m venv venv
venv\Scripts\activate          # Windows   (Mac/Linux : source venv/bin/activate)
pip install -r requirements.txt
streamlit run app.py
```

## Structure du projet

| Fichier | Rôle |
|---|---|
| `app.py` | Page d'accueil : saisie / import de la matrice de décision |
| `pages/1_Ponderation.py` | Calcul des poids des critères |
| `pages/2_Classement.py` | Classement WASPAS / TOPSIS |
| `pages/3_TOPSIS_floue.py` | TOPSIS floue |
| `methods.py` | Implémentation des méthodes MCDM |
| `utils.py`, `ui.py` | Fonctions utilitaires et composants d'interface |
| `lancer.bat` / `lancer.sh` | Scripts de lancement |
