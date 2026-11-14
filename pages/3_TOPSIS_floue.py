import streamlit as st
import pandas as pd

import ui
from methods import fuzzy_topsis, ECHELLE_ALTERNATIVES, ECHELLE_POIDS
from utils import init_state, afficher_steps, afficher_df

ui.setup("TOPSIS floue", "🌫️")
init_state()
ui.sidebar_info()

ui.page_title("🌫️ TOPSIS floue (Chen, 2000)",
              "Évaluations linguistiques de plusieurs décideurs, nombres flous triangulaires.")

# --- Exemple du cours (exercice : recrutement d'un ingénieur) -----------------
EX_CRIT = ["C1", "C2", "C3", "C4", "C5"]
EX_ALT = ["A1", "A2", "A3"]
EX_EVAL = {
    "A1": ["MG G F VG F", "G MG G G F", "MG F G VG F"],
    "A2": ["G VG VG VG VG", "G VG VG VG MG", "MG VG G VG G"],
    "A3": ["VG MG G G G", "G G MG VG G", "F VG VG MG MG"],
}
EX_POIDS = ["H VH VH VH M", "VH VH H VH MH", "MH VH H VH MH"]


def exemple(nb_dm):
    dms = [f"DM{k + 1}" for k in range(nb_dm)]
    rows = {(a, d): EX_EVAL[a][k].split() for a in EX_ALT for k, d in enumerate(dms)}
    ev = pd.DataFrame(list(rows.values()), index=pd.MultiIndex.from_tuples(rows, names=["Alternative", "Décideur"]),
                      columns=EX_CRIT)
    w = pd.DataFrame([EX_POIDS[k].split() for k in range(nb_dm)], index=pd.Index(dms, name="Décideur"),
                     columns=EX_CRIT)
    return ev, w


def vide(alts, dms, crits, defaut):
    idx = pd.MultiIndex.from_product([alts, dms], names=["Alternative", "Décideur"])
    return pd.DataFrame(defaut, index=idx, columns=crits)


# --- 1. Source -------------------------------------------------------------------
st.markdown("#### 1. Données")
source = st.radio("Structure du problème",
                  ["Exemple du cours (3 candidats, 5 critères, 3 décideurs)",
                   "Reprendre les alternatives et critères de la matrice active"],
                  horizontal=True)
v = st.session_state.version

if source.startswith("Exemple"):
    alts, crits = EX_ALT, EX_CRIT
    nb_dm = 3
    ev0, w0 = exemple(nb_dm)
    types = pd.Series(["max"] * len(crits), index=crits, name="Type")
    cle = f"ex_{v}"
else:
    alts = list(st.session_state.matrice.index)
    crits = list(st.session_state.matrice.columns)
    nb_dm = st.number_input("Nombre de décideurs", 1, 10, 3)
    dms = [f"DM{k + 1}" for k in range(nb_dm)]
    ev0 = vide(alts, dms, crits, "F")
    w0 = pd.DataFrame("M", index=pd.Index(dms, name="Décideur"), columns=crits)
    types = st.session_state.types.copy()
    cle = f"mat_{v}_{nb_dm}"

with st.expander("📖 Échelles linguistiques (Tableau 1)"):
    f = lambda t: "(" + ", ".join(f"{x:g}" for x in t) + ")"
    c1, c2 = st.columns(2)
    c1.dataframe(pd.DataFrame({"Nombre flou": {k: f(t) for k, t in ECHELLE_ALTERNATIVES.items()}}))
    c2.dataframe(pd.DataFrame({"Nombre flou": {k: f(t) for k, t in ECHELLE_POIDS.items()}}))

# --- 2. Évaluations des alternatives -------------------------------------------
st.markdown("#### 2. Évaluation des alternatives par chaque décideur")
st.caption("Étiquettes : " + ", ".join(ECHELLE_ALTERNATIVES))
cfg_alt = {c: st.column_config.SelectboxColumn(options=list(ECHELLE_ALTERNATIVES), required=True)
           for c in crits}
ev = st.data_editor(ev0.reset_index(), column_config=cfg_alt, key=f"fev_{cle}", hide_index=True,
                    disabled=["Alternative", "Décideur"])
ev = ev.set_index(["Alternative", "Décideur"])

# --- 3. Poids ----------------------------------------------------------------------
st.markdown("#### 3. Importance des critères par chaque décideur")
st.caption("Étiquettes : " + ", ".join(ECHELLE_POIDS))
cfg_w = {c: st.column_config.SelectboxColumn(options=list(ECHELLE_POIDS), required=True) for c in crits}
w = st.data_editor(w0.reset_index(), column_config=cfg_w, key=f"fw_{cle}", hide_index=True,
                   disabled=["Décideur"]).set_index("Décideur")

# --- 4. Types -------------------------------------------------------------------------
st.markdown("#### 4. Type de chaque critère")
t_edit = st.data_editor(types.to_frame().T, hide_index=True, key=f"ft_{cle}",
                        column_config={c: st.column_config.SelectboxColumn(options=["max", "min"], required=True)
                                       for c in crits})
types = t_edit.iloc[0].rename("Type")

st.write("")
if st.button("▶ Calculer le classement flou", type="primary"):
    try:
        if ev.isna().any().any() or w.isna().any().any():
            raise AssertionError("Certaines évaluations sont vides.")
        st.session_state.res_fuzzy = fuzzy_topsis(ev, w, types)
    except AssertionError as e:
        st.error(f"Erreur : {e}")

res = st.session_state.get("res_fuzzy")
if res:
    st.divider()
    classement = res["result"]
    st.markdown("### 📊 Résultat : classement")
    ui.winner(classement.index[0], "CC", classement["CC"].iloc[0])
    g, t = st.columns([2, 1])
    g.bar_chart(classement["CC"])
    with t:
        afficher_df(classement)
    afficher_steps(res)
