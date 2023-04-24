import csv
from datetime import datetime, timedelta
import pandas as pd
import requests




def get_events(nameWithOwner, since_date, until_date):
    owner = nameWithOwner.split("/")[0]
    name = nameWithOwner.split("/")[1]
    
    # define a data de início e fim do intervalo de tempo
    since_d = datetime.strptime(since_date,"%Y-%m-%d %H:%M:%S")
    until_d = datetime.strptime(until_date,"%Y-%m-%d %H:%M:%S")
    
    
    # faz uma requisição para obter informações sobre os eventos
    page = 1
    per_page = 100
    while True:
        response = requests.get(f"https://api.github.com/repos/{owner}/{name}/events", params={"since": since_d, "until": until_d,"page": page, "per_page": per_page, "include": "user","event__in": "pull_request, push"})
        data = response.json()
        
        with open('teste.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)
        return data

def main():
    file_name = "csv2_intervalos.csv"
    df = pd.read_csv(file_name)
    get_events("jquery/jquery", "2021-11-30 22:40:21","2021-11-30 22:48:03")
    # for index,row in df.iterrows():
    #     # jquery/jquery,1523216424,2021-11-30 22:40:21,1523238728,2021-11-30 22:48:03,0h07m
    #     get_events(row["nameWithOwner"],row["failed_time"],row["success_time"])
    return
    
main()