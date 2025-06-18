import requests

import pandas as pd
import streamlit as st

def base_link(prefix: str = None, query:str = None):
    """
    Cette fonction permet de rechercher des informations de base telles que l'auteur, une recherche simple, etc.
    
    Args : 
        prefix(str) : nom du domaine
        query(str) : information à rechercher, paramètre pouvant être utilisé. 
    """
    # A documenter !!!!!!
    root = f"https://api.archives-ouvertes.fr/{"ref/" + prefix 
                                            if prefix in ["anrproject","doctype","instance","metadata","structure","metadatalist","journal","domain","europeanproject","author"] 
                                            else "search/"}"
    endpoint = f"?q={query}&wt=json"
    return requests.get(root+endpoint).json()

def id_author(lastName:str, firstName:str):
    """
    Cette fonction permet de rechercher les identifiants des auteurs que vous souhaitez.
    
    Args :
        lastName(str) : Nom de l'auteur
        firstName(str) : prénom de l'auteur
    """
    if not lastName:
        return "Erreur Recherche HAL : Veuillez renseigner le nom de famille."
    if not firstName:
        return "Erreur Recherche HAL : Veuillez renseigner le prénom."
    
    req = base_link(prefix = "author", query= f"{lastName} {firstName}")

    id_auth = []
    docs = req["response"]["docs"]
    numFound = req["response"]["numFound"]
        
    if int(numFound) == 0:
        return "Erreur Recherche HAL : Nous n'avons pas trouvé de données\nVérifiez les informations renseignées."
    
    for doc in docs:
        docid = doc["docid"]
        if docid.split("-")[1] not in id_auth:
            id_auth.append(docid) # .split("-")[1]
    return id_auth

def get_hal_researcher_data(lastName:str,firstName:str):
    """
    Cette fonction permet de rechercher les identifiants des auteurs que vous souhaitez.
    
    Args :
        lastName(str) : Nom de l'auteur
        firstName(str) : prénom de l'auteur
    """

    # authIdForm_i:158428 -> Marc Humbert -> 449
    ids = id_author(lastName = lastName, firstName=firstName)
    if isinstance(ids, list):
        data_hal = []
        for id in ids:
            req = base_link(query=f"authIdFormPerson_s:{id}&fl=title_s,doiId_s,authIdHal_s,pubmedId_id,journalTitle_s,journalPublisher_s,publicationDate_s,authLastNameFirstName_s&start=0&rows=1000")
            docs = req["response"]["docs"]
            for doc in docs:
                title_s = doc["title_s"][0]
                journalTitle_s = doc.get("journalTitle_s", None)
                journalPublisher_s = doc.get("journalPublisher_s", None)
                publicationDate_s = doc["publicationDate_s"]
                doiId_s = doc.get("doiId_s", None)
                pubmedId_id = doc.get("pubmedId_id", None)
                authLastNameFirstName_s = doc.get("authLastNameFirstName_s", None)
                data_hal.append({
                    "Titre_journal": journalTitle_s,
                    "Author Full Names" : authLastNameFirstName_s,
                    "Title_article": title_s,
                    "journalPublisher_s" : journalPublisher_s,
                    "publicationDate_s" : publicationDate_s,
                    "DOI": doiId_s,
                    "pubmedId": pubmedId_id
                })
    return pd.DataFrame(data_hal)