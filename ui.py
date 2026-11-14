"""Éléments d'interface partagés : style, en-têtes, cartes."""
import streamlit as st

CSS = """
<style>
.block-container {padding-top: 2rem; max-width: 1200px;}
h1, h2, h3 {letter-spacing: -0.01em;}

.hero {
  background: linear-gradient(120deg, #4F46E5 0%, #7C3AED 55%, #0EA5E9 100%);
  color: #fff; border-radius: 20px; padding: 2rem 2.2rem; margin-bottom: 1.4rem;
  box-shadow: 0 10px 30px rgba(79,70,229,.25);
}
.hero h1 {color:#fff; margin:0 0 .4rem 0; font-size: 2rem; padding:0;}
.hero p  {margin:0; opacity:.92; font-size: 1.02rem;}

.page-title {
  border-left: 6px solid #4F46E5; padding: .2rem 0 .2rem 1rem; margin-bottom: 1rem;
}
.page-title h1 {margin:0; font-size:1.8rem; padding:0;}
.page-title p {margin:.2rem 0 0 0; opacity:.75;}

.card {
  background: rgba(255,255,255,.75); border: 1px solid rgba(79,70,229,.15);
  border-radius: 16px; padding: 1rem 1.2rem; height: 100%;
  box-shadow: 0 2px 10px rgba(30,30,80,.05);
}
.card h4 {margin: 0 0 .3rem 0; color:#4F46E5;}
.card p {margin:0; font-size:.93rem; opacity:.85;}

.badge {
  display:inline-block; padding:.15rem .6rem; border-radius:999px; font-size:.75rem;
  font-weight:600; background:#E0E7FF; color:#3730A3; margin-right:.3rem;
}
.badge.obj {background:#DCFCE7; color:#166534;}
.badge.sub {background:#FEF3C7; color:#92400E;}

.winner {
  background: linear-gradient(120deg,#059669,#10B981); color:#fff; border-radius:16px;
  padding:1.1rem 1.4rem; margin: .6rem 0 1rem 0; box-shadow:0 8px 22px rgba(16,185,129,.25);
}
.winner .lbl {font-size:.8rem; text-transform:uppercase; letter-spacing:.08em; opacity:.85;}
.winner .nom {font-size:1.7rem; font-weight:700; line-height:1.2;}
.winner .sc  {opacity:.9;}

div[data-testid="stMetric"] {
  background: rgba(255,255,255,.75); border:1px solid rgba(79,70,229,.15);
  border-radius:14px; padding:.7rem 1rem;
}
.stButton>button[kind="primary"] {
  border-radius: 12px; font-weight:600; padding:.55rem 1.6rem;
}
section[data-testid="stSidebar"] {border-right: 1px solid rgba(79,70,229,.15);}
</style>
"""


def setup(titre_onglet, icone="🎯"):
    st.set_page_config(page_title=titre_onglet, page_icon=icone, layout="wide")
    st.markdown(CSS, unsafe_allow_html=True)


def sidebar_info():
    """Résumé de la matrice courante dans la barre latérale."""
    m = st.session_state.matrice
    with st.sidebar:
        st.markdown("### 🎯 Aide à la décision")
        st.caption(f"Matrice active : **{st.session_state.get('source', '—')}**")
        c1, c2 = st.columns(2)
        c1.metric("Alternatives", m.shape[0])
        c2.metric("Critères", m.shape[1])
        st.divider()


def hero(titre, texte):
    st.markdown(f'<div class="hero"><h1>{titre}</h1><p>{texte}</p></div>', unsafe_allow_html=True)


def page_title(titre, texte=""):
    st.markdown(f'<div class="page-title"><h1>{titre}</h1><p>{texte}</p></div>',
                unsafe_allow_html=True)


def card(titre, texte):
    st.markdown(f'<div class="card"><h4>{titre}</h4><p>{texte}</p></div>', unsafe_allow_html=True)


def winner(nom, libelle_score, valeur):
    st.markdown(
        f'<div class="winner"><div class="lbl">🏆 Meilleure alternative</div>'
        f'<div class="nom">{nom}</div><div class="sc">{libelle_score} = {valeur:.4f}</div></div>',
        unsafe_allow_html=True)


def badge(texte, kind=""):
    return f'<span class="badge {kind}">{texte}</span>'


def lien_page(chemin, label, icon=None):
    """Lien vers une page ; ignoré silencieusement si la page est introuvable."""
    try:
        st.page_link(chemin, label=label, icon=icon)
    except Exception:
        pass
