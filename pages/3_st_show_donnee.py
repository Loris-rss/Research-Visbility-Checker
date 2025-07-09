from io import BytesIO

import streamlit as st
import pandas as pd
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
    # Afficher les données de la base de données
    with tab:
        st.header(f"Données de {db_name}")
        # Vérifier que df est bien un DataFrame
        if not isinstance(df, pd.DataFrame):
            st.error(f"❌ Erreur : Les données de {db_name} ne sont pas dans le bon format.")
            st.write(f"Type reçu : {type(df)}")
            st.write(f"Contenu : {df}")
            st.info("💡 Retournez à l'étape d'importation des données pour corriger le problème.")
            continue
        # Supprimer la colonne "Unnamed: 0" si elle existe
        st.write(f"📊 Colonnes disponibles : {list(df.columns)}")   
        if "Unnamed: 0" in df.columns:
            df = df.drop(columns=["Unnamed: 0"])     
        # Afficher le nombre d'articles de recherche trouvés
        st.write(f"📚 **{len(df)} articles de recherche trouvés.**")     
        # Vérifier que le DataFrame n'est pas vide
        if df.empty:
            st.warning(f"⚠️ Aucune donnée trouvée pour {db_name}")
            continue     
        # Afficher les données dans un tableau
        st.dataframe(df)

        # Définir les colonnes de date
        date_list_col = ["Year","year", "Date", "publicationDate_s", "Publication Year"]

        # Définir la bonne colonne de date pour chaque dataframe
        right_col = "".join([col for col in df.columns if col in date_list_col])
    
        csv, xlsx = st.columns(2)
        
        # Création du bouton de téléchargement en csv
        with csv:
            csv_data = df.to_csv(index=False).encode("utf-8")

            # Créer le bouton de téléchargement
            st.download_button(
                label="Télécharger les données en csv",
                data=csv_data,
                file_name=f"{db_name}.csv",
                mime="text/csv"
            )
        
        # Création du bouton de téléchargement en excel
        with xlsx:
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')

            # Repositionner le curseur du buffer au début
            output.seek(0)

            # Téléchargement des données en excel
            st.download_button(
                label="Télécharger les données en excel",
                data=output,
                file_name=f"{db_name}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )


        st.divider()

        st.markdown("## Distribution temporelle des publications")
        
        # Distribution des publications par année
        with st.expander("Distribution temporelle des publications", expanded=False):
            st.markdown("""
            Cette section présente la répartition des publications scientifiques par année. Cela permet de visualiser l'évolution du volume de publications au fil du temps pour le chercheur sélectionné.
            """)
            publications_par_annee = df[right_col].value_counts().sort_index()
            st.bar_chart(publications_par_annee)

st.divider()

# Création des boutons de réinitialisation et de retour
reset, back, forward = st.columns(3)
with reset:
    reset_session()
with back:
    reach_st_donnee(message = "Revenir à l'importation des données", type_button = 'secondary')
with forward:
    reach_st_comparaison()