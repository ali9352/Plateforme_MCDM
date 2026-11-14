import streamlit as st
import pandas as pd

import ui
from methods import entropie, critic, ahp, bwm, construire_matrice_ahp
from utils import init_state, afficher_steps, afficher_df

ui.setup("Pondération", "⚖️")
init_state()
ui.sidebar_info()

matrice = st.session_state.matrice
types = st.session_state.types
criteres = list(matrice.columns)
v = st.session_state.version

ui.page_title("⚖️ Pondération des critères",
              "Déterminez l'importance relative de chaque critère.")

DESCR = {
    "Entropie": ("Objective", "obj", "Poids issus de la dispersion des valeurs."),
    "CRITIC": ("Objective", "obj", "Poids issus du contraste et des corrélations."),
    "AHP": ("Subjective", "sub", "Comparaisons par paires (échelle de Saaty)."),
    "BWM": ("Subjective", "sub", "Comparaisons du meilleur et du pire critère."),
}
methode = st.sidebar.radio("Méthode de pondération", list(DESCR),
                           captions=[d[0] for d in DESCR.values()])
type_m, cls, expl = DESCR[methode]
st.markdown(f"### {methode} &nbsp; {ui.badge(type_m, cls)}", unsafe_allow_html=True)
st.caption(expl)

A = None
if methode in ("Entropie", "CRITIC"):
    st.info("Aucun paramètre à saisir : les poids sont calculés à partir de la matrice.")
    with st.expander("Voir la matrice de décision", expanded=True):
        st.dataframe(matrice)

elif methode == "AHP":
    if len(criteres) > 10:
        st.error("AHP est limité à 10 critères (table de l'indice aléatoire).")
        st.stop()
    st.caption("Pour chaque paire, indiquez l'importance du 1er critère par rapport au 2e "
               "(échelle de Saaty). **3** = le 1er est modérément plus important ; "
               "**1/3** = c'est le 2e qui l'est.")
    options = [1 / k for k in range(9, 1, -1)] + [float(k) for k in range(1, 10)]
    fmt = lambda x: str(int(x)) if x >= 1 else f"1/{round(1 / x)}"
    comparaisons = {}
    colonnes = st.columns(2)
    k = 0
    for i in range(len(criteres)):
        for j in range(i + 1, len(criteres)):
            with colonnes[k % 2]:
                comparaisons[(criteres[i], criteres[j])] = st.select_slider(
                    f"{criteres[i]}  vs  {criteres[j]}", options=options, value=1.0,
                    format_func=fmt, key=f"ahp_{v}_{i}_{j}")
            k += 1
    A = construire_matrice_ahp(criteres, comparaisons)

elif methode == "BWM":
    st.caption("Choisissez le meilleur et le pire critère, puis comparez-les aux autres "
               "(échelle de 1 à 9).")
    c1, c2 = st.columns(2)
    best = c1.selectbox("Meilleur critère", criteres, index=0, key=f"best_{v}")
    worst = c2.selectbox("Pire critère", criteres, index=len(criteres) - 1, key=f"worst_{v}")
    if best == worst:
        st.error("Le meilleur et le pire critère doivent être différents.")
        st.stop()
    a_BW = st.slider(f"{best} (meilleur) vs {worst} (pire)", 2, 9, 5, key=f"bw_{v}_{best}_{worst}")
    best_to_others = {best: 1, worst: a_BW}
    others_to_worst = {worst: 1, best: a_BW}
    col_b, col_w = st.columns(2)
    for c in [c for c in criteres if c not in (best, worst)]:
        best_to_others[c] = col_b.slider(f"« {best} » est … plus important que « {c} »",
                                         1, 9, 2, key=f"bo_{v}_{best}_{worst}_{c}")
        others_to_worst[c] = col_w.slider(f"« {c} » est … plus important que « {worst} »",
                                          1, 9, 2, key=f"ow_{v}_{best}_{worst}_{c}")

st.write("")
if st.button("▶ Calculer les poids", type="primary"):
    try:
        if methode == "Entropie":
            res = entropie(matrice, types)
        elif methode == "CRITIC":
            res = critic(matrice, types)
        elif methode == "AHP":
            res = ahp(A)
        else:
            res = bwm(criteres, best, worst, best_to_others, others_to_worst)
        st.session_state.res_pond = {"methode": methode, "res": res}
        st.session_state.poids = res["result"]
        st.session_state.poids_source = methode
    except AssertionError as e:
        st.error(f"Erreur : {e}")

stocke = st.session_state.get("res_pond")
if stocke and stocke["methode"] == methode:
    st.divider()
    w = stocke["res"]["result"]
    st.markdown("### 📊 Résultat : poids des critères")
    top = w.idxmax()
    m1, m2, m3 = st.columns(3)
    m1.metric("Critère dominant", top)
    m2.metric("Poids max", f"{w.max():.1%}")
    m3.metric("Poids min", f"{w.min():.1%}")
    g, t = st.columns([2, 1])
    g.bar_chart(w)
    with t:
        afficher_df(w.to_frame())
    st.success(f"Poids ({methode}) enregistrés : ils seront proposés dans la page Classement.")
    ui.lien_page("pages/2_Classement.py", label="Passer au classement", icon="🏆")
    afficher_steps(stocke["res"])
