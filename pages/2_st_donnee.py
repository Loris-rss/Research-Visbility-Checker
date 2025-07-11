import pandas as pd
import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from os import path
from fonction import get_hal_researcher_data, Orcid_Researcher, Scopus_Researcher
from utilitaire import reset_session, reach_st_show_donnee, read_markdown_file

st.title("Récupération des données")

with st.expander("Guide d'utilisation pour la récupération des données.", expanded=False):
    st.markdown(read_markdown_file(r"md/guide_utilisation_donnees.md"), unsafe_allow_html=True)

# Téléversement des fichiers
st.header("1. Rentrer les informations suivantes")

databases = {}

check_list = []

# Option pour charger des exemples
if st.checkbox("Utiliser les exemples fournis", value=False):
    try:
        # Charger les exemples depuis le dossier ressources
        hal_df = pd.read_excel(path.relpath("ressources/hal_humbert.xlsx"))
        scopus_df = pd.read_excel(path.relpath("ressources/scopus_mh.xlsx"))
        orcid_df = pd.read_excel(path.relpath("ressources/orcid_publication.xlsx"))
        wos_df = pd.read_excel(path.relpath("ressources/Marc Humbert WoS.xlsx"))
        
        databases["HAL"] = hal_df
        databases["Scopus"] = scopus_df
        databases["Orcid"] = orcid_df
        databases["WoS"] = wos_df

        st.success(f"Exemples chargés avec succès: HAL ({len(hal_df)} publications), Scopus ({len(scopus_df)} publications), Orcid ({len(orcid_df)} publications)")
        st.session_state["databases"] = databases

    except Exception as e:
        st.error(f"Erreur lors du chargement des exemples: {str(e)}")

else:
    with st.expander("Récupérer les données HAL :", expanded=False):
        search_by = st.radio(label = "Recherche HAL par : ", options=["Nom et prénom", "ID HAL"])
        
        st.session_state["search_by"] = search_by

        if search_by == "Nom et prénom":
            last_name_col, first_name_col = st.columns(2)
            with first_name_col:
                researcher_first_name = st.text_input("Prénom du chercheur :")
                
                if researcher_first_name:
                    st.session_state["researcher_first_name"] = researcher_first_name
                    st.success(f"Prénom du chercheur : {researcher_first_name}")
                else:
                    pass
            
            with last_name_col:
                researcher_last_name = st.text_input("Nom du chercheur :")
                if researcher_last_name:
                    st.session_state["researcher_last_name"] = researcher_last_name
                    st.success(f"Nom du chercheur : {researcher_last_name}")
                else:
                    pass
            
            if researcher_first_name and researcher_last_name:
                check_list.append((researcher_first_name,researcher_last_name))
                        
        elif st.session_state["search_by"] == "ID HAL":
            id_hal = st.text_input("ID HAL du chercheur :")
            if id_hal:
                st.session_state["id_hal"] = id_hal
                st.success(f"ID HAL du chercheur : {id_hal}")
                check_list.append(id_hal)
            else:
                pass
        
    with st.expander("Récupérer les données Orcid :", expanded=False):
        orcid_researcher = st.text_input("Veuillez saisir l'URL vers le profil ORCID du chercheur :", 
                                    help="Veuillez saisir le lien URL complet.")
        if orcid_researcher:
            st.session_state["orcid_researcher"] = orcid_researcher
            st.success(f"ORCID du chercheur : {orcid_researcher}")
            check_list.append(orcid_researcher)
        else:
            pass
    
    if os.getenv("SCOPUS_API_KEY") != "YOUR_SCOPUS_API_KEY": # API Key Available
        # Créer une ligne de boutons côte à côte
        
        with st.expander("Récupérer les données Scopus :", expanded=False):
            scopus_id = st.text_input("Entrer le Socpus ID du chercheur :", 
                                    help="Exemple : '01234567891'.")
            if scopus_id:
                st.session_state["scopus_id"] = scopus_id
                st.success(f"Scopus ID du chercheur : {scopus_id}")
                check_list.append(scopus_id)
            else:
                pass

        with st.expander("Récupérer les données WoS :", expanded=False):
            # Téléversement des fichiers Web Of Science
            uploaded_files = st.file_uploader(
                f"Téléverser les fichiers Web Of Science{'/Scopus' if os.getenv('SCOPUS_API_KEY') != 'YOUR_SCOPUS_API_KEY' else ''}", 
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
                    if db_name not in list(databases.keys()):
                        databases[f"Publication {db_name}"] = df
                        st.success(f"Base de données {db_name} ajoutée avec succès.")
    
    else: # API Key not Available
        with st.expander("Récupérer les données WoS/Scopus :", expanded=False):
            uploaded_files = st.file_uploader(
                f"Téléverser les fichiers Web Of Science{'/Scopus' if os.getenv('SCOPUS_API_KEY') == 'YOUR_SCOPUS_API_KEY' else ''}", 
                accept_multiple_files=True,
                type=["xlsx", "xls", "csv"]
            )
            check_list.append(uploaded_files)
            
            # Si des fichiers sont téléversés
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
                    if db_name not in list(databases.keys()):
                        databases[f"Publication {db_name}"] = df

            # st.session_state.show_hal_fields = not st.session_state.show_hal_fields

    empty = st.empty()

    # Lancer la récupération de données
    if empty.button("Lancer la récupération de données", type='primary'):
        if len(check_list) < 2:
            st.error("Veuillez renseigner au moins deux bases de données.")
        else:
            # Récupération des données
            with st.spinner(""):
                bar_perc = 0
                progress_bar = empty.progress(bar_perc, text="Recherche des données orcid en cours...")
                
                # Récupération des données ORCID
                if st.session_state.orcid_researcher:
                    orcid_df = Orcid_Researcher(orcid_link=orcid_researcher).format_df_orcids()
                else:
                    pass
                
                bar_perc += 1
                progress_bar.progress(bar_perc / 3, text="Recherche des données HAL en cours...") 
                

                if st.session_state["id_hal"]:
                    hal_df = get_hal_researcher_data(idhal=id_hal)
                else:
                    hal_df = get_hal_researcher_data(researcher_last_name, researcher_first_name, id_hal)


                bar_perc += 1
                progress_bar.progress(bar_perc/ 3, text="Recherche des données Scopus en cours...") 
                
                # Récupération des données Scopus
                if os.getenv("SCOPUS_API_KEY") != "YOUR_SCOPUS_API_KEY":
                    if st.session_state["scopus_id"]:
                        if len(scopus_id) == 0:
                            st.error("Veuillez renseigner un Scopus ID.")
                        elif len(scopus_id) >= 10:
                            scopus_df = Scopus_Researcher(scopus_id=scopus_id).get_publication_scopus()
                        else:
                            st.error("Le Scopus ID doit contenir au moins 10 chiffres.")
                    else:
                        # st.write("pas de données scopus")
                        pass
                bar_perc += 1
                progress_bar.progress(bar_perc / 3,text="Recherche des données en cours...") 
            
            # Ajout des données dans la base de données
            if st.session_state.id_hal:
                databases["Publication HAL"] = hal_df
            if os.getenv("SCOPUS_API_KEY") != "YOUR_SCOPUS_API_KEY":
                if st.session_state.scopus_id:
                    databases["Publication Scopus"] = scopus_df # if "Publication Scopus" not in list(databases.keys()) else databases["Publication Scopus"]
                else:
                    pass
            if st.session_state.orcid_researcher:
                databases["Publication Orcid"] = orcid_df
            st.success("Données chargées avec succès.")
        empty.empty()

        st.session_state["databases"] = databases

if os.getenv("SCOPUS_API_KEY") == "YOUR_SCOPUS_API_KEY":
        st.warning("Vous n'avez pas de clé API Scopus. Veuillez la renseigner dans le fichier .env ou téléverser les données Scopus.")


st.divider()

# Passer à la page suivante si les données sont chargées
reset, comparaison = st.columns(2)
with comparaison:
    if "databases" in st.session_state.keys():
        reach_st_show_donnee(message = "Montrer les données", type_button = 'primary')
    else:
        pass

# Bouton pour réinitialiser la session
with reset:
    reset_session()