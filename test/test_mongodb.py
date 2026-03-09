# python -m unittest migration_mongodb_autotest.py
# python -m unittest -v migration_mongodb_autotest.py
import unittest
import pandas as pd
import pymongo
from read_csv import get_stats
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/")
DB_NAME = os.getenv("DB_NAME", "db_hcare")
# *****************************************************
# *********************** READ **********************
# client : pymongo.MongoClient('localhost')
client = pymongo.MongoClient(MONGO_URI)
# READ : Lecture de la BDD Mongodb
# db_hcare_docs = client.hcare_db.hcare
mydb = client[DB_NAME]
db_hcare_docs = mydb["hcare"]
cursor = db_hcare_docs.find()
entries = list(cursor)
df_data_Mongo_db = pd.DataFrame(entries)
# *** Analyse manuel et traitement des colonnes inutilisables *****
# get_stats(df_data_Mongo_db, "Hospitalisation")
print(df_data_Mongo_db.head(2))
# A tester
class scan_Integrite:
    def __init__(self, df_hcare_to_test):
        self.dataframe = df_hcare_to_test
    def count_line_col(self):
        # Calcul du nombre de lignes et de colonnes
        count_lines, count_columns = self.dataframe.shape
        print(f"=> Le dataframe comprend {count_lines} lignes et {count_columns} colonnes\n")
        # Affichage du nombre d'occurrences de chaque valeur possible des colonnes catégorielles
        print("\n=> Affichage du nombre d'occurrences de chaque valeur possible des colonnes catégorielles\n")
        print(self.dataframe.info())
        if (count_lines != 54966) or (count_columns != 16):
            return True # fail=True
        return False
    def count_duplicated_line(self):
        # Calcul du nombre de données 
        duplicated = self.dataframe.duplicated().sum()
        print(f"=> Le dataframe comprend {duplicated} ligne(s) dupliquée(s)\n")
        if duplicated > 0 :
            return True # fail=True
        return False
    def count_val_null(self):
        # Calcul le nb de valeurs manquantes par colonne
        fail=False
        for column in self.dataframe.columns:
            numberNull = self.dataframe[column].isnull().sum()
            if numberNull > 0 :
                print(f"=> FAIL : La colonne \"{column}\" à {numberNull} valeurs manquantes\n")
                fail=True
        return fail
    def eval_type_colonne(self):
        # Calcul le nb de valeurs manquantes par colonne
        fail=False
        for column in self.dataframe.columns:
            colType = self.dataframe[column].dtypes
            if (column == "Age") and (colType != "int64") :
                fail=True
            if (column == "Room Number") and (colType != "int64") :
                fail=True
            if (column == "Billing Amount") and (colType != "float64") :
                fail=True  
            if (column == "Date of Admission") and (colType != "datetime64[us]") :
                fail=True  
            if (column == "Discharge Date") and (colType != "datetime64[us]") :
                fail=True              
            if not((column == "Room Number") or (column == "Age") or (column == "Billing Amount") \
                or (column == "Date of Admission") or (column == "Discharge Date") or (column == "_id")) \
                and (colType != "str") :
                fail=True
        return fail
# Test unitaire
class Test_dataframeOUT(unittest.TestCase):
    def test_line_col(self):
        # Arrange
        a = scan_Integrite(df_data_Mongo_db)
        # Act
        outcome = a.count_line_col()
        # Assert
        self.assertFalse(outcome)
    def test_duplicated_line(self):
        # Arrange
        a = scan_Integrite(df_data_Mongo_db)
        # Act
        outcome = a.count_duplicated_line()
        # Assert
        self.assertFalse(outcome)
    def test_value_set_null(self):
        # Arrange
        a = scan_Integrite(df_data_Mongo_db)
        # Act
        outcome = a.count_val_null()
        # Assert
        self.assertFalse(outcome)
    def test_type_colonne(self):
        # Arrange
        a = scan_Integrite(df_data_Mongo_db)
        # Act
        outcome = a.eval_type_colonne()
        # Assert
        self.assertFalse(outcome)

#if __name__ == "__main_":
#unittest.main()
unittest.main(verbosity=2)
