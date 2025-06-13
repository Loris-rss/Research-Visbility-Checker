import re

import pandas as pd
import streamlit as st

class CheckResearcherInPaper():
    def __init__(self,dataframe,name_of_auth:str):
        self.dataframe = dataframe
        self.name_of_auth = name_of_auth
        pass

    def researcher_in_paper(self):
        for author_names in self.dataframe["Author Full Names"].tolist():
            author_df_names_lower = author_names.lower()
            if self.name_of_auth in author_df_names_lower:
                continue
        return self.dataframe
    
    def identify_anomalies(self):
        count_auth = {}
        auth_researched_lower = self.name_of_auth.lower()

        # Ajout de la colonne "Anomalie" initialisée à False
        self.dataframe["Anomalie"] = False

        # Parcours de la liste des noms complets des auteurs
        for idx, author_df_names in enumerate(self.dataframe["Author Full Names"].tolist()):
            author_df_names_lower = author_df_names.lower()

            # Vérification si l'auteur recherché n'est pas présent
            if auth_researched_lower not in author_df_names_lower:
                # Marquer cette ligne comme une anomalie
                self.dataframe.at[idx, "Anomalie"] = True

                # Extraction des noms de famille
                author_names_split = re.split(r", |; ", author_df_names_lower)[::2]

                # Comptage des noms de famille uniques
                for unique_last_names in author_names_split:
                    count_auth[unique_last_names] = count_auth.get(unique_last_names, 0) + 1
            else:
                self.dataframe.at[idx, "Anomalie"] = False

        # self.dataframe = self.dataframe.drop("Anomalie", axis=1)
        return self.dataframe

    def report_anomalies(self, df_filtre_anomalie, count_auth):
        if not df_filtre_anomalie.empty:
            # Trier les noms de famille par fréquence et garder les 3 plus fréquents
            sorted_by_values = dict(sorted(count_auth.items(), key=lambda item: item[1], reverse=True)[0:3])

            # Message général
            st.text(
                f"Sur {len(self.dataframe)} articles - il y a {len(df_filtre_anomalie)} articles qui ne sont potentiellement pas au chercheur.\n"
                f"Veuillez vérifier que ces articles vous appartiennent bien.\n"
                f"Voici les 3 noms de familles qui reviennent le plus souvent."
            )

            # Détails des noms fréquents
            for key, value in sorted_by_values.items():
                st.text(f"Nom : {key.capitalize()} : {value} fois")
        else:
            st.write("Il n'y a pas d'anomalie")

def action_suggeree(df):
    name_file_list = df["profile"]

    # S'il n'y a pas d'orcid_path (donc NaN -> float) = dans WoS.
    if pd.isna(df["orcid path"]):  # Vérifie si la valeur est NaN
        if df["Anomalie"] == True:
            return "Nous pensons que ces publications ne vous appartiennent pas. Nous vous suggérons de les supprimer des deux profils WoS."
        return f"Pas dans orcID"
        
    

    elif isinstance(df["orcid path"], str):  # Vérifie si c'est une chaîne (donc un ID ORCID)
        if df["Anomalie"] == True:
            return "Nous pensons que ces publications ne vous appartiennent pas. Nous vous suggérons de les supprimer des deux profils WoS."
        return f"Dans ORCID et situé dans votre WoS ResearcherID : {name_file_list}"