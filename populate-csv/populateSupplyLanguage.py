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
reposDf = pd.read_csv('populate-csv/supply_language.csv')

#drop duplicates
reposDf = reposDf.drop_duplicates()

for index, row in reposDf.iterrows():
    rid = row['rid'].item()
    lid = row['lid'].item()
    sql = f"INSERT INTO SupplyLanguage VALUES ({rid}, {lid})"
    val = (rid, lid)
    mycursor.execute(sql)

    if index % 1000 == 0:
        print(index)

mydb.commit()
