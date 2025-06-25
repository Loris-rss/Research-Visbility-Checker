import streamlit as st
from os import path
import io

from utilitaire import read_markdown_file

st.set_page_config("Research Visibility Checker", layout="wide")

st.markdown("""
# Bienvenue sur Research Visibility Checker !"""
)

with st.expander("Présentation de l'application", expanded=False):
    st.markdown(read_markdown_file(r"md\presentation_app.md"), unsafe_allow_html=True)

st.divider()
# Retrieve the matplotlib figure
fig = st.session_state["plot_pie_chart"]["plot_Marc humbert wos_Scopus"]

# Convert the figure to PNG in-memory
buf = io.BytesIO()
fig.savefig(buf, format='png')
buf.seek(0)
st.divider()

st.download_button(
    label="Télécharger le graphique",
    data=buf,
    file_name="plot_Marc humbert wos_Scopus.png",
    mime="image/png"
)

def main():
    if "navigation" not in st.session_state:
        st.navigation([st.Page(path.relpath("pages/1_st_choix_analyse.py"),title='Research Visibility Checker'), st.Page(path.relpath("pages/0_tutorial.py"),title='Tutoriel')]).run()
    else: 
        st.navigation([st.Page(path.relpath(f"pages/{st.session_state["navigation"]}"), title="Research Visibility Checker"), st.Page(path.relpath("pages/0_tutorial.py"),title='Tutoriel')]).run()

if __name__ == "__main__":
    main()