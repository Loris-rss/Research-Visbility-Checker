import streamlit as st
from os import path
import pathlib
from utilitaire import reach_st_tutoriel

st.set_page_config("Research Visibility Checker", layout="wide")

st.markdown("""
# Bienvenue sur Research Visibility Checker !""")

with st.expander("Présentation de l'application", expanded=False):
    st.markdown("""
    Cette application est votre assistant personnel pour analyser et optimiser votre visibilité académique. Elle vous permet de comparer 
    vos publications à travers les principales bases de données scientifiques :
    - HAL
    - ORCID 
    - Scopus 
    - Web Of Science 

    ### Objectif
    Identifier rapidement les recoupements entre ces différentes bases de données et s'assurer que toutes vos publications 
    sont correctement référencées partout.

    ### 📝 Comment utiliser l'application ?
        1. Entrez les informations du chercheur (nom, prénom, identifiants ORCID et Scopus)
        2. Ajoutez des fichiers supplémentaires si nécessaire (Web of Science, etc.)
        3. Les données sont automatiquement récupérées depuis HAL, ORCID et Scopus
        4. Lancez l'analyse pour visualiser les recoupements
    """)

st.divider()

def main():
    if "navigation" not in st.session_state:
        st.navigation([st.Page(path.relpath("pages/1_st_choix_analyse.py"),title='Research Visibility Checker'), st.Page(path.relpath("pages/0_tutorial.py"),title='Tutoriel')]).run()
    else: 
        st.navigation([st.Page(path.relpath(f"pages/{st.session_state["navigation"]}"), title="Research Visibility Checker"), st.Page(path.relpath("pages/0_tutorial.py"),title='Tutoriel')]).run()

if __name__ == "__main__":
    main()