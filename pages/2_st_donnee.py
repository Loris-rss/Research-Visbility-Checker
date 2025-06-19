import pandas as pd

import streamlit as st
import pathlib

from os import path
from fonction import get_hal_researcher_data, Orcid_Researcher, Scopus_Researcher
from utilitaire import reset_session, reach_st_donnee, reach_st_show_donnee, read_markdown_file

st.title("Récupération des données")

with st.expander("Guide d'utilisation pour la récupération des données.", expanded=False):
    st.markdown(read_markdown_file(r"md\guide_utilisation_donnees.md"), unsafe_allow_html=True)

# Téléversement des fichiers
st.header("1. Rentrer les informations suivantes")
databases = {}

check_list = []

# Option pour charger des exemples
use_examples = st.checkbox("Utiliser les exemples fournis", value=False,)

# Chargement des exemples.
if use_examples:
    try:
        # Charger les exemples depuis le dossier ressources
        hal_df = pd.read_excel(path.relpath("ressources\hal_humbert.xlsx"))
        scopus_df = pd.read_excel(path.relpath("ressources\scopus_mh.xlsx"))
        orcid_df = pd.read_excel(path.relpath("ressources\orcid_publication.xlsx"))
        wos_df = pd.read_excel(path.relpath("ressources\Marc Humbert WoS.xlsx"))
        
        databases["HAL"] = hal_df
        databases["Scopus"] = scopus_df
        databases["Orcid"] = orcid_df
        databases["WoS"] = wos_df
  
        st.success(f"Exemples chargés avec succès: HAL ({len(hal_df)} publications), Scopus ({len(scopus_df)} publications), Orcid ({len(orcid_df)} publications)")
        st.session_state["databases"] = databases

    except Exception as e:
        st.error(f"Erreur lors du chargement des exemples: {str(e)}")

else:
    if "show_hal_fields" not in st.session_state:
        st.session_state.show_hal_fields = False
        st.session_state["primary_button"] = "primary"
    if "show_scopus_fields" not in st.session_state:
        st.session_state.show_scopus_fields = False
    if "show_orcid_fields" not in st.session_state:
        st.session_state.show_orcid_fields = False
    if "show_wos_fields" not in st.session_state:
        st.session_state.show_wos_fields = False

    # Créer une ligne de boutons côte à côte
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button(
            "HAL", 
            type="primary" if st.session_state.show_hal_fields == False else "secondary",
            help="Récupérer les données HAL"
        ):
            st.session_state.show_hal_fields = not st.session_state.show_hal_fields
            st.rerun()

    with col2:
        if st.button(
            "ORCID", 
            type="primary" if not st.session_state.show_orcid_fields else "secondary",
            help="Récupérer les données ORCID"
        ):
            st.session_state.show_orcid_fields = not st.session_state.show_orcid_fields
            st.rerun()

    with col3:
        if st.button(
            "Scopus", 
            type="primary" if not st.session_state.show_scopus_fields else "secondary",
            help="Récupérer les données Scopus"
            ):
            st.session_state.show_scopus_fields = not st.session_state.show_scopus_fields
            st.rerun()

    with col4:
        if st.button(
            "WoS", 
            type="primary" if not st.session_state.show_wos_fields else "secondary",
            help="Récupérer les données WoS"
        ):
            st.session_state.show_wos_fields = not st.session_state.show_wos_fields
            st.rerun()

    # Afficher les champs HAL si nécessaire
    if st.session_state.show_hal_fields:
        st.session_state.primary_button = "secondary"
        last_name_col, first_name_col = st.columns(2)
        with first_name_col:
            researcher_first_name = st.text_input("Prénom du chercheur :")
        with last_name_col:
            researcher_last_name = st.text_input("Nom du chercheur :")
        check_list.append((researcher_first_name,researcher_last_name))

    # Afficher les champs ORCID si nécessaire
    if st.session_state.show_orcid_fields:
        orcid_researcher = st.text_input("Veuillez saisir l'URL vers le profil ORCID du chercheur :", 
                                    help="Veuillez saisir le lien URL complet.")
        check_list.append(orcid_researcher)

    # Afficher les champs Scopus si nécessaire
    if st.session_state.show_scopus_fields:
        scopus_id = st.text_input("Entrer le Socpus ID du chercheur :", 
                                help="Exemple : '01234567891'.")
        check_list.append(scopus_id)
    
    if st.session_state.show_wos_fields:
        # Téléversement des fichiers Web Of Science
        uploaded_files = st.file_uploader(
            "Téléverser les fichiers Web Of Science", 
            accept_multiple_files=True,
            type=["xlsx", "xls", "csv"]
        )
        check_list.append(uploaded_files)
        if uploaded_files:
            for file in uploaded_files:
                # Déterminer le nom de la base de données à partir du nom du fichier
                db_name = file.name.split(".")[0].capitalize()
                
                st.markdown(f"#### Fichier: {file.name}")

                # Lecture du fichier selon son type
                if file.name.endswith('.csv'):
                    df = pd.read_csv(file)
                else:
                    df = pd.read_excel(file)
                
                # Ajouter à la liste des bases de données
                databases[db_name] = df
    st.write(len(databases))
    empty = st.empty()

    if empty.button("Lancer la récupération de données", type='primary'):
        if len(check_list) < 2:
            pass
        
        else:
            with st.spinner(""):
                bar_perc = 0
                progress_bar = empty.progress(bar_perc, text="Recherche des données orcid en cours...")
                if orcid_researcher:
                    orcid_df = Orcid_Researcher(orcid_link=orcid_researcher).format_df_orcids()
                else:
                    st.write("pas de données orcid")
                    pass
                
                bar_perc += 1
                progress_bar.progress(bar_perc / 3, text="Recherche des données HAL en cours...") 
                hal_df = get_hal_researcher_data(researcher_last_name, researcher_first_name)
                

                bar_perc += 1
                progress_bar.progress(bar_perc/ 3, text="Recherche des données Scopus en cours...") 
                
                if st.session_state["show_scopus_fields"]:
                    if len(scopus_id) >= 10:
                        scopus_df = Scopus_Researcher(scopus_id=scopus_id).get_publication_scopus()
                    else:
                        st.error("Le Scopus ID doit contenir au moins 10 chiffres.")
                else:
                    # st.write("pas de données scopus")
                    pass
                bar_perc += 1
                progress_bar.progress(bar_perc / 3,text="Recherche des données en cours...") 
        try:
            databases["HAL"] = hal_df
            databases["Scopus"] = scopus_df
            databases["Orcid"] = orcid_df
            st.success("Données chargées avec succès.")
        except NameError as e:
            pass
        empty.empty()

st.session_state["databases"] = databases

st.divider()
st.write(len(databases))
st.write(st.session_state["databases"])

reset, comparaison = st.columns(2)
with comparaison:
    reach_st_show_donnee(message = "Montrer les données", type_button = 'primary')
with reset:
    reset_session()