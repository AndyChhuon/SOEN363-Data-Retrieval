import pandas as pd
import mysql.connector
import json
from dotenv import load_dotenv
import os
import numpy as np

load_dotenv()
PASSWORD = os.getenv('mysql_password')
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password=PASSWORD,
  database="soen363-project",
)

mycursor = mydb.cursor()

# read repos csv file
reposDf = pd.read_csv('populate-csv/demand_language.csv')

with open('populate-csv/validJid.json', 'r') as f:
    validJids = json.load(f)

#drop duplicates
reposDf = reposDf.drop_duplicates()

for index, row in reposDf.iterrows():
    jid = row['jid'].item()
    
    if str(jid) not in validJids:
        print("Invalid jid" + str(jid))
        continue
    lid = row['lid'].item()
    sql = f"INSERT INTO DemandLanguage VALUES ({jid}, {lid})"
    val = (jid, lid)
    mycursor.execute(sql)

    if index % 1000 == 0:
        print(index)

mydb.commit()
