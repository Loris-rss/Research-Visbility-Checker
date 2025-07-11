import streamlit as st
import requests
import pandas as pd

class Orcid_Researcher:
    """
    Cette classe permet de récupérer les données depuis l'ORCID.
    
    Elle fournit des méthodes pour :
    - Récupérer les données depuis l'ORCID
    - Transformer les données récupérées en DataFrame
    """
    def __init__(self, orcid_link:str):
        self.orcid_link = orcid_link
        self.df_orcid:pd.DataFrame = self.extract_ids_from_orcids()
        
    def req_orcid(self) -> dict:
        """
        Récupère les données de l'ORCID.
        
        Returns :
            dict : données de l'ORCID
        """
        if "https://orcid.org/" in self.orcid_link:
            return requests.get(self.orcid_link,headers={'Accept':'application/json'}).json()
        else:
            st.write("Pour Orcid :")
            return st.error("L'URL doit contenir https://orcid.org/")

    def extract_ids_from_orcids(self) -> pd.DataFrame:
        """
        Extrait les identifiants de l'ORCID.
        
        Returns :
            pd.DataFrame : DataFrame avec les identifiants de l'ORCID
        """
        response_json = self.req_orcid()
        if isinstance(response_json, dict):
            doi_orcid_list = []
            id_type_list = []
            path_list = []
            title_list = []
            journal_title_list = []
            year_list = []

            path_json = response_json['activities-summary']['works']['group']

            for nb_publi in range(0, len(path_json)):
                # On prend seulement le premier work-summary car c'est le même pour chaque groupe
                work_summary = path_json[nb_publi]["work-summary"][0]
                
                # Récupération des informations de base
                year = (work_summary["publication-date"].get("year", "NaN"))["value"]
                path = work_summary["path"]
                title = work_summary["title"]["title"]["value"]
                journal_title = work_summary.get('journal-title') or {}
                journal_title = journal_title.get("value", "NaN")

                # Pour chaque identifiant externe
                external_ids = path_json[nb_publi]['external-ids']["external-id"]
                for id in range(0, len(external_ids)):
                    year_list.append(year)
                    path_list.append(path)
                    title_list.append(title)
                    journal_title_list.append(journal_title)
                    id_type_list.append(external_ids[id]["external-id-type"])
                    doi_orcid_list.append(external_ids[id]["external-id-value"])
            return pd.DataFrame(data={
                "Titre Article": title_list,
                "Titre Journal": journal_title_list,
                "Orcid path": path_list,
                "type": id_type_list,
                "value": doi_orcid_list,
                "Date de publication": year_list
            }).sort_values("type").reset_index(drop=True)

        else:   
            return None            
    def check_id_missing(self) -> tuple[list, list]:
        """
        Vérifie la présence des identifiants dans un DataFrame.
        
        Args:
            all_ids (list): Liste des identifiants à vérifier
            df (pd.DataFrame): DataFrame contenant les données
            colonne (str): Nom de la colonne à vérifier (par défaut "type")
        
        Returns:
            tuple[list, list]: (ids_presents, ids_manquants)
        """
        
        all_ids = ["other-id","pmc","doi","pmid","wosuid"]
        
        if isinstance(self.df_orcid, pd.DataFrame):
            ids_uniques = set(self.df_orcid["type"].unique())
        else:
            return None, None
        ids_presents = []
        ids_manquants = []
        
        for id_value in all_ids:
            if id_value in ids_uniques:
                ids_presents.append(id_value)
            else:
                ids_manquants.append(id_value)
                
        return ids_presents, ids_manquants

    def to_rename_and_drop(self) -> tuple[dict, list]:
        """
        Renomme et supprime les colonnes du DataFrame.
        
        Args:
            self -> Donner le dataframe avec les informations des articles scientifiques du chercheur souhaité.
            
        Return:
            tuple[dict, list] : Tuple avec le dictionnaire de renommage et la liste des colonnes à supprimer.
        """
        
        ids_present, ids_missing = self.check_id_missing()
        if ids_present is None or ids_missing is None:
            return None, None
        rename_dict = {}
        to_drop = []

        if "doi" in ids_present:
            if "doi" not in rename_dict.keys():
                rename_dict["doi"] = "DOI"
        if "wosuid" in ids_present:
            if "wosuid" not in rename_dict.keys():
                rename_dict["wosuid"] = "UT (Unique WOS ID)"
        if "pmid" in ids_present:
            if "pmid" not in rename_dict.keys():
                rename_dict["pmid"] = "Pubmed Id"

        if "other-id" in ids_present:
            to_drop.append("other-id")
        if "pmc" in ids_present:
            to_drop.append("pmc")

        return rename_dict, to_drop

    def format_df_orcids(self) -> pd.DataFrame | None:
        """ 
        Création des colonnes en fonction du type d'ID (ex: Orcid, Pubmed Id,WoS etc) et remplir ces colonnes avec les bons IDs
        
        Args:
            self -> Donner le dataframe avec les informations des articles scientifiques du chercheur souhaité.
        
        Return:
            pd.DataFrame : DataFrame avec les colonnes "DOI", Pubmed Id et UT (Unique WOS ID).
        """
        rename_dict, to_drop = self.to_rename_and_drop()

        if self.df_orcid is None:
            return None
        else:
            orcid_df_sorted = self.df_orcid.sort_values("type").reset_index(drop=True)

            # Obtenir les types uniques de la colonne 'type' pour créer une colonne par type.
            types_ids = orcid_df_sorted["type"].unique()

            # Créer une nouvelle colonne pour chaque type d'identification (ex: Orcid, Pubmed Id,WoS etc) et remplir ces colonnes avec les bons IDs.
            for id_type in types_ids:
                # Utiliser apply pour remplir chaque colonne en fonction de la condition sur 'type'.
                orcid_df_sorted[id_type] = orcid_df_sorted.apply(lambda x: x["value"] if x["type"] == id_type else None, axis=1)

            if to_drop:
                # On enlève "other-id" et "pmc" parce qu'elles sont négligable et on renomme pour mettre en commun les noms avec WoS.
                orcid_df_id_col = orcid_df_sorted.drop(to_drop,axis=1).rename(columns=rename_dict)
            else:
                orcid_df_id_col = orcid_df_sorted.rename(columns=rename_dict)
            return orcid_df_id_col