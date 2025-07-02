import streamlit as st
import pandas as pd
from io import BytesIO
from utilitaire import reset_session, reach_st_comparaison, reach_st_donnee, read_markdown_file

st.title("3. Vérifier les données")

st.markdown("""
Cette page vous permet de visualiser et d'explorer les données collectées pour le chercheur sélectionné. Vous pouvez consulter les articles trouvés dans chaque base de données, examiner les statistiques principales et analyser la distribution temporelle des publications.
""")

with st.expander("Guide de la page pour la visualisation des données.", expanded=False):
    st.markdown(read_markdown_file(r"md/Visualisation des données.md"), unsafe_allow_html=True)

st.write("Voici les données trouvées pour le chercheur :")

tabs = st.tabs(list(st.session_state["databases"].keys()))

# Pour chaque onglet, afficher le DataFrame correspondant
for tab, (db_name, df) in zip(tabs, st.session_state["databases"].items()):
    with tab:
        st.header(f"Données de {db_name}")
        if "Unnamed: 0" in df.columns:
            df = df.drop(columns=["Unnamed: 0"])
        st.write(f"{len(df)} articles de recherche trouvés.")
        # Va falloir rajouter d'autres statistiques
        st.dataframe(df)
        date_list_col = ["Year","year", "Date", "publicationDate_s", "Publication Year"]

        right_col = "".join([col for col in df.columns if col in date_list_col])
        
        csv, xlsx = st.columns(2)
        with csv:
            csv_data = df.to_csv(index=False)
            if st.download_button("Télécharger les données en csv", csv_data, file_name=f"{db_name}.csv", mime="text/csv"):
                st.success("Les données ont été téléchargées avec succès.")
        with xlsx:
            output = BytesIO()
            df.to_excel(output, index=False, engine='openpyxl')
            xlsx_data = output.getvalue()
            
            if st.download_button("Télécharger les données en excel", xlsx_data, file_name=f"{db_name}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"):
                st.success("Les données ont été téléchargées avec succès.")

        st.divider()

        st.markdown("## Distribution temporelle des publications")
        # Distribution des publications par anné
        with st.expander("Distribution temporelle des publications", expanded=False):
            st.markdown("""
            Cette section présente la répartition des publications scientifiques par année. Cela permet de visualiser l'évolution du volume de publications au fil du temps pour le chercheur sélectionné.
            """)
            publications_par_annee = df[right_col].value_counts().sort_index()
            st.bar_chart(publications_par_annee)

st.divider()

reset, back, forward = st.columns(3)
with reset:
    reset_session()
with back:
    reach_st_donnee(message = "Revenir à l'importation des données", type_button = 'secondary')
with forward:
    reach_st_comparaison()