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
reposDf = pd.read_csv('populate-csv/job_final.csv')
validJids = []

for index, row in reposDf.iterrows():
    sql = "INSERT INTO Job (jid, job_title, job_description) VALUES (%s, %s, %s)"
    val = (row['jid'], row['job_title'], row['job_description'])
    try:
        mycursor.execute(sql, val)
        validJids.append(row['jid'])
    except:
        print("Error")
        continue

    if index % 1000 == 0:
        print(index)

with open('populate-csv/validJid.json', 'w') as f:
    json.dump(validJids, f)
mydb.commit()
