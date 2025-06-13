import streamlit as st
import pandas as pd

def markdown_title(title:str):
    return st.markdown(
    f"""
    <div class="subtitle">
        {title}
    </div>
    """,
    unsafe_allow_html=True)

def move_column_first(df: pd.DataFrame, col_name: str) -> pd.DataFrame:
    """
    Déplace une colonne spécifiée en première position.
    """
    if col_name not in df.columns:
        raise ValueError(f"Colonne '{col_name}' introuvable dans le DataFrame.")
    cols = [col_name] + [col for col in df.columns if col != col_name]
    return df[cols]