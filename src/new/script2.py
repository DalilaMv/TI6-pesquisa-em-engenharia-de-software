


import requests
import csv
import tempfile
import os
from dotenv import load_dotenv

load_dotenv()

token = os.environ["token"]
repositories = []



def get_builds(nameWithOwner):
    
    # define as variáveis para a autenticação e a URL do repositório
    owner = nameWithOwner.split("/")[0]
    name = nameWithOwner.split("/")[1]

    # define a URL da API do GitHub para obter as informações de builds
    url = f'https://api.github.com/repos/{owner}/{name}/actions/runs'
    
    # define os parâmetros da requisição para a API
    # params = {
    #     'status': 'all',  # inclui builds com status de sucesso e falha
    #     'per_page': 100  # define o número máximo de resultados por página
    # }

    # define o cabeçalho da requisição com o token de acesso
    headers = {
        'Authorization': f'Token {token}'
    }

    # faz a requisição GET para obter as informações de builds
    response = requests.get(url, headers=headers)

    # obtém os dados JSON da resposta
    data = response.json()

    # ordena as builds da mais antiga para a mais recente
    runs = sorted(data['workflow_runs'], key=lambda r: r['created_at'])
    breakpoint()
    # abre um arquivo CSV temporário para escrever os dados
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as csv_file:
        writer = csv.writer(csv_file, delimiter=';')

        # escreve o cabeçalho do arquivo CSV
        writer.writerow(['idBuild', 'status da build', 'data/hora da build'])

        # escreve os dados de cada build no arquivo CSV
        for run in runs:
            writer.writerow([run['id'], run['conclusion'], run['created_at']])

    # imprime o nome do arquivo CSV temporário gerado
    print(f'O arquivo CSV temporário foi salvo em: {csv_file.name}')

  

    return

def main():
    nameWithOwner = "jquery/jquery"  # temporario
    get_builds(nameWithOwner)
    return
    
main()