import pandas as pd

import streamlit as st
import pathlib

from os import path
from fonction import get_hal_researcher_data, Orcid_Researcher, Scopus_Researcher
from utilitaire import reset_session, reach_st_donnee, reach_st_show_donnee

st.title("Récupération des données")

with st.expander("Guide d'utilisation", expanded=False):
    st.markdown("""
    ### 📝 Comment remplir cette page ?

    Vous avez deux options pour charger vos données :

    #### Option 1 : Utiliser les exemples
    - Cochez simplement la case "Utiliser les exemples fournis"
    - Les données de démonstration seront automatiquement chargées

    #### Option 2 : Entrer vos propres données
    1. **Informations personnelles** :
        - Saisissez votre prénom et nom
        - Ces informations permettent de chercher les publications dans HAL

    2. **Identifiants de recherche** :
        - **ORCID** : Collez l'URL complète de votre profil ORCID
        - **Scopus ID** : Entrez votre identifiant Scopus

    3. **Données Web of Science** :
        - Téléversez vos fichiers d'export Web of Science (formats acceptés : Excel, CSV)
        - Veuillez vous référer à la page "Tutoriel d'utilisation" pour savoir comment récupérer ces fichiers.

    4. **Lancement de la recherche** :
        - Cliquez sur le bouton "Lancer la recherche", un indicateur de progression vous informera de l'avancement.

    #### 🔍 Visualisation des résultats
    - Utilisez le bouton "Montrer les données" pour voir vos publications
    - Le bouton "Reset" permet de recommencer à zéro si nécessaire
    """)

# Téléversement des fichiers
st.header("1. Rentrer les informations suivantes")
databases = {}

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
    # Interface pour entrer les informations du chercheur et charger les bases de données.
    last_name_col, first_name_col = st.columns(2)

    with first_name_col:
        researcher_first_name = st.text_input("Prénom du chercheur :")
    with last_name_col:
        researcher_last_name = st.text_input("Nom du chercheur :")

    orcid_col, scopus_col = st.columns(2)
    
    with orcid_col:
        orcid_researcher = st.text_input("Veuillez saisir l'URL vers le profil ORCID du chercheur :", help="Veuillez saisir le lien URL complet.")


    with scopus_col:
        scopus_id = st.text_input("Entrer le Socpus ID du chercheur :", help="Exemple : '01234567891'.")

    # Téléversement des fichiers Web Of Science.
    uploaded_files = st.file_uploader(
        "Téléverser les fichiers Web Of Science", 
        accept_multiple_files=True,
        type=["xlsx", "xls", "csv"]
    )

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
            databases["WoS"] = df

    empty = st.empty()

    if empty.button("Lancer la récupération de données", type='primary'):
        if not scopus_id or not researcher_last_name or not researcher_first_name or not orcid_researcher:
            pass
        
        else:
            with st.spinner(""):
                bar_perc = 0
                progress_bar = empty.progress(bar_perc, text="Recherche des données orcid en cours...")
                orcid_df = Orcid_Researcher(orcid_link=orcid_researcher).format_df_orcids()
                
                bar_perc += 1
                progress_bar.progress(bar_perc / 3, text="Recherche des données HAL en cours...") 
                hal_df = get_hal_researcher_data(researcher_last_name, researcher_first_name)
                
                bar_perc += 1
                progress_bar.progress(bar_perc/ 3, text="Recherche des données Scopus en cours...") 
                if len(scopus_id) >= 10:
                    scopus_df = Scopus_Researcher(scopus_id=scopus_id).get_publication_scopus()
                else:
                    st.error("Le Scopus ID doit contenir au moins 10 chiffres.")
                bar_perc += 1
                progress_bar.progress(bar_perc / 3,text="Recherche des données en cours...") 
        try:
            databases["HAL"] = hal_df
            databases["Scopus"] = scopus_df
            databases["Orcid"] = orcid_df
            st.success("Données chargées avec succès.")
            st.session_state["databases"] = databases
        except NameError as e:
            pass
        empty.empty()


st.divider()

reset, comparaison = st.columns(2)
with comparaison:
    reach_st_show_donnee(message = "Montrer les données", type_button = 'primary')
with reset:
    reset_session()
