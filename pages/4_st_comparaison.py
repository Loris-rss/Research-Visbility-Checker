import streamlit as st

from fonction import compare_all_databases, suggest_column_mapping, compare_publication_databases
from fonction import TxRecoupement, CheckResearcherInPaper

from utilitaire import reset_session, reach_st_donnee, download_plot, download_all_plots

# Si au moins deux bases de données sont chargées

st.title("3. Lancer la comparaison")

st.markdown("""
### Explication
Cette comparaison vous permet de visualiser et d'explorer les données collectées pour le chercheur sélectionné. Vous pouvez consulter les articles trouvés dans chaque base de données, examiner les statistiques principales et analyser la distribution temporelle des publications.
""")

st.divider()
st.markdown("## Comparaison de vos bases de données.")

# if st.session_state["comparison_mode"] == "Comparer deux bases de données":
#     # ---- 1. Sélection des bases de données ---- 
#     col1, col2 = st.columns(2)
    
#     # ---- 2. Sélection de la base de données source ---- 
#     with col1:
#         source_name = st.selectbox("Base de données source", options=list(st.session_state["databases"].keys()))
    
#     # ---- 3. Sélection de la base de données cible ---- 
#     with col2:
#         target_name = st.selectbox(
#             "Base de données cible", 
#             options=[db for db in st.session_state["databases"].keys() if db != source_name]
#         )
    
#     # ---- 4. Sauvegarder les résultats ---- 
#     save_option = st.checkbox("Sauvegarder les graphiques", value=True)
    
#     # ---- 5. Lancer la comparaison ---- 
#     if st.button("Comparer les bases de données"):
#         # ---- 6. Afficher les résultats ---- 
#         st.markdown("## Résultats de la comparaison")
#         # Effectuer la comparaison
#         compare_publication_databases(
#             st.session_state["databases"][source_name],
#             st.session_state["databases"][target_name],
#             source_name=source_name,
#             target_name=target_name,
#             save_file=save_option
#         )
    
#     st.divider()

# Si aucune base de données n'est chargée
if "databases" not in st.session_state.keys():
    st.error("Veuillez téléverser au moins deux bases de données pour effectuer une comparaison.")
    reach_st_donnee(message = "Revenir à l'importation des données", type_button = 'secondary')
else:
    compare_all_databases(st.session_state["databases"])


# Si des graphiques sont disponibles
if "plot_pie_chart" in st.session_state.keys():
    st.divider()
    st.markdown("## Télécharger un graphique ou plusieurs graphiques ?")
    
    dl_choice = st.radio(label = "", options=["Un graphique", "Tous les graphiques"], index=0)
    
    if dl_choice == "Un graphique":
        st.markdown("## Télécharger un graphique")
        download_plot()
    else:
        st.markdown("## Télécharger tous les graphiques")
        download_all_plots()
else:
    pass

st.divider()

reset, deux = st.columns(2)

# Bouton pour réinitialiser la session
with reset:
    reset_session()

