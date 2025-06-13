import streamlit as st
import pandas as pd

from utilitaire import reset_session, reach_st_comparaison, reach_st_donnee, read_markdown_file

st.title("3. Vérifier les données")

with st.expander("Guide de la page pour la visualisation des données.", expanded=False):
    st.markdown(read_markdown_file(r"md\Visualisation des données.md"), unsafe_allow_html=True)

st.write("Voici les données trouvées pour le chercheur :")

st.write(st.session_state)


tabs = st.tabs(list(st.session_state["databases"].keys()))
    
reset, back, forward = st.columns(3)
with reset:
    reset_session()
with back:
    reach_st_donnee(message = "Revenir à l'importation des données", type_button = 'secondary')
with forward:
    reach_st_comparaison()

# Pour chaque onglet, afficher le DataFrame correspondant
for tab, (db_name, df) in zip(tabs, st.session_state["databases"].items()):
    with tab:
        st.header(f"Données de {db_name}")
        if "Unnamed: 0" in df.columns:
            df = df.drop(columns=["Unnamed: 0"])
        st.write(f"{len(df)} articles de recherche trouvés.")
        # Va falloir rajouter d'autres statistiques
        st.dataframe(df)
        date_list_col = ["year", "Date", "publicationDate_s"]

        right_col = "".join([col for col in df.columns if col in date_list_col])

        if right_col == "publicationDate_s":
            df[right_col] = df[right_col].apply(lambda x: x.split("-")[0])
        
        if right_col == "Date":
            
            def extract_last_or_full(x):
                words = x.split(" ")
                return words[-1] if words[-1].isdigit() else x.split(" ")[0]

            df[right_col] = df[right_col].apply(extract_last_or_full)

        # Distribution des publications par année
        with st.expander("Distribution temporelle des publications"):
            # Rajouter description
            publications_par_annee = df[right_col].value_counts().sort_index()
            st.bar_chart(publications_par_annee)

st.divider()

