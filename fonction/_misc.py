import streamlit as st
import pandas as pd

def markdown_title(title:str) -> markdown:
    """
    Permet d'afficher un titre dans le markdown.
    
    Args :
        title(str) : titre à afficher
    
    Returns :
        markdown : titre affiché
    """
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
    
    Args :
        df(pd.DataFrame) : DataFrame à modifier
        col_name(str) : nom de la colonne à déplacer
    
    Returns :
        pd.DataFrame : DataFrame modifié
    """
    if col_name not in df.columns:
        raise ValueError(f"Colonne '{col_name}' introuvable dans le DataFrame.")
    cols = [col_name] + [col for col in df.columns if col != col_name]
    return df[cols]