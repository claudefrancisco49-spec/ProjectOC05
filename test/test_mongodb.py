# python -m unittest migration_mongodb_autotest.py
# python -m unittest -v migration_mongodb_autotest.py
import unittest
import pandas as pd
import pymongo
from read_csv import get_stats
import os
# ********************************************************************************
# ***************** Récupere les variables d'environement ************************
MONGO_URI_P = os.getenv("MONGO_URI_P", "mongodb://admin_hospat:word1234@mongo:27017/")
MONGO_URI_H = os.getenv("MONGO_URI_H", "mongodb://admin_hospat:word1234@mongo:27017/")
DB_NAME_P = os.getenv("DB_NAME_P", "db_patientcare")
DB_NAME_H = os.getenv("DB_NAME_H", "db_hospitalcare")
# *********************************************************************************
# ****************************** READ db Patient **********************************
client_patient = pymongo.MongoClient(MONGO_URI_P)
# READ : Lecture de la BDD Mongodb
mydb_patient = client_patient[DB_NAME_P]
db_patientcare_docs = mydb_patient["patient"]
cursor_patient = db_patientcare_docs.find()
entries_patient = list(cursor_patient)
df_patientdata_Mongo_db = pd.DataFrame(entries_patient)
# *********************************************************************************
# ****************************** READ db Patient **********************************
client_hospital = pymongo.MongoClient(MONGO_URI_H)
# READ : Lecture de la BDD Mongodb
mydb_hospital = client_hospital[DB_NAME_H]
db_hospitalcare_docs = mydb_hospital["hospital"]
cursor_hospital = db_hospitalcare_docs.find()
entries_hospital = list(cursor_hospital)
df_hospitaldata_Mongo_db = pd.DataFrame(entries_hospital)
# *********************************************************************************
# ************ Affichage des dataframes base de données Mongodb *******************
print(df_patientdata_Mongo_db.head(2))
print(df_hospitaldata_Mongo_db.head(2))
# *********************************************************************************
# ***************** fonction de test de la base de données ************************
class scan_Integrite:
    def __init__(self, df_hospitalcare_to_test):
        self.dataframe = df_hospitalcare_to_test
    # Test le nombre de ligne et colonnes de la dataframe patient (Mongodb) 
    def countp_line_col(self):
        # Calcul du nombre de lignes et de colonnes
        count_lines, count_columns = self.dataframe.shape
        print(f"=> Le dataframe comprend {count_lines} lignes et {count_columns} colonnes\n")
        # Affichage du nombre d'occurrences de chaque valeur possible des colonnes catégorielles
        print("\n=> Affichage du nombre d'occurrences de chaque valeur possible des colonnes catégorielles\n")
        print(self.dataframe.info())
        if (count_lines != 54944) or (count_columns != 7):
            return True # fail=True
        return False
    # Test le nombre de ligne et colonnes de la dataframe hospital (Mongodb)     
    def counth_line_col(self):
        # Calcul du nombre de lignes et de colonnes
        count_lines, count_columns = self.dataframe.shape
        print(f"=> Le dataframe comprend {count_lines} lignes et {count_columns} colonnes\n")

        # Affichage du nombre d'occurrences de chaque valeur possible des colonnes catégorielles
        print("\n=> Affichage du nombre d'occurrences de chaque valeur possible des colonnes catégorielles\n")
        print(self.dataframe.info())
        if (count_lines != 54966) or (count_columns != 14):
            return True # fail=True
        return False
     # Test le nombre de ligne doublon de la dataframe
    def count_duplicated_line(self):
        # Calcul du nombre de données 
        duplicated = self.dataframe.duplicated().sum()
        print(f"=> Le dataframe comprend {duplicated} ligne(s) dupliquée(s)\n")
        if duplicated > 0 :
            return True # fail=True
        return False
     # Test le nombre de valeur null > 0 de la dataframe 
    def countp_val_null(self):
        # Calcul le nb de valeurs manquantes par colonne
        fail=False
        for column in self.dataframe.columns:
            numberNull = self.dataframe[column].isnull().sum()
            if numberNull > 0 :
                print(f"=> FAIL : La colonne \"{column}\" à {numberNull} valeurs manquantes\n")
                fail=True
        return fail
     # Test le nombre de valeur null > 0 de la dataframe 
    def counth_val_null(self):
        # Calcul le nb de valeurs manquantes par colonne
        fail=False
        for column in self.dataframe.columns:
            numberNull = self.dataframe[column].isnull().sum()
            if numberNull > 0 :
                print(f"=> FAIL : La colonne \"{column}\" à {numberNull} valeurs manquantes\n")
                fail=True
        return fail
    # Test le type des valeurs de la dataframe 
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
            if (column == "id_p") and (colType != "int64") :
                fail=True
            if (column == "id_h") and (colType != "int64") :
                fail=True
            if not((column == "Room Number") or (column == "Age") or (column == "Billing Amount") \
              or (column == "Date of Admission") or (column == "Discharge Date") or (column == "_id") or (column == "id_h") or (column == "id_p")) \
              and (colType != "str") :
                if (colType != "object") :
                    print(f"=> FAIL : column {column} and coltype \"{colType}\" \n")
                    fail=True
        return fail
# ******************************************************************************************
# ******************* TEST DE LA DATA mongodb (avec unittest )******************************
# Test unitaire
class Test_dataframeOUT(unittest.TestCase):
    def test_patient_line_col(self):
        # Arrange
        a = scan_Integrite(df_patientdata_Mongo_db)
        # Act
        outcome = a.countp_line_col()
        # Assert
        self.assertFalse(outcome)
    def test_hospital_line_col(self):
        # Arrange
        a = scan_Integrite(df_hospitaldata_Mongo_db)
        # Act
        outcome = a.counth_line_col()
        # Assert
        self.assertFalse(outcome)
    def test_patient_duplicated_line(self):
        # Arrange
        a = scan_Integrite(df_patientdata_Mongo_db)
        # Act
        outcome = a.count_duplicated_line()
        # Assert
        self.assertFalse(outcome)
    def test_hospital_duplicated_line(self):
        # Arrange
        a = scan_Integrite(df_hospitaldata_Mongo_db)
        # Act
        outcome = a.count_duplicated_line()
        # Assert
        self.assertFalse(outcome)
    def test_patient_value_set_null(self):
        # Arrange
        a = scan_Integrite(df_patientdata_Mongo_db)
        # Act
        outcome = a.countp_val_null()
        # Assert
        self.assertFalse(outcome)
    def test_hospital_value_set_null(self):
        # Arrange
        a = scan_Integrite(df_hospitaldata_Mongo_db)
        # Act
        outcome = a.counth_val_null()
        # Assert
        self.assertFalse(outcome)
    def test_patient_type_colonne(self):
        # Arrange
        a = scan_Integrite(df_patientdata_Mongo_db)
        # Act
        outcome = a.eval_type_colonne()
        # Assert
        self.assertFalse(outcome)
    def test_hospital_type_colonne(self):
        # Arrange
        a = scan_Integrite(df_hospitaldata_Mongo_db)
        # Act
        outcome = a.eval_type_colonne()
        # Assert
        self.assertFalse(outcome)
# ******************************************************************************************
# lance les autotests OUTPUT db (unittest -v test_csv.py)
# ******************************************************************************************
unittest.main(verbosity=2)
