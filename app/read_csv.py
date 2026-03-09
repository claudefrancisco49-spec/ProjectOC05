# python -m unittest migration_mongodb_autotest.py
# python -m unittest -v migration_mongodb_autotest.py
# import unittest
import pandas as pd
# import pymongo
# Définition de quelques fonctions stat
def get_stats(dataframe, line_meaning):
    # Affichage des 2 premières lignes
    dataframe.head(2)
    # Affichage signification d'une ligne
    print(f"=> {line_meaning}\n")
    # Calcul du nombre de lignes et de colonnes
    count_lines, count_columns = dataframe.shape
    print(f"=> Le dataframe comprend {count_lines} lignes et {count_columns} colonnes\n")
    # Calcul du nombre de données 
    duplicated = dataframe.duplicated().sum()
    print(f"=> Le dataframe comprend {duplicated} ligne(s) dupliquée(s)\n")
    # Calcul de la proportion de valeurs manquantes par colonne et suppression si taux de 100%
    for column in dataframe.columns:
        percent = dataframe[column].isnull().sum()*100/count_lines
        if percent == 100.0:
            # Suppression de la colonne car inutilisable
            print(f"=> Suppression de la colonne \"{column}\" car toutes les valeurs sont manquantes\n")
            dataframe.pop(column)
    print(f"=> Nombres de valeurs manquantes\n")
    print(dataframe.isna().sum())
    # Affichage des statistiques descriptives basiques pour les colonnes numériques
    print("=> Affichage des statistiques descriptives basiques pour les colonnes numériques")
    print(dataframe.describe())
    # Affichage du nombre d'occurrences de chaque valeur possible des colonnes catégorielles
    print("\n=> Affichage du nombre d'occurrences de chaque valeur possible des colonnes catégorielles\n")
    print(dataframe.info())
    return dataframe
def get_csv():
    df_datahcare = pd.read_csv('./data/healthcare_dataset.csv',  low_memory=False)
    # Traitement des champs date (type : conversion str to date)
    df_datahcare["Date of Admission"] =pd.to_datetime(df_datahcare["Date of Admission"])
    df_datahcare["Discharge Date"] =pd.to_datetime(df_datahcare["Discharge Date"])
    # Traitement des doublon
    df_datahcare = df_datahcare.drop_duplicates()
    return df_datahcare
    # *****************************************************************
    # **  preparation des documens NoSQL avant import mongodb
    # *****************************************************************
    # documents = df_datahcare.to_dict(orient="records")
    # *****************************************************************
