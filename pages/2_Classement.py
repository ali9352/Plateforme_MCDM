import streamlit as st
import pandas as pd

import ui
from methods import waspas, topsis
from utils import init_state, afficher_steps, afficher_df

ui.setup("Classement", "🏆")
init_state()
ui.sidebar_info()

matrice = st.session_state.matrice
types = st.session_state.types
criteres = list(matrice.columns)
v = st.session_state.version

ui.page_title("🏆 Classement des alternatives",
              "Ordonnez les alternatives à partir des poids des critères.")

methode = st.sidebar.radio("Méthode de classement", ["WASPAS", "TOPSIS"],
                           captions=["Somme + produit pondérés", "Distance à l'idéal"])
st.markdown(f"### {methode}")

# --- 1. Poids ---------------------------------------------------------------
st.markdown("#### 1. Poids des critères")
poids_memo = st.session_state.get("poids")
memo_ok = poids_memo is not None and list(poids_memo.index) == criteres

options = ["Saisie manuelle"]
if memo_ok:
    options.insert(0, f"Derniers poids calculés ({st.session_state.poids_source})")
origine = st.radio("Origine des poids", options, horizontal=True)

if origine == "Saisie manuelle":
    st.caption("Valeurs positives : elles sont normalisées automatiquement (somme = 1).")
    brut = st.data_editor(pd.DataFrame({"Poids": [1.0] * len(criteres)}, index=criteres),
                          key=f"poids_manuels_{v}")["Poids"]
    if (brut <= 0).any() or brut.isna().any():
        st.error("Tous les poids doivent être strictement positifs.")
        st.stop()
    poids = (brut / brut.sum()).rename("Poids")
else:
    poids = poids_memo.rename("Poids")

st.bar_chart(poids, height=200)

# --- 2. Paramètres ------------------------------------------------------------
lam = 0.5
if methode == "WASPAS":
    st.markdown("#### 2. Paramètre λ")
    lam = st.slider("λ (0 = produit pondéré pur, 1 = somme pondérée pure)", 0.0, 1.0, 0.5, 0.05)

st.write("")
if st.button("▶ Calculer le classement", type="primary"):
    try:
        res = waspas(matrice, types, poids, lam) if methode == "WASPAS" else topsis(matrice, types, poids)
        st.session_state.res_class = {"methode": methode, "res": res}
    except AssertionError as e:
        st.error(f"Erreur : {e}")

stocke = st.session_state.get("res_class")
if stocke and stocke["methode"] == methode:
    st.divider()
    classement = stocke["res"]["result"]
    score = "Q" if methode == "WASPAS" else "C"
    st.markdown("### 📊 Résultat : classement")
    ui.winner(classement.index[0], score, classement[score].iloc[0])

    g, t = st.columns([2, 1])
    g.bar_chart(classement[score])
    with t:
        afficher_df(classement, fmt="{:.4f}")
    afficher_steps(stocke["res"])
