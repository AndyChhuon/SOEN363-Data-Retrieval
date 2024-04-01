import pandas as pd
import mysql.connector
import json
from dotenv import load_dotenv
import os

load_dotenv()
PASSWORD = os.getenv('mysql_password')
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password=PASSWORD,
  database="soen363-project",
  use_unicode=True
)

mycursor = mydb.cursor()

# read repos csv file
reposDf = pd.read_csv('populate-csv/language.csv')


for index, row in reposDf.iterrows():
    sql = "INSERT INTO Language (lid, language) VALUES (%s, %s)"
    val = (row['lid'], row['language'])
    mycursor.execute(sql, val)

    if index % 1000 == 0:
        print(index)

mydb.commit()
