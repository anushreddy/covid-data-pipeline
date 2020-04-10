# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 15:24:17 2020

@author: Anush
"""

import requests
import mysql.connector
import os
import csv

# function to read database credentials from a file
def read_db_creds(fileName):
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(THIS_FOLDER, fileName)
    with open (file_path, "r") as db_file:
        data = db_file.readlines()
        db_creds = []
        for elem in data:
            db_creds.extend(elem.rstrip('\n').split('\n'))
    if db_creds is None:
        print("There is no data in the file. Please check the file!")
    else:
        db_file.close()
        return db_creds

# function to connect to mysql db    
def connect_db(db_creds):
    mydb = mysql.connector.connect(
      host="localhost",
      user="anush",
      passwd="anush",
      database="covid_db"
    )
    
    return mydb 

# read file to access api credentials
def read_api_creds(fileName):
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(THIS_FOLDER, fileName)
    with open (file_path, "r") as myfile:
        data = myfile.readlines()
        ref_data = []
        for elem in data:
            ref_data.extend(elem.rstrip('\n').split('\n'))
    if ref_data is None:
        print("There is no data in the file. Please check the file!")
    else:
        myfile.close()
        return ref_data
    
# function to call the api and convert response json to python dictionary    
def call_api(api_data):
    url = "https://covid-19-coronavirus-statistics.p.rapidapi.com/v1/stats"

    querystring = {"country":"US"}
    
    headers = {
        'x-rapidapi-host': api_data[0],
        'x-rapidapi-key': api_data[1]
        }
    
    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
        response.raise_for_status()
        dict_data = response.json()
        return dict_data
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err) 

# function to insert python dictionaries to mysql database  
def export_to_mysql(dict_data, mydb):
    for mydict in dict_data['data']['covid19Stats']:
        columns = ', '.join("`" + x + "`" for x in mydict.keys())
        values = ', '.join("'" + str(x).replace("'", "''") + "'" for x in mydict.values())
        sql = "INSERT INTO %s ( %s ) VALUES ( %s );" % ('covid_stats', columns, values)
        mycursor = mydb.cursor()
        mycursor.execute(sql)
    try:
        mydb.commit() 
        print("Success: Exported to MySQL!")
    except:
        print("Error: Unable to Export")
#    print(mycursor.rowcount, "was inserted.")

def export_to_csv(dict_data):
    csv_file = "covid_data.csv"
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, dict_data['data']['covid19Stats'][0].keys())
            writer.writeheader()
            for data in dict_data['data']['covid19Stats']:
                writer.writerow(data)
        print("Success: Exported to CSV file!")
    except IOError:
        print("Error: Unable to Export. I/O Error")
        
db_creds = read_db_creds("database.txt")
mydb = connect_db(db_creds)
api_data = read_api_creds("api_credentials.txt")
dict_data = call_api(api_data)
#exporting data to mysql and csv
export_to_mysql(dict_data, mydb)
export_to_csv(dict_data)