import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------------
# Exemples de matrices de décision (toutes les valeurs sont > 0, requis par
# la méthode de l'Entropie). Chaque exemple : description, critères, types,
# alternatives et données.
# ---------------------------------------------------------------------------
EXEMPLES = {
    "💼 Choix d'un portefeuille d'investissement": {
        "description": "Comparer 5 classes d'actifs selon leur rendement, leur risque et leurs coûts.",
        "alternatives": ["Actions", "Obligations", "Mixte", "Immobilier", "Tech"],
        "criteres": ["Rendement (%)", "Volatilité (%)", "Sharpe", "Drawdown max (%)", "Frais (%)"],
        "types": ["max", "min", "max", "min", "min"],
        "data": [
            [12.5, 18.0, 0.58, 35, 0.8],
            [4.2, 5.5, 0.40, 12, 0.3],
            [8.1, 10.2, 0.60, 20, 0.6],
            [6.8, 8.5, 0.56, 18, 1.2],
            [16.0, 25.0, 0.56, 45, 1.0],
        ],
    },
    "📱 Choix d'un smartphone": {
        "description": "Sélectionner un smartphone selon le prix, l'autonomie, la photo, le poids et la performance.",
        "alternatives": ["Galaxy S", "iPhone", "Pixel", "Xiaomi 14", "OnePlus 12", "Nothing Phone"],
        "criteres": ["Prix (€)", "Autonomie (h)", "Score photo", "Poids (g)", "Performance (score)"],
        "types": ["min", "max", "max", "min", "max"],
        "data": [
            [899, 15, 92, 195, 88],
            [999, 17, 94, 187, 96],
            [799, 14, 96, 199, 82],
            [749, 16, 90, 188, 90],
            [769, 18, 86, 220, 91],
            [549, 13, 78, 201, 68],
        ],
    },
    "🏭 Sélection d'un fournisseur": {
        "description": "Évaluer des fournisseurs sur le coût, le délai, la qualité, la fiabilité et la distance.",
        "alternatives": ["Fournisseur A", "Fournisseur B", "Fournisseur C", "Fournisseur D", "Fournisseur E"],
        "criteres": ["Coût unitaire (€)", "Délai livraison (j)", "Qualité (%)", "Fiabilité (/10)", "Distance (km)"],
        "types": ["min", "min", "max", "max", "min"],
        "data": [
            [12.5, 7, 96, 8.5, 350],
            [10.8, 12, 91, 7.0, 1200],
            [14.2, 4, 98, 9.2, 150],
            [9.9, 20, 85, 6.5, 4800],
            [11.7, 9, 94, 8.0, 700],
        ],
    },
    "🌱 Choix d'une énergie renouvelable": {
        "description": "Comparer des filières énergétiques selon coût, émissions, rendement, disponibilité et emplois.",
        "alternatives": ["Solaire PV", "Éolien terrestre", "Éolien offshore", "Hydraulique", "Biomasse", "Géothermie"],
        "criteres": ["Investissement (M€/MW)", "Émissions CO₂ (g/kWh)", "Rendement (%)",
                     "Facteur de capacité (%)", "Emplois (/MW)"],
        "types": ["min", "min", "max", "max", "max"],
        "data": [
            [0.9, 45, 20, 22, 25],
            [1.3, 12, 45, 35, 12],
            [3.2, 14, 50, 45, 17],
            [2.1, 24, 85, 48, 7],
            [2.5, 230, 30, 80, 20],
            [3.8, 38, 15, 90, 9],
        ],
    },
    "👩‍💼 Recrutement d'un candidat": {
        "description": "Départager des candidats selon expérience, tests, entretien, salaire et disponibilité.",
        "alternatives": ["Amina", "Youssef", "Sara", "Karim", "Lina"],
        "criteres": ["Expérience (ans)", "Test technique (/20)", "Entretien (/20)",
                     "Prétention salariale (k€)", "Disponibilité (sem.)"],
        "types": ["max", "max", "max", "min", "min"],
        "data": [
            [5, 16, 14, 48, 4],
            [8, 14, 17, 60, 8],
            [3, 18, 15, 42, 2],
            [10, 13, 12, 72, 12],
            [6, 15, 18, 52, 6],
        ],
    },
    "📍 Localisation d'un entrepôt": {
        "description": "Choisir un site logistique selon loyer, accès, main-d'œuvre, risque et distance clients.",
        "alternatives": ["Casablanca", "Tanger", "Kénitra", "Marrakech", "Agadir"],
        "criteres": ["Loyer (€/m²)", "Accès autoroute/port (/10)", "Main-d'œuvre (/10)",
                     "Risque (/10)", "Distance clients (km)"],
        "types": ["min", "max", "max", "min", "min"],
        "data": [
            [6.5, 9.0, 9.0, 4, 120],
            [5.2, 9.5, 7.5, 3, 340],
            [4.1, 8.0, 7.0, 3, 180],
            [4.6, 6.5, 7.5, 5, 380],
            [3.8, 6.0, 6.0, 4, 510],
        ],
    },
}
EXEMPLE_DEFAUT = "💼 Choix d'un portefeuille d'investissement"


def charger_exemple(nom):
    """Charge un exemple dans l'état de session et réinitialise l'éditeur."""
    ex = EXEMPLES[nom]
    m = pd.DataFrame(ex["data"], index=ex["alternatives"], columns=ex["criteres"]).astype(float)
    m.index.name = "Alternative"
    definir_matrice(m, pd.Series(ex["types"], index=ex["criteres"], name="Type"), nom)


def definir_matrice(matrice, types, nom_source):
    """Remplace la matrice courante (exemple, import CSV...)."""
    st.session_state.matrice = matrice
    st.session_state.types = types
    st.session_state.base_matrice = matrice.copy()   # ce que voit l'éditeur
    st.session_state.base_types = types.copy()
    st.session_state.source = nom_source
    st.session_state.version = st.session_state.get("version", 0) + 1
    # Les anciens résultats ne correspondent plus à la nouvelle matrice
    for k in ("poids", "poids_source", "res_pond", "res_class"):
        st.session_state.pop(k, None)


def init_state():
    """Initialise la matrice au premier chargement (à appeler dans chaque page)."""
    if "matrice" not in st.session_state:
        charger_exemple(EXEMPLE_DEFAUT)


def afficher_df(obj, fmt="{:.4f}"):
    """Affiche un DataFrame/Series formaté, pleine largeur (compatible toutes versions)."""
    df = pd.DataFrame(obj)
    styled = df.style.format(fmt, subset=df.select_dtypes("number").columns)
    try:
        st.dataframe(styled, width="stretch")
    except TypeError:
        st.dataframe(styled, use_container_width=True)


def afficher_steps(res):
    """Affiche les étapes de calcul dans des blocs dépliables."""
    st.markdown("#### 🧮 Détail des calculs")
    for i, (titre, obj) in enumerate(res["steps"], 1):
        with st.expander(f"Étape {i} : {titre}", expanded=(i == len(res["steps"]))):
            if isinstance(obj, (pd.DataFrame, pd.Series)):
                afficher_df(obj)
            else:
                st.write(obj)
