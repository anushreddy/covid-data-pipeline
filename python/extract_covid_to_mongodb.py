# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 14:13:34 2020

@author: Anush
"""

# pip install pymongo[srv]
import requests
from pymongo import MongoClient
import os


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

# function to connect to mongo db    
def connect_db(db_creds):
    client = MongoClient(db_creds[0])
    db = client.get_database(db_creds[1])
    records = db.covid_collection
    if records is None:
        print("There is no data in the Database!")
    else:
        return records 

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

# function to insert dictionary items to mongo db collection
def export_to_mongodb(dict_data):
    for key in dict_data['data']['covid19Stats']:
    #    print(key + ":", dict_data['data']['covid19Stats'][0][key])
        records.insert_one(key)
    
db_creds = read_db_creds("database.txt")
records = connect_db(db_creds)
api_data = read_api_creds("api_credentials.txt")
dict_data = call_api(api_data)
export_to_mongodb(dict_data)

