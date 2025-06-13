import streamlit as st

from pathlib import Path

def reset_session(message = "Annuler et reprendre au départ"):
    if st.button(message,type='secondary'):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.session_state["navigation"] = "1_st_choix_analyse.py"
        st.rerun()

def reach_st_donnee(message = "Importer vos données", type_button = 'primary'):
    if st.button(message, type=type_button):
        if "navigation" in st.session_state:
            st.session_state["previous_page"] = st.session_state["navigation"]
        st.session_state["navigation"] = "2_st_donnee.py"
        st.rerun()

def reach_st_show_donnee(message = "Montrer les données", type_button = 'primary'):
    if st.button(message, type=type_button):
        if "navigation" in st.session_state:
            st.session_state["previous_page"] = st.session_state["navigation"]
        st.session_state["navigation"] = "3_st_show_donnee.py"
        st.rerun()

def reach_st_comparaison(message = "Lancer la comparaison", type_button = 'primary'):
    if st.button(message, type=type_button):
        if "navigation" in st.session_state:
            st.session_state["previous_page"] = st.session_state["navigation"]
        st.session_state["navigation"] = "4_st_comparaison.py"
        st.rerun()

def reach_st_tutoriel(message = "Accéder au tutoriel", type_button = 'primary'):
    if st.button(message, type=type_button):
        if "navigation" in st.session_state:
            st.session_state["previous_page"] = st.session_state["navigation"]
        st.session_state["navigation"] = "0_tutorial.py"
        st.rerun()

# def comeback_to_previous_page(message = "Revenir à la page précédente", type_button = 'secondary'):
#     if st.button(message, type=type_button):
#         if "previous_page" in st.session_state:
#             current_page = st.session_state["navigation"]
#             st.session_state["navigation"] = st.session_state["previous_page"]
#             st.session_state["previous_page"] = current_page
#             st.rerun()

def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text(encoding="utf-8")