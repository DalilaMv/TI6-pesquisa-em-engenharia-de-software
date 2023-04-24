
from datetime import datetime
import requests
import csv
import tempfile
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

token = os.environ["token"]
repositories = []


def get_time_diff(start_time, end_time):
    diff_seconds = (end_time - start_time).total_seconds()
    diff_hours, diff_minutes = divmod(diff_seconds, 3600)
    diff_minutes //= 60
    return "{:.0f}h{:02.0f}m".format(diff_hours, diff_minutes)

def get_build_fix_efficiency(nameWithOwner, linhas):
    num_fixed_instantly = 0
    num_build_failure = 0
    previous_row = None
    
    for i, linha in enumerate(linhas):
        if linha[1] == "failure":
            num_build_failure +=1 
            next_row = linhas[i+1]
            if next_row[1] == "success" and previous_row[1] == "success": 
                num_fixed_instantly += 1
        previous_row = linha

    num_not_fixed_instantly = num_build_failure - num_fixed_instantly

    row_data = [nameWithOwner, num_build_failure, num_fixed_instantly,num_not_fixed_instantly]
    with open('csv3_build_efficiency.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(row_data)
            
    return

def get_intervalos(nameWithOwner, reader):
    
    failed_id = None
    failed_time = None 
    
    for row in reader:  
        # 0 - id, 1 - status, 2 - data/hora
        if row[1] == "failure" and failed_id == None:
            failed_id = row[0]
            failed_time = datetime.strptime(
                        row[2], '%Y-%m-%dT%H:%M:%SZ')
        if row[1] == "success" and failed_id != None:
            success_id = row[0]
            success_time = datetime.strptime(
                        row[2], '%Y-%m-%dT%H:%M:%SZ')
            time_diff =  get_time_diff(failed_time, success_time)
            row_data = [nameWithOwner, failed_id, success_id, time_diff]
            with open('csv2_intervalos.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(row_data)
            failed_id = None
            failed_time = None

    return

def get_builds_info(nameWithOwner, file_path):
    
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        next(reader)
        linhas = []
        for linha in reader:
            linhas.append(linha)
        get_intervalos(nameWithOwner, reader)
        get_build_fix_efficiency(nameWithOwner, linhas)
    return

def get_builds(nameWithOwner):
    
    # define as variáveis para a autenticação e a URL do repositório
    owner = nameWithOwner.split("/")[0]
    name = nameWithOwner.split("/")[1]

    # define a URL da API do GitHub para obter as informações de builds
    url = f'https://api.github.com/repos/{owner}/{name}/actions/runs'

    # define o cabeçalho da requisição com o token de acesso
    headers = {
        'Authorization': f'Token {token}'
    }
    
    page_number = 1
    # define os parâmetros da requisição para a API

    params = {
        'page': page_number,
        'per_page': 100  # define o número máximo de resultados por página
    }

    # abre um arquivo CSV temporário para escrever os dados
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as csv_file:
        writer = csv.writer(csv_file, delimiter=';')

        # escreve o cabeçalho do arquivo CSV
        writer.writerow(['idBuild', 'status da build', 'data/hora da build'])

        # faz a primeira requisição GET para obter as informações de builds
        response = requests.get(url, params=params, headers=headers)

        # obtém os dados JSON da resposta
        data = response.json()

        # adiciona os resultados da primeira página à lista de builds
        runs = data['workflow_runs']

        # enquanto houver mais páginas de resultados, faz uma nova requisição
        # com o valor do cursor da próxima página e adiciona os resultados à lista de builds
        while 'next' in response.links:
            print(response.links)
            next_url = response.links['next']['url']
            response = requests.get(next_url, headers=headers)
            data = response.json()
            runs += data['workflow_runs']

        # ordena as builds da mais antiga para a mais recente
        runs = sorted(runs, key=lambda r: r['created_at'])

        # escreve os dados de cada build no arquivo CSV
        for run in runs:
            writer.writerow([run['id'], run['conclusion'], run['created_at']])
            
    # imprime o nome do arquivo CSV temporário gerado
    print(f'O arquivo CSV temporário foi salvo em: {csv_file.name}')

    return csv_file.name

def main():
    nameWithOwner = "jquery/jquery"  # temporario
    # vai ter um for futuramente... 
    file_path = get_builds(nameWithOwner)
    get_builds_info(nameWithOwner, file_path)
    return
    
main()