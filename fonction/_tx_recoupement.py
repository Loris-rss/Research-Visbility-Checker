import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

class TxRecoupement:
    """
    Cette classe permet de calculer le taux de recoupement entre deux DataFrames.
    """
    def __init__(self, source_df: pd.DataFrame = None, target_df:pd.DataFrame = None, provenance:str = None):
        """
        Initialise la classe TxRecoupement.
        
        Args:
            source_df(pd.DataFrame) : DataFrame source
            target_df(pd.DataFrame) : DataFrame cible
            provenance(str) : provenance des données
        """
        self.source_df = source_df
        self.target_df = target_df
        self.provenance = provenance
        # Obtention des noms de colonnes pertinentes
        self.col_name_tuple = self.get_col_name()
    
    def get_col_name(self) -> tuple:
        """
        Identifie les colonnes pertinentes dans le DataFrame.
        
        Return:
            tuple : tuple avec les noms des colonnes DOI, Pubmed et Wos
        """
        doi_col = None
        pubmed_col = None
        wos_col = None

        # Récupération des noms de colonnes
        for col in self.source_df.columns:
            lower_col = col.lower()
            
            # Récupération de la colonne DOI
            if "doi" in lower_col:
                doi_col = col if doi_col is None else doi_col
            
            # Récupération de la colonne Pubmed
            elif "pubmed" in lower_col:
                pubmed_col = col if pubmed_col is None else pubmed_col
            
            # Récupération de la colonne Wos
            elif "ut (unique wos id)" in lower_col:
                wos_col = col if wos_col is None else wos_col

        if doi_col is None:
            st.warning(f"Aucune colonne DOI trouvée pour {self.provenance}")
        if pubmed_col is None:
            st.warning(f"Aucune colonne Pubmed trouvée pour {self.provenance}")
            
        return doi_col, pubmed_col, wos_col

    def get_tx_recoup(self) -> pd.DataFrame:
        """
        Calcule le taux de recoupement entre deux DataFrames.
        
        Return:
            pd.DataFrame : DataFrame avec les taux de recoupement
        """
        doi, pubmed, wos = self.col_name_tuple
        
        # Vérification des colonnes requises
        if doi is None:
            st.error(f"Colonne DOI manquante pour {self.provenance}")
            return None
            
        if pubmed is None:
            st.warning(f"Colonne Pubmed manquante pour {self.provenance}, le recoupement sera limité au DOI")
            # Créer une colonne fictive pour éviter les erreurs
            self.df[pubmed] = None

        if "Unnamed: 0" in self.df.columns:
            self.df = self.df.drop(columns="Unnamed: 0")

        # Vérification des colonnes Orcid requises
        required_orcid_cols = ["value", "DOI", "Pubmed Id"]
        missing_cols = [col for col in required_orcid_cols if col not in self.target_df.columns]
        
        if missing_cols:
            st.error(f"Colonnes manquantes dans les données Orcid: {missing_cols}")
            # Créer des colonnes fictives pour éviter les erreurs
            for col in missing_cols:
                self.target_df[col] = None

        try:
            if self.df[pubmed].dtype == "float64":
                self.df[pubmed] = pd.to_numeric(self.df[pubmed], errors="coerce").astype("Int64")
            elif pubmed is not None:
                self.df[pubmed] = self.df[pubmed].apply(lambda x: x if x != "[]" else None)
        except Exception as e:
            st.error(f"Erreur lors de la conversion de la colonne Pubmed: {str(e)}")
            self.df[pubmed] = None

        try:
            self.df["common_doi"] = self.df[doi].isin(self.target_df["value"])
            self.df["common_pubmed"] = self.df[pubmed].isin(self.target_df["value"])
            self.target_df["common_doi"] = self.target_df["DOI"].isin(self.df[doi])
            self.target_df["common_pubmed"] = self.target_df["Pubmed Id"].isin(self.df[pubmed])
        except Exception as e:
            st.error(f"Erreur lors de la comparaison des identifiants: {str(e)}")
            return None

        try:
            if wos:
                # Vérifier si "UT (Unique WOS ID)" existe dans df_orcid
                if "UT (Unique WOS ID)" not in self.target_df.columns:
                    self.target_df["UT (Unique WOS ID)"] = None
                    
                self.df["common_wos"] = self.df[wos].isin(self.target_df["value"])
                self.target_df["common_wos"] = self.target_df["UT (Unique WOS ID)"].isin(self.df[wos])
                
                common_cols = ["common_doi", "common_pubmed", "common_wos"]
            else:
                common_cols = ["common_doi", "common_pubmed"]
        except Exception as e:
            common_cols = ["common_doi", "common_pubmed"]
        
        self.df["common_publi"] = self.df[common_cols].any(axis=1)
        self.target_df["common_publi"] = self.target_df[common_cols].any(axis=1)
        
        common_publi = self.df[self.df["common_publi"]].reset_index(drop=True)
        df_unco_publi = self.df[~self.df["common_publi"]].reset_index(drop=True)
        df_unco_publi_orcid = self.target_df[~self.target_df["common_publi"]].reset_index(drop=True)
        df_common_orcid = self.target_df[self.target_df["common_publi"]].reset_index(drop=True)
        # Résultats
        tx_recoup = f"{(len(common_publi) / len(self.df)) * 100:.2f}%"
        
        st.markdown(f"""
            ### Résultats du Taux de Recoupement :

            - **Source** : ORCID et {self.provenance}
            - **Total des publications** : {len(self.df)}
            - **Publications Communes** : {len(common_publi)}
            - **Taux de recoupement** : {tx_recoup}
        """)
        # self.df = self.df.drop(columns=common_cols + ["common_publi"])

        unco, common, unco_orcid, common_orcid = st.tabs([f"Non Commun {self.provenance}", f"Commun {self.provenance}","Non Common orcID","Common orcID"])
        
        with unco:
            st.write(df_unco_publi.drop(["common_publi"]+common_cols, axis=1))
        with common:
            st.write(common_publi.drop(["common_publi"]+common_cols, axis=1))
        
        # Vérifier quelles colonnes sont disponibles avant de les supprimer
        cols_to_drop = []
        for col in ["Unnamed: 0", "common_publi", "common_doi", "common_pubmed", "UT (Unique WOS ID)"]:
            if col in df_unco_publi_orcid.columns:
                cols_to_drop.append(col)
                
        with unco_orcid:
            if cols_to_drop:
                st.write(df_unco_publi_orcid.drop(cols_to_drop, axis=1))
            else:
                st.write(df_unco_publi_orcid)
        with common_orcid:
            if cols_to_drop:
                st.write(df_common_orcid.drop(cols_to_drop, axis=1))
            else:
                st.write(df_common_orcid)

def normalize_doi(doi_str)  -> str:
    """
    Normalise le DOI pour améliorer la correspondance.
    
    Args:
        doi_str(str) : DOI à normaliser.
        
    Return:
        str : DOI normalisé.
    """
    if not isinstance(doi_str, str):
        return doi_str
    
    doi_str = doi_str.lower()
    doi_str = doi_str.replace('doi:', '').replace('https://doi.org/', '').replace('http://doi.org/', '')
    doi_str = doi_str.strip()
    return doi_str

def create_id_column(df) -> pd.DataFrame:
    """
    Crée une colonne all_ids contenant tous les identifiants disponibles.
    
    Args:
        df(pd.DataFrame) : DataFrame à modifier.
    
    Return:
        pd.DataFrame : DataFrame modifié.
    """
    # Vérifier si l'objet est un DataFrame
    if not isinstance(df, pd.DataFrame):
        
        # Convertir en DataFrame si c'est une liste de dictionnaires
        if isinstance(df, list) and df and isinstance(df[0], dict):
            df = pd.DataFrame(df)
        else:
            # Si ce n'est pas une liste de dictionnaires, créer un DataFrame vide
            df = pd.DataFrame()
    
    # Vérifier si le DataFrame est vide
    if df.empty:
        df['all_ids'] = None
        return df
        
    id_columns = []
    for col in df.columns:
        col_lower = col.lower()
        if any(term in col_lower for term in ['doi', 'scopus_id', 'pubmed', 'wos', 'ut (unique']):
            id_columns.append(col)
    
    # Si aucune colonne d'ID n'est trouvée, ajouter une colonne vide
    if not id_columns:
        df['all_ids'] = None
        return df
    
    def combine_ids(row):
        ids = []
        for col in id_columns:
            if pd.notna(row[col]) and row[col] not in ['', '[]']:
                # Normaliser directement l'identifiant
                value = str(row[col])
                if 'doi' in col.lower():
                    value = normalize_doi(value)
                ids.append(value)
        return ids if ids else None
    
    df['all_ids'] = df.apply(combine_ids, axis=1)
    return df

def suggest_column_mapping(df) -> dict:
    """
    Pas utilisé
    Suggère un mapping automatique des colonnes importantes (DOI, Pubmed, etc.) à partir des noms de colonnes existants.
    
    Args:
        df(pd.DataFrame) : DataFrame à modifier.
        
    Return:
        dict : mapping des colonnes.
    """
    mapping = {
        "doi": None,
        "pubmed": None,
        "wos": None,
        "scopus": None,
        "title": None
    }
    
    # Chercher les colonnes par mots-clés
    for col in df.columns:
        col_lower = col.lower()
        
        # DOI
        if "doi" in col_lower and mapping["doi"] is None:
            mapping["doi"] = col
        
        # Pubmed
        elif any(term in col_lower for term in ["pubmed", "pmid"]) and mapping["pubmed"] is None:
            mapping["pubmed"] = col
        
        # WoS
        elif any(term in col_lower for term in ["wos", "ut (unique", "web of science"]) and mapping["wos"] is None:
            mapping["wos"] = col
        
        # Scopus
        elif "scopus" in col_lower and mapping["scopus"] is None:
            mapping["scopus"] = col
        
        # Titre
        elif any(term in col_lower for term in ["title", "titre"]) and mapping["title"] is None:
            mapping["title"] = col
    
    return mapping

def compare_publication_databases(source_df, target_df, source_name="Source", target_name="Target", save_file=True) -> pd.DataFrame:
    """
    Compare deux bases de données de publications scientifiques et identifie les recoupements.
    
    Args:
        source_df(pd.DataFrame) : DataFrame source
        target_df(pd.DataFrame) : DataFrame cible
        source_name(str) : nom de la source
        target_name(str) : nom de la cible
        save_file(bool) : enregistrer les résultats
    
    Return:
        pd.DataFrame : DataFrame avec les résultats
    """
    message = st.empty()
    with st.spinner(f"Comparaison entre {source_name} et {target_name} en cours..."):
        # Vérifier si les objets sont des DataFrames
        if not isinstance(source_df, pd.DataFrame):
            if isinstance(source_df, list) and source_df and isinstance(source_df[0], dict):
                source_df = pd.DataFrame(source_df)
            else:
                st.warning(f"La base de données source {source_name} n'est pas un DataFrame valide.")
                return pd.DataFrame()
        
        # Vérifier si ça fait pas la même chose.
        if not isinstance(target_df, pd.DataFrame):
            if isinstance(target_df, list) and target_df and isinstance(target_df[0], dict):
                target_df = pd.DataFrame(target_df)
            else:
                st.warning(f"La base de données cible {target_name} n'est pas un DataFrame valide.")
                return source_df
        
        if target_df.empty:
            st.warning(f"La base de données cible {target_name} est vide.")
            # Retourner un DataFrame avec les colonnes nécessaires mais sans correspondances
            source = source_df.copy()
            in_target_col = f"in_{target_name.lower()}"
            matching_id_col = f"matching_id_{target_name.lower()}"
            status_col = f"statut_{target_name.lower()}"
            
            source = create_id_column(source)
            source[in_target_col] = False
            source[matching_id_col] = None
            source[status_col] = f"Pas dans {target_name}"
            
            return source
        
        # ---- 1. Préparation des données ---- 
        source = source_df.copy()
        target = target_df.copy()
        
        source = create_id_column(source)
        target = create_id_column(target)
        
        # ---- 2. Création d'un ensemble d'identifiants cibles pour recherche rapide ---- 
        target_ids = set()
        for ids in target['all_ids'].dropna():
            if isinstance(ids, list) and ids:
                target_ids.update(ids)
        
        # ---- 3. Recherche des correspondances ---- 
        in_target_col = f"in_{target_name.lower()}"
        matching_id_col = f"matching_id_{target_name.lower()}"
        
        source[in_target_col] = False
        source[matching_id_col] = None
        
        progress_bar = st.progress(0)
        total_rows = len(source)
        
        for idx, row in source.iterrows():
            progress_bar.progress((idx + 1) / total_rows)
            
            if not isinstance(row['all_ids'], list) or not row['all_ids']:
                continue
                
            for id_str in row['all_ids']:
                if id_str in target_ids:
                    source.at[idx, in_target_col] = True
                    source.at[idx, matching_id_col] = id_str
                    break
        
        # ---- 4. Calcul des statistiques ---- 
        total_source = len(source)
        found_in_target = source[in_target_col].sum()
        percentage = (found_in_target / total_source) * 100 if total_source > 0 else 0
        
        # ---- 5. Création d'une colonne de statut ---- 
        status_col = f"statut_{target_name.lower()}"
        source[status_col] = source[in_target_col].apply(
            lambda x: f"Dans {target_name}" if x else f"Pas dans {target_name}"
        )
        message.success("Comparaison terminée avec succès!")
        message.empty()
        
        # ---- 6. Affichage des résultats ----  
        
        st.subheader("Résultats")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Publications dans " + source_name, total_source)
            st.metric("Dont publications trouvées dans " + target_name, found_in_target)
        
        with col2:
            st.metric("Taux de recoupement", f"{percentage:.2f}%")

            def create_pie_chart(source_name, target_name, values, ax):
                # Configuration des styles pour chaque catégorie
                resultat = values[f"Pas dans {target_name}"] > values[f"Dans {target_name}"]
                
                # Configuration des styles en fonction de la valeur la plus grande
                if resultat:
                    # Réorganiser les valeurs pour qu'elles correspondent aux labels
                    labels = [f"Pas dans {target_name}", f"Dans {target_name}"]
                    colors = ["red", "green"]
                
                else:
                    labels = [f"Dans {target_name}", f"Pas dans {target_name}"]
                    colors = ["green", "red"]
                    
                
                # Créer le graphique
                ax.pie(values, 
                    labels=labels,
                    colors=colors,
                    explode=[0.05, 0],
                    autopct="%1.1f%%")
                ax.set_title(f'Proportion des articles {source_name} présents dans {target_name}')
                
                if "plot_pie_chart" not in st.session_state.keys():
                    st.session_state["plot_pie_chart"] = {f"plot_{source_name}_{target_name}": fig}
                else:
                    st.session_state["plot_pie_chart"][f"plot_{source_name}_{target_name}"] = fig
                st.pyplot(fig)

            fig, ax = plt.subplots(figsize=(6, 6))
            status_counts = source[status_col].value_counts()
            create_pie_chart(source_name, target_name, status_counts, ax)
        
        # ---- 7. Affichage des tableaux ---- 
        st.subheader("Détail des résultats")
        tabs = st.tabs(["Tous les articles", f"Communs ({found_in_target})", f"Non trouvés ({total_source - found_in_target})"])
        
        with tabs[0]:
            display_cols = [col for col in source.columns if col not in ["all_ids", status_col, in_target_col, matching_id_col, "Unnamed: 0"]]
            st.dataframe(source[display_cols], height=400)
        
        with tabs[1]:
            common_pubs = source[source[in_target_col]].reset_index(drop=True)
            if len(common_pubs) > 0:
                display_cols = [col for col in common_pubs.columns if col not in ["all_ids", status_col, in_target_col, matching_id_col, "Unnamed: 0"]]
                st.dataframe(common_pubs[display_cols], height=400)
        
        with tabs[2]:
            missing_pubs = source[~source[in_target_col]].reset_index(drop=True)
            if len(missing_pubs) > 0:
                display_cols = [col for col in missing_pubs.columns if col not in ["all_ids", status_col, in_target_col, matching_id_col, "Unnamed: 0"]]
                st.dataframe(missing_pubs[display_cols], height=400)
        
        if save_file:
            source.to_excel(f"{source_name}_{target_name}.xlsx")

        return source

def compare_all_databases(databases, save_results=True) -> dict:

    """
    Compare toutes les combinaisons possibles de bases de données fournies.
    
    Args:
        databases(dict) : dictionnaire avec les bases de données
        save_results(bool) : enregistrer les résultats
    
    Return:
        dict : dictionnaire avec les résultats
    """
    if len(databases) < 2:
        st.warning("Veuillez téléverser au moins deux bases de données pour effectuer une comparaison.")
        return None
    
    # Vérifier que toutes les entrées sont des DataFrames valides
    for name, df in databases.items():
        if not isinstance(df, pd.DataFrame):
            st.error(f"La base de données '{name}' n'est pas un DataFrame valide.")
            return None
    
    results = {}
    recap = []
    
    # Création d'une barre de progression
    progress_bar = st.progress(0)
    
    # Calculer le nombre total de comparaisons
    n_databases = len(databases)
    total_comparisons = n_databases * (n_databases - 1)  # Nombre de permutations n*(n-1)
    
    # Compteur pour la progression
    comp_counter = 0
            
    source_names = list(databases.keys())
    # Créer un onglet par base de données
    tabs = st.tabs(source_names)

    for i, (source_name, tab) in enumerate(zip(source_names, tabs)):
            with tab:
                st.header(f"Comparaisons avec {source_name} comme source")
                # Comparer avec toutes les autres bases de données
                for target_name in source_names:
                    if target_name != source_name:  # Éviter de comparer une base avec elle-même
                        comp_counter += 1
                        progress_bar.progress(comp_counter / total_comparisons)
                        
                        st.markdown(f"### Comparaison {source_name} → {target_name}")
                        key = f"{source_name}_{target_name}"
                        
                        try:
                            results[key] = compare_publication_databases(
                                databases[source_name],
                                databases[target_name],
                                source_name=source_name, 
                                target_name=target_name,
                                save_file=save_results
                            )
                            
                            # Création des statistiques pour le récapitulatif
                            if not results[key].empty:
                                in_target_col = f"in_{target_name.lower()}"
                                total = len(results[key])
                                found = results[key][in_target_col].sum()
                                percentage = (found / total) * 100 if total > 0 else 0
                                
                                recap.append({
                                    'Source': source_name,
                                    'Cible': target_name,
                                    'Total articles source': total,
                                    'Articles trouvés dans cible': found,
                                    'Taux de recoupement': f"{percentage:.2f}%"
                                })
                        except Exception as e:
                            st.error(f"Erreur lors de la comparaison entre {source_name} et {target_name}: {str(e)}")
                        
                        st.markdown("---")
        
    # Créer un tableau récapitulatif des taux de recoupement
    if recap:
        st.subheader("Récapitulatif des taux de recoupement")
        recap_df = pd.DataFrame(recap)
        st.dataframe(recap_df)
    else:
        st.warning("Aucune comparaison n'a pu être effectuée avec succès.")
    
    return results