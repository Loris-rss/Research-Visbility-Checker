import streamlit as st
import io 

from fonction import compare_all_databases, suggest_column_mapping, compare_publication_databases
from fonction import TxRecoupement, CheckResearcherInPaper

from utilitaire import reset_session, reach_st_donnee

# Si au moins deux bases de données sont chargées

st.title("3. Lancer la comparaison")

st.markdown("""
### Explication
Cette comparaison vous permet de visualiser et d'explorer les données collectées pour le chercheur sélectionné. Vous pouvez consulter les articles trouvés dans chaque base de données, examiner les statistiques principales et analyser la distribution temporelle des publications.
""")

st.divider()

if st.session_state["comparison_mode"] == "Comparer deux bases de données":
    col1, col2 = st.columns(2)
    
    with col1:
        source_name = st.selectbox("Base de données source", options=list(st.session_state["databases"].keys()))
    
    with col2:
        target_name = st.selectbox(
            "Base de données cible", 
            options=[db for db in st.session_state["databases"].keys() if db != source_name]
        )
    
    save_option = st.checkbox("Sauvegarder les résultats", value=True)
    
    if st.button("Comparer les bases de données"):
        st.markdown("## Résultats de la comparaison")
        # Effectuer la comparaison
        compare_publication_databases(
            st.session_state["databases"][source_name],
            st.session_state["databases"][target_name],
            source_name=source_name,
            target_name=target_name,
            save_file=save_option
        )
else:
    save_option = st.checkbox("Sauvegarder les résultats", value=False)
    
    if st.button("Lancer la comparaison de toutes les bases",key="compare_all_databases", type = 'primary'):
        if "databases" not in st.session_state.keys():
            st.error("Veuillez téléverser au moins deux bases de données pour effectuer une comparaison.")
            reach_st_donnee(message = "Revenir à l'importation des données", type_button = 'secondary')
        else:
            compare_all_databases(st.session_state["databases"], save_results=save_option)
st.divider()
reset, deux = st.columns(2)

with reset:
    reset_session()

