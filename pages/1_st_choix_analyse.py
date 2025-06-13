import streamlit as st
import pathlib
from utilitaire import reset_session, reach_st_donnee, reach_st_tutoriel

st.title("Choix de l'analyse")

comparison_mode = st.radio(
    "Mode de comparaison",
    ["Comparer deux bases de données", "Comparer toutes les bases de données entre elles"]
)

if "comparison_mode" not in st.session_state:
    st.session_state["comparison_mode"] = comparison_mode
    st.rerun()


st.divider()

reset, tutoriel, reach_donnee = st.columns(3)

with reset:
    reset_session()

with reach_donnee:
    if st.session_state["comparison_mode"] == comparison_mode:
        reach_st_donnee()
    else:
        st.session_state["comparison_mode"] = comparison_mode
        reach_st_donnee()
