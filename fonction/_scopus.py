import requests

import pandas as pd
import streamlit as st
import os

from dotenv import load_dotenv
load_dotenv(r".env")
scopus_api_key = os.getenv("SCOPUS_API_KEY")
scopus_insttoken = os.getenv("SCOPUS_INSTTOKEN")

class Scopus_Researcher:
    def __init__(self, scopus_id):
        self.scopus_id = str(scopus_id)
        self.api_key = scopus_api_key  # Définir avant l'appel à get_scopus_data
        self.insttoken = scopus_insttoken
        self.df_scopus: pd.DataFrame = self.get_scopus_data()  # Appel après la définition des attributs

    def get_scopus_data(self) -> list:
        """
        Récupère les données depuis l'API Scopus.
        """
        found_items_num: int = 1
        start_item: int = 0
        items_per_query: int = 200
        max_items: int = 1305
        JSON: list = []

        while found_items_num > 0:
            resp = requests.get(
                'https://api.elsevier.com/content/search/scopus',
                headers={'Accept': 'application/json', 'X-ELS-APIKey': self.api_key},
                params={
                    'query': f"AU-ID({self.scopus_id})",
                    'count': items_per_query,
                    'start': start_item,
                    'insttoken': self.insttoken
                }
            )

            if resp.status_code != 200:
                break
                # raise Exception(f"Scopus API error {resp.status_code}, JSON dump: {resp.json()}")

            if found_items_num == 1:
                found_items_num = int(resp.json().get('search-results').get('opensearch:totalResults'))

            if found_items_num == 0:
                st.error("Nous n'avons pas trouvé d'article pour ce Scopus ID.")
                break

            search_results = resp.json()['search-results']
            if 'entry' in search_results:
                JSON += search_results['entry']

            start_item += items_per_query
            found_items_num -= items_per_query

            if start_item >= max_items:
                break
        
        return JSON

    def get_publication_scopus(self) -> pd.DataFrame:
        """
        Transforme les données récupérées depuis l'API Scopus en DataFrame.
        """
        scopus_articles = self.df_scopus
        data_list = []
        for articles in scopus_articles:
            data_list.append({
                "Nom Publication": articles["prism:publicationName"],
                "Date": articles["prism:coverDisplayDate"],
                "pubmed-id": articles.get("pubmed-id", None),
                "scopus_id": articles["dc:identifier"],
                "doi": articles.get("prism:doi", "")
            })

        return pd.DataFrame(data=data_list)