import pandas as pd
import pymongo
from read_csv import get_patient_csv, get_hospital_csv, get_csv, get_stats
import os
#MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/")
MONGO_URI_P = os.getenv("MONGO_URI_P", "mongodb://admin_hp:pass1234@mongo:27017/")
MONGO_URI_H = os.getenv("MONGO_URI_H", "mongodb://admin_hp:pass1234@mongo:27017/")
#MONGO_URI_H = os.getenv("MONGO_URI_H", "mongodb://user_h:apph1234@mongo:27017/")
DB_NAME_P = os.getenv("DB_NAME_P", "db_pcare_patient")
DB_NAME_H = os.getenv("DB_NAME_H", "db_hcare_hospital")
# DB_NAME = os.getenv("DB_NAME", "db_hcare")
#print('****************************** Authentication ****************************')
#print(MONGO_URI_H)
#print(DB_NAME_H)
# Récupere une dataframe 
df_datahcare = get_csv()
df_patient = get_patient_csv()
df_hospital = get_hospital_csv()
# *** Analyse manuel et traitement des colonnes inutilisables *****
# df_datahcare = get_stats(df_datahcare, "Hospitalisation")
# *****************************************************
# *****************************************************
# documents = df_datahcare.to_dict(orient="records")
documents_p = df_patient.to_dict(orient="records")
documents_h = df_hospital.to_dict(orient="records")
# Creation mongo_db
# client = pymongo.MongoClient(MONGO_URI)
# mydb = client[DB_NAME]
# db_hcare = mydb["hcare"]
# Enregistre tout le csv dans la BDD Mongodb 

# ************************* db et collection patient *********************
client_p = pymongo.MongoClient(MONGO_URI_P)
mydb_p = client_p[DB_NAME_P]
db_patient = mydb_p["patient"]
# ************************* db et collection Hopital *********************
client_h = pymongo.MongoClient(MONGO_URI_H)
mydb_h = client_h[DB_NAME_H]
db_hospital = mydb_h["hospital"]
# *********************** INSERT **********************
print('*** INSERT : csv to db ***')
#result = db_hcare.insert_many(documents)
result_p=db_patient.insert_many(documents_p)
result_h=db_hospital.insert_many(documents_h)
# Create an index on the collection (amméliore les temps de recherche sur la colonne Name)
name_index = db_patient.create_index("Name")
hospital_index = db_hospital.create_index("Hospital")
print('*** done : db updated ! ***')


