import io
import pandas as pd
import streamlit as st

import ui
from methods import valider_matrice
from utils import (EXEMPLES, EXEMPLE_DEFAUT, init_state, charger_exemple,
                   definir_matrice)

ui.setup("Aide à la décision multicritère", "🎯")
init_state()
ui.sidebar_info()

ui.hero("Aide à la décision multicritère",
        "Saisissez une matrice de décision, calculez les <b>poids des critères</b> "
        "(Entropie, CRITIC, AHP, BWM) puis <b>classez les alternatives</b> (WASPAS, TOPSIS, TOPSIS floue).")

# --- Parcours en 3 cartes -------------------------------------------------
c1, c2, c3 = st.columns(3)
with c1:
    ui.card("1 · Matrice", "Choisissez un exemple, importez un CSV ou saisissez vos données.")
with c2:
    ui.card("2 · Pondération", "Calculez les poids par des méthodes objectives ou subjectives.")
with c3:
    ui.card("3 · Classement", "Classez les alternatives avec WASPAS, TOPSIS ou TOPSIS floue.")

st.write("")

# --- 1. Source de la matrice ---------------------------------------------
st.subheader("1. Source des données")
tab_ex, tab_csv = st.tabs(["📚 Exemples", "📁 Importer un CSV"])

with tab_ex:
    noms = list(EXEMPLES)
    choix = st.selectbox("Exemple de matrice", noms, index=noms.index(EXEMPLE_DEFAUT))
    ex = EXEMPLES[choix]
    st.caption(f"{ex['description']}  —  {len(ex['alternatives'])} alternatives × "
               f"{len(ex['criteres'])} critères")
    if st.button("Charger cet exemple", type="primary"):
        charger_exemple(choix)
        st.rerun()

with tab_csv:
    st.caption("Première colonne : noms des alternatives. Autres colonnes : critères "
               "(valeurs numériques > 0). Les types (max/min) se règlent ensuite.")
    fichier = st.file_uploader("Fichier CSV", type=["csv"])
    if fichier is not None and st.button("Utiliser ce fichier"):
        try:
            brut = fichier.getvalue().decode("utf-8-sig")
            sep = ";" if brut.splitlines()[0].count(";") > brut.splitlines()[0].count(",") else ","
            d = pd.read_csv(io.StringIO(brut), sep=sep, index_col=0)
            d.index = d.index.astype(str)
            d.index.name = "Alternative"
            d = d.astype(float)
            t = pd.Series(["max"] * d.shape[1], index=d.columns, name="Type")
            valider_matrice(d, t)
            definir_matrice(d, t, f"CSV : {fichier.name}")
            st.rerun()
        except Exception as e:
            st.error(f"Import impossible : {e}")

st.divider()

# --- 2. Édition de la matrice --------------------------------------------
st.subheader("2. Matrice de décision")
st.caption("Modifiez les valeurs, renommez les alternatives, ajoutez-en (ligne vide en bas) "
           "ou supprimez-en.")

v = st.session_state.version
base = st.session_state.base_matrice.reset_index()
edite = st.data_editor(base, num_rows="dynamic", hide_index=True,
                       key=f"editeur_{v}")

st.subheader("3. Type de chaque critère")
st.caption("**max** : plus grand = mieux (bénéfice)   |   **min** : plus petit = mieux (coût)")
types_df = st.session_state.base_types.to_frame().T
types_edite = st.data_editor(
    types_df, hide_index=True, key=f"types_{v}",
    column_config={c: st.column_config.SelectboxColumn(options=["max", "min"], required=True)
                   for c in types_df.columns},
)

# --- Validation et enregistrement ----------------------------------------
try:
    edite = edite.dropna(subset=["Alternative"])
    if edite["Alternative"].duplicated().any():
        raise AssertionError("Les noms d'alternatives doivent être uniques.")
    if edite.isna().any().any():
        raise AssertionError("Certaines cases sont vides.")
    nouvelle = edite.set_index("Alternative")
    nouveaux_types = types_edite.iloc[0].rename("Type")
    valider_matrice(nouvelle, nouveaux_types)

    st.session_state.matrice = nouvelle
    st.session_state.types = nouveaux_types
    st.success(f"✅ Matrice valide : {nouvelle.shape[0]} alternatives × "
               f"{nouvelle.shape[1]} critères. Prête pour les autres pages.")
    n1, n2 = st.columns(2)
    ui.lien_page("pages/1_Ponderation.py", label="Calculer les poids", icon="⚖️")
    ui.lien_page("pages/2_Classement.py", label="Classer les alternatives", icon="🏆")
    st.download_button("⬇️ Télécharger la matrice (CSV)",
                       nouvelle.to_csv().encode("utf-8-sig"), "matrice_decision.csv", "text/csv")
except AssertionError as e:
    st.error(f"Matrice non valide : {e}")
