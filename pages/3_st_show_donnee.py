import streamlit as st
import pandas as pd

from utilitaire import reset_session, reach_st_comparaison, reach_st_donnee, read_markdown_file

st.title("3. Vérifier les données")

st.markdown("""
Cette page vous permet de visualiser et d'explorer les données collectées pour le chercheur sélectionné. Vous pouvez consulter les articles trouvés dans chaque base de données, examiner les statistiques principales et analyser la distribution temporelle des publications.
""")

with st.expander("Guide de la page pour la visualisation des données.", expanded=False):
    st.markdown(read_markdown_file(r"md\Visualisation des données.md"), unsafe_allow_html=True)

st.write("Voici les données trouvées pour le chercheur :")

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
        st.write(df.columns)
        date_list_col = ["year", "Date", "publicationDate_s", "Publication Year"]

        right_col = "".join([col for col in df.columns if col in date_list_col])
        
        if right_col == "publicationDate_s":
            df[right_col] = df[right_col].apply(lambda x: x.split("-")[0])
        
        if right_col == "Date":
            
            def extract_last_or_full(x:str) -> str:
                """
                Extrait le dernier mot ou la première phrase si le dernier mot n'est pas un nombre.
                
                Args:
                    x (str): La chaîne de caractères à traiter.
                    
                Returns:
                    str: Le dernier mot ou la première phrase si le dernier mot n'est pas un nombre.
                """
                words = x.split(" ")
                return words[-1] if words[-1].isdigit() else x.split(" ")[0]

            df[right_col] = df[right_col].apply(extract_last_or_full)
        
        csv, xlsx = st.columns(2)
        with csv:
            if st.button("Télécharger les données en csv", type = 'secondary', key = f"csv_{db_name}"):
                df.to_csv(f"{db_name}.csv", index=False)
                st.success("Les données ont été téléchargées avec succès.")
        with xlsx:
            if st.button("Télécharger les données en excel", type = 'secondary', key = f"xlsx_{db_name}"):
                df.to_excel(f"{db_name}.xlsx", index=False)
                st.success("Les données ont été téléchargées avec succès.")

        # Distribution des publications par année
        with st.expander("Distribution temporelle des publications", expanded=True):
            st.markdown("""
            Cette section présente la répartition des publications scientifiques par année. Cela permet de visualiser l'évolution du volume de publications au fil du temps pour le chercheur sélectionné.
            """)
            # st.write("Publication Year", df["Publication Year"])
            # st.write(df[right_col])
            # publications_par_annee = df[right_col].value_counts().sort_index()
            # st.bar_chart(publications_par_annee)

st.divider()

