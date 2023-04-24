import csv
from datetime import datetime
import pandas as pd
import requests
import json


def get_events(nameWithOwner, since_date, until_date):
    owner = nameWithOwner.split("/")[0]
    name = nameWithOwner.split("/")[1]

    # define a data de início e fim do intervalo de tempo
    since_d = datetime.strptime(since_date, "%Y-%m-%d %H:%M:%S")
    until_d = datetime.strptime(until_date, "%Y-%m-%d %H:%M:%S")

    # faz uma requisição para obter informações sobre os eventos

    events = []
    page = 1
    per_page = 100
    while True:
        response = requests.get(f"https://api.github.com/repos/{owner}/{name}/events", params={
            "page": page, "per_page": per_page, "include": "user"})
        data = response.json()

        if not data:
            break
        for event in data:
            event_date = datetime.strptime(
                event['created_at'], '%Y-%m-%dT%H:%M:%SZ')
            if event_date >= since_d and event_date < until_d:
                events.append(event)

        with open('teste.csv', mode='a', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            for item in events:
                row = [item['id'], json.dumps(item, indent=2)]
                writer.writerow(row)

        print(response.links)

        # verifica se há mais páginas e atualiza o contador da página
        if 'next' in response.links:
            page += 1
        else:
            break

    return data


def main():
    file_name = "csv2_intervalos.csv"
    df = pd.read_csv(file_name)
    get_events("jquery/jquery", "2023-04-04 22:09:54", "2023-04-04 22:12:43")
    # for index, row in df.iterrows():
    #     breakpoint()
    #     get_events(row[0], row[2], row[4])
    #     print(index)
    return


main()
