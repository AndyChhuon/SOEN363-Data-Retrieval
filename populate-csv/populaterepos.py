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
reposDf = pd.read_csv('populate-csv/repos.csv')


for index, row in reposDf.iterrows():
    sql = "INSERT INTO Repository (rid, name, numIssues, numWatchers) VALUES (%s, %s, %s, %s)"
    val = (row['id'], row['name'], row['numIssues'], row['numWatchers'])
    mycursor.execute(sql, val)

    if index % 1000 == 0:
        print(index)

mydb.commit()
