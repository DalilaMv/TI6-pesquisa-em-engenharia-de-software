
from datetime import datetime
import random
from time import sleep
import requests
import csv
import tempfile
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

tokens = [os.environ["newToken1"], os.environ["newToken2"]]
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
    num_total_builds = 0
    for i, linha in enumerate(linhas):
        num_total_builds += 1
        if linha[1] == "failure":
            num_build_failure += 1
            if i+1 < len(linhas):
                next_row = linhas[i+1]
                if i == 0 and next_row[1] == "success" or next_row[1] == "success" and previous_row[1] == "success":
                    num_fixed_instantly += 1
        previous_row = linha

    num_not_fixed_instantly = num_build_failure - num_fixed_instantly

    row_data = [nameWithOwner, num_total_builds, num_build_failure,
                num_fixed_instantly, num_not_fixed_instantly]
    with open('csv3_build_efficiency.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(row_data)

    return


def get_intervalos(nameWithOwner, linhas):

    failed_id = None
    failed_time = None

    for i, linha in enumerate(linhas):
        # 0 - id, 1 - status, 2 - data/hora
        if linha[1] == "failure" and failed_id == None:
            failed_id = linha[0]
            userIdFalha = linha[3]
            failed_time = datetime.strptime(
                linha[2], '%Y-%m-%dT%H:%M:%SZ')
        if linha[1] == "success" and failed_id != None:
            success_id = linha[0]
            userIdSucesso = linha[3]
            is_same_user = False
            if userIdFalha == userIdSucesso:
                is_same_user = True
            success_time = datetime.strptime(
                linha[2], '%Y-%m-%dT%H:%M:%SZ')
            time_diff = get_time_diff(failed_time, success_time)
            row_data = [nameWithOwner, failed_id, failed_time,
                        success_id, success_time, time_diff, is_same_user]
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
        get_intervalos(nameWithOwner, linhas)
        get_build_fix_efficiency(nameWithOwner, linhas)
    return


def get_builds(nameWithOwner):
    token = random.choice(tokens)

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
        writer = csv.writer(csv_file, delimiter=';',
                            lineterminator='\n')

        # escreve o cabeçalho do arquivo CSV
        writer.writerow(['idBuild', 'status da build',
                        'data/hora da build', 'userId'])

        sleep(1.0)
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
            token = random.choice(tokens)

        # ordena as builds da mais antiga para a mais recente
        runs = sorted(runs, key=lambda r: r['created_at'])

        # escreve os dados de cada build no arquivo CSV
        for run in runs:
            writer.writerow([run['id'], run['conclusion'],
                            run['created_at'], run['actor']['id']])

    # imprime o nome do arquivo CSV temporário gerado
    print(f'O arquivo CSV temporário foi salvo em: {csv_file.name}')

    return csv_file.name


def main():

    with open("./repos_new_list.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            nameWithOwner = row[0]
            file_path = get_builds(nameWithOwner)
            get_builds_info(nameWithOwner, file_path)

    # with open("./repos_new_list.csv", "r") as f:
    #     reader = csv.reader(f)
    #     next(reader)

    #     token = random.choice(tokens)
    #     headers = {
    #         'Authorization': f'Token {token}'
    #     }
    #     for row in reader:
    #         nameWithOwner = row[0]
    #         owner = nameWithOwner.split("/")[0]
    #         name = nameWithOwner.split("/")[1]
    #         url = f'https://api.github.com/repos/{owner}/{name}/actions/runs'
    #         response = requests.get(url, headers=headers)
    #         data = response.json()
    #         numBuilds = data['total_count']
    #         with open('num_builds_temp.csv', mode='a', newline='') as file:
    #             writer = csv.writer(file)
    #             writer.writerow([nameWithOwner, numBuilds])
    #         token = random.choice(tokens)

    return


main()
