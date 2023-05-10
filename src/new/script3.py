import csv
from datetime import datetime
import pandas as pd
import requests
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import json

load_dotenv()

CONNECTION_STRING = os.environ["CONNECTION_STRING"]
DB_NAME = os.environ["DB_NAME"]


def get_events(nameWithOwner, since_date, until_date, failed_id):
    owner = nameWithOwner.split("/")[0]
    name = nameWithOwner.split("/")[1]

    try:
        client = MongoClient(CONNECTION_STRING)
        db = client[DB_NAME]
    except:
        print("Não foi possível conectar-se ao servidor do MongoDB:")

    # define a data de início e fim do intervalo de tempo
    since_d = datetime.strptime(since_date, "%Y-%m-%d %H:%M:%S")
    until_d = datetime.strptime(until_date, "%Y-%m-%d %H:%M:%S")

    # faz uma requisição para obter informações sobre os eventos

    events = []

    collection = db[nameWithOwner]
    page = 1
    per_page = 100
    while True:
        response = requests.get(f"https://api.github.com/repos/{owner}/{name}/actions/runs", params={
            "created": "2021-09-17T16:18:48Z..2021-09-17T16:23:44Z", "page": page, "per_page": per_page, "include": "user"})
        data = response.json()

        with open('arquivoteste.json', 'w') as arquivo:
            json.dump(data, arquivo)

        if not data:
            break
        for event in data["workflow_runs"]:
            event_date = datetime.strptime(
                event['created_at'], '%Y-%m-%dT%H:%M:%SZ')
            if event_date >= since_d and event_date < until_d:
                events.append(event)

        with open('teste.csv', mode='a', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            for item in events:
                row = [failed_id, json.dumps(item, indent=2)]
                writer.writerow(row)

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
    file_name = "csv2_intervalos.csv"
    df = pd.read_csv(file_name)
    get_events("jquery/jquery", "2021-09-17 16:18:48",
               "2021-09-17 16:23:44", "1246204751")
    # for index, row in df.iterrows():
    #     get_events(row[0], row[2], row[4])
    #     print(index)
    # return


main()
