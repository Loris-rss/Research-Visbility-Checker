import streamlit as st

from fonction import compare_all_databases

from utilitaire import reset_session, reach_st_donnee, download_plot, download_all_plots

# Si au moins deux bases de données sont chargées

st.title("3. Lancer la comparaison")

st.markdown("""
### Explication
Cette comparaison vous permet de visualiser et d'explorer les données collectées pour le chercheur sélectionné. Vous pouvez consulter les articles trouvés dans chaque base de données, examiner les statistiques principales et analyser la distribution temporelle des publications.
""")

st.divider()
st.markdown("## Comparaison de vos bases de données.")

# Si aucune base de données n'est chargée
if "databases" not in st.session_state.keys():
    st.error("Veuillez téléverser au moins deux bases de données pour effectuer une comparaison.")
    reach_st_donnee(message = "Revenir à l'importation des données", type_button = 'secondary')
else:
    compare_all_databases(st.session_state["databases"])
    
# Si des graphiques sont disponibles
if "plot_venn_diagram" in st.session_state.keys():
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

