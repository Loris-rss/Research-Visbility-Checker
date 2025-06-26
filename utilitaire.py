import streamlit as st

import io

from pathlib import Path

def reset_session(message = "Annuler et reprendre au départ"):
    """
    Bouton pour annuler et reprendre au départ.

    Args:
        message (str): Le message à afficher sur le bouton.
        type_button (str): Le type de bouton à afficher.

    Return:
        None : Affiche le bouton et redirige vers la page de sélection des données
    """
    if st.button(message,type='secondary'):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.session_state["navigation"] = "1_st_choix_analyse.py"
        st.rerun()

def reach_st_donnee(message = "Importer vos données", type_button = 'primary'):
    """
    Bouton pour atteindre la page de sélection des données.

    Args:
        message (str): Le message à afficher sur le bouton.
        type_button (str): Le type de bouton à afficher.

    Return:
        None : Affiche le bouton et redirige vers la page de sélection des données
    """
    if st.button(message, type=type_button):
        if "navigation" in st.session_state:
            st.session_state["previous_page"] = st.session_state["navigation"]
        st.session_state["navigation"] = "2_st_donnee.py"
        st.rerun()

def reach_st_show_donnee(message = "Montrer les données", type_button = 'primary'):
    """
    Bouton pour atteindre la page de visualisation des données.

    Args:
        message (str): Le message à afficher sur le bouton.
        type_button (str): Le type de bouton à afficher.

    Return:
        None : Affiche le bouton et redirige vers la page de visualisation des données
    """
    if st.button(message, type=type_button):
        if "navigation" in st.session_state:
            st.session_state["previous_page"] = st.session_state["navigation"]
        st.session_state["navigation"] = "3_st_show_donnee.py"
        st.rerun()

def reach_st_comparaison(message = "Lancer la comparaison", type_button = 'primary'):
    """
    Bouton pour atteindre la page de comparaison des données.

    Args:
        message (str): Le message à afficher sur le bouton.
        type_button (str): Le type de bouton à afficher.

    Return:
        None : Affiche le bouton et redirige vers la page de comparaison des données
    """
    if st.button(message, type=type_button):
        if "navigation" in st.session_state:
            st.session_state["previous_page"] = st.session_state["navigation"]
        st.session_state["navigation"] = "4_st_comparaison.py"
        st.rerun()

def reach_st_tutoriel(message = "Accéder au tutoriel", type_button = 'primary'):
    """
    Bouton pour atteindre la page de tutoriel.

    Args:
        message (str): Le message à afficher sur le bouton.
        type_button (str): Le type de bouton à afficher.

    Return:
        None : Affiche le bouton et redirige vers la page de tutoriel
    """
    if st.button(message, type=type_button):
        if "navigation" in st.session_state:
            st.session_state["previous_page"] = st.session_state["navigation"]
        st.session_state["navigation"] = "0_tutorial.py"
        st.rerun()

# Pas utilisé pour l'instant
# def comeback_to_previous_page(message = "Revenir à la page précédente", type_button = 'secondary'):
#     if st.button(message, type=type_button):
#         if "previous_page" in st.session_state:
#             current_page = st.session_state["navigation"]
#             st.session_state["navigation"] = st.session_state["previous_page"]
#             st.session_state["previous_page"] = current_page
#             st.rerun()

def read_markdown_file(markdown_file):
    """
    Permet la lecture d'un fichier markdown.

    Args:
        markdown_file (str): Le chemin du fichier markdown à lire.

    Return:
        str : Le contenu du fichier markdown
    """
    return Path(markdown_file).read_text(encoding="utf-8")

def download_plot():
    """
    Télécharge un graphique matplotlib depuis l'interface Streamlit.

    Return:
        None : Affiche les widgets de sélection et le bouton de téléchargement
    """
    selecton_plot = st.selectbox("Choisissez la base de données", options=st.session_state["plot_pie_chart"].keys())

    formats = ["png", "jpeg", "svg", "pdf"]

    selected_format = st.selectbox(
        "Choisissez le format de téléchargement :",
        formats,
        index=0,
    )

    fig = st.session_state["plot_pie_chart"][selecton_plot]

    # Convert the figure to PNG in-memory
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)

    st.download_button(
        label="Télécharger le graphique",
        data=buf,
        file_name=f"{selecton_plot}.{selected_format}",
        mime=f"image/{selected_format}"
    )