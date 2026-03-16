# python -m unittest migration_mongodb_autotest.py
# python -m unittest -v migration_mongodb_autotest.py
import unittest
import pandas as pd
from read_csv import get_csv, get_stats
#import pymongo
# ****************************************************************************
# ******************* READ CSV ***********************************************
# ***********Lecture de la data du fichier healthcare_dataset.csv  ***********
df_datahcare = get_csv()
print(df_datahcare.head(2))
# ****************************************************************************
# ******************* FONCTION TEST CSV **************************************
# **** quelques fonctions de test de la data healthcare_dataset.csv **********
class scan_Integrite:
    def __init__(self, df_hcare_to_test):
        self.dataframe = df_hcare_to_test
    # Test le nombre de ligne et colonnes de la dataframe (ficher csv) 
    def count_line_col(self):
        # Calcul du nombre de lignes et de colonnes
        count_lines, count_columns = self.dataframe.shape
        print(f"=> Le dataframe comprend {count_lines} lignes et {count_columns} colonnes\n")
        # Affichage du nombre d'occurrences de chaque valeur possible des colonnes catégorielles
        print("\n=> Affichage du nombre d'occurrences de chaque valeur possible des colonnes catégorielles\n")
        print(self.dataframe.info())
        if (count_lines != 54966) or (count_columns != 15):
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
    def count_val_null(self):
        # Calcul le nb de valeurs manquantes par colonne
        fail=False
        for column in self.dataframe.columns:
            numberNull = self.dataframe[column].isnull().sum()
            if (numberNull > 0):
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
            if not((column == "Room Number") or (column == "Age") or (column == "Billing Amount") \
                or (column == "Date of Admission") or (column == "Discharge Date")) \
                and (colType != "str") :
                fail=True
        return fail
# ******************************************************************************************
# ******************* TEST DE LA DATA csv (avec unittest )**********************************
# *** Test unitaire
class Test_dataframeIN(unittest.TestCase):
    def test_line_col(self):
        # Arrange
        a = scan_Integrite(df_datahcare)
        # Act
        outcome = a.count_line_col()
        # Assert
        self.assertFalse(outcome)
    def test_duplicated_line(self):
        # Arrange
        a = scan_Integrite(df_datahcare)
        # Act
        outcome = a.count_duplicated_line()
        # Assert
        self.assertFalse(outcome)
    def test_value_set_null(self):
        # Arrange
        a = scan_Integrite(df_datahcare)
        # Act
        outcome = a.count_val_null()
        # Assert
        self.assertFalse(outcome)
    def test_type_colonne(self):
        # Arrange
        a = scan_Integrite(df_datahcare)
        # Act
        outcome = a.eval_type_colonne()
        # Assert
        self.assertFalse(outcome)
# ******************************************************************************************
# lance les autotests INPUT db (unittest -v test_csv.py)
# ******************************************************************************************
unittest.main(verbosity=2)
