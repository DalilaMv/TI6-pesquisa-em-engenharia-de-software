import csv
from datetime import datetime
import pandas as pd
import requests
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

CONNECTION_STRING = os.environ["CONNECTION_STRING"]
DB_NAME = os.environ["DB_NAME"]

def get_events(nameWithOwner):
    owner = nameWithOwner.split("/")[0]
    name = nameWithOwner.split("/")[1]

    try:
        client = MongoClient(CONNECTION_STRING)
        db = client[DB_NAME]
    except:
        print("Não foi possível conectar-se ao servidor do MongoDB:")

    collection = db[nameWithOwner]
    page = 1
    per_page = 100
    while True:
        # response = requests.get(f"https://api.github.com/repos/{owner}/{name}/events", params={
        #     "page": page, "per_page": per_page, "include": "user"})
        response = requests.get(f"https://api.github.com/repos/{owner}/{name}/actions/runs", params={
            "page": page, "per_page": per_page, "include": "user"})
        data = response.json()
        
        if not data:
            break

        # events = [event for event in data ]
        # for event in events:
        #     event["created_at"] = datetime.strptime(event["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        try:
            collection.insert_many(data["workflow_runs"])
        except Exception as err:
            print(err)
            breakpoint()
        if 'next' in response.links:
            page += 1
        else:
            break


def main():
    with open("allRepositories.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)  
        for row in reader:
            nameWithOwner = row[0]
            print(f"Obtendo eventos para {nameWithOwner}")
            get_events(nameWithOwner)



main()
