# Research Visibility Checker V2

## Présentation

**Research Visibility Checker** est une application web développée avec Streamlit qui permet aux chercheurs d'analyser et d'optimiser leur visibilité académique en comparant leurs publications à travers les principales bases de données scientifiques.

### Objectif

L'application vise à identifier rapidement les recoupements entre différentes bases de données scientifiques et à s'assurer que toutes les publications d'un chercheur sont correctement référencées partout. Cela permet de :

- **Détecter les publications manquantes** dans certaines bases de données (Web Of Science)
- **Identifier les doublons** et incohérences
- **Optimiser la visibilité** académique du chercheur
- **Générer des rapports** détaillés de comparaison

## Bases de données supportées

L'application intègre les principales bases de données scientifiques :

- **HAL** (Hyper Articles en Ligne) - Archive ouverte française
- **ORCID** - Identifiant unique pour les chercheurs
- **Scopus** - Base de données bibliographique d'Elsevier
- **Web of Science** - Base de données bibliographique de Clarivate

## Fonctionnalités principales

### 1. Récupération automatique des données
- **HAL** : Récupération automatique via l'API HAL
- **ORCID** : Récupération via l'API ORCID publique
- **Scopus** : Récupération via l'API Scopus (nécessite un identifiant Scopus)
- **Web of Science** : Import manuel de fichiers Excel exportés

### 2. Analyse et comparaison
- **Recoupement automatique** entre les bases de données
- **Détection des publications manquantes**
- **Identification des doublons** et incohérences
- **Calcul des taux de recoupement**

### 3. Visualisation et export
- **Graphiques interactifs** pour visualiser les recoupements
- **Tableaux de comparaison** détaillés
- **Export Excel** des résultats d'analyse
- **Rapports personnalisés** par chercheur

## 🛠️ Installation et utilisation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation locale

1. **Cloner le repository**
```bash
git clone https://github.com/votre-username/Research-Visbility-Checker-V2.git
cd Research-Visbility-Checker-V2
```

2. **Lancer l'application**
```bash
streamlit run main.py
```

L'application sera accessible à l'adresse : `http://localhost:8501`

## Guide d'utilisation

### Étape 1 : Préparation des données

#### Pour Web of Science :
1. Aller sur le profil du chercheur dans Web of Science
2. Cliquer sur le nombre de publications pour afficher tous les articles
3. Cliquer sur "Exporter" puis sélectionner "Excel"
4. Configurer l'export avec les options recommandées

#### Pour Scopus :
1. Aller sur le profil Scopus du chercheur
2. Copier l'identifiant Scopus (visible dans l'URL)

#### Pour ORCID :
1. Aller sur le profil ORCID du chercheur
2. Copier l'URL complète du profil

### Étape 2 : Utilisation de l'application

1. **Saisir les informations du chercheur** :
   - Nom et prénom
   - Identifiant ORCID
   - Identifiant Scopus

2. **Ajouter les fichiers** :
   - Fichier Excel Web of Science (optionnel)
   - Autres fichiers de publications si nécessaire (Scopus)

3. **Lancer l'analyse** :
   - Les données sont automatiquement récupérées depuis HAL, ORCID et Scopus
   - L'application effectue les comparaisons et génère les rapports de manière autonome.

4. **Consulter les résultats** :
   - Visualiser les recoupements via des graphiques
   - Examiner les tableaux de comparaison détaillés
   - Exporter les résultats en Excel

## Architecture du projet

```
Research-Visbility-Checker-V2/
├── main.py                 # Point d'entrée de l'application Streamlit
├── utilitaire.py          # Fonctions utilitaires
├── fonction/              # Modules de traitement des données
│   ├── _hal.py           # Intégration avec HAL
│   ├── _orcid.py         # Intégration avec ORCID
│   ├── _scopus.py        # Intégration avec Scopus
│   ├── _wos.py           # Traitement des données Web of Science
│   ├── _tx_recoupement.py # Logique de comparaison et recoupement
│   └── _misc.py          # Fonctions utilitaires diverses
├── pages/                 # Pages de l'interface utilisateur
│   ├── 0_tutorial.py     # Page de tutoriel
│   ├── 1_st_choix_analyse.py # Page de sélection d'analyse
│   ├── 2_st_donnee.py    # Page de saisie des données
│   ├── 3_st_show_donnee.py # Page d'affichage des données
│   └── 4_st_comparaison.py # Page de comparaison
├── md/                    # Documentation en Markdown
├── img/                   # Images pour le tutoriel
├── ressources/            # Fichiers de données d'exemple
└── requirements.txt       # Dépendances Python
```

## 🔧 Technologies utilisées

- **Streamlit** : Interface utilisateur web
- **Pandas** : Manipulation et analyse des données
- **Requests** : Appels API vers les bases de données
- **OpenPyXL** : Lecture/écriture de fichiers Excel
- **Matplotlib** : Graphiques supplémentaires
- **OS** : Gestion des variables d'environnement et des chemins
- **re** : Expressions régulières pour le traitement des chaînes
- **IO** : Gestion des flux d'entrée/sortie
- **Pathlib** : Manipulation des chemins de fichiers

## 📊 Fonctionnalités avancées

### Analyse de recoupement
- **Taux de recoupement** entre chaque paire de bases de données
- **Identification des publications uniques** à chaque base
- **Détection des incohérences** dans les métadonnées

### Suggestions d'amélioration
- **Recommandations** pour améliorer la visibilité
- **Actions suggérées** pour corriger les incohérences
- **Priorisation** des actions à entreprendre

### Export et reporting
- **Rapports Excel** détaillés avec plusieurs onglets
- **Graphiques exportables** pour les présentations
- **Données structurées** pour analyses complémentaires

## 📝 Licence

Ce projet est sous licence MIT.
---
Avec Docker :
Si on a modifié le code, il faut forcer forcer la compilation : 
sudo docker compose up --force-recreate --build

**Développé pour optimiser la visibilité académique des chercheurs** 🎓 
