import pandas as pd
import pymongo
from read_csv import get_csv, get_stats
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/")
DB_NAME = os.getenv("DB_NAME", "db_hcare")
# print(MONGO_URI)
# Récupere une dataframe 
df_datahcare = get_csv()
# *** Analyse manuel et traitement des colonnes inutilisables *****
# df_datahcare = get_stats(df_datahcare, "Hospitalisation")
# *****************************************************
# *****************************************************
documents = df_datahcare.to_dict(orient="records")
# Creation mongo_db
client = pymongo.MongoClient(MONGO_URI)
mydb = client[DB_NAME]
db_hcare = mydb["hcare"]
# Enregistre tout le csv dans la BDD Mongodb 
# *********************** INSERT **********************
print('*** INSERT : csv to db ***')
result = db_hcare.insert_many(documents)
#print(result.inserted_ids[0])
# Create an index on the collection (amméliore les temps de recherche sur la colonne Name)
name_index = db_hcare.create_index("Name")
print('*** done : db updated ! ***')

