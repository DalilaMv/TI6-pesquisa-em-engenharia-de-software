import requests
import os
from dotenv import load_dotenv


# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém o valor da variável de ambiente "token"
token = os.getenv("ACCESS_TOKEN")

#Nome do proprietário do repositório
owner = "java-native-access"

#Nome do repositório
repo = "jna"

import requests
import json

build_number = '3875801326' # substitua pelo número da build que deseja consultar
url = f'https://api.github.com/repos/{owner}/{repo}/actions/runs/{build_number}/jobs'

headers = {
    'Accept': 'application/vnd.github.v3+json',
    'Authorization': f'token {token}'
}

response = requests.get(url, headers=headers)
data = json.loads(response.text)
print(data)


# Agora você pode iterar sobre os jobs da build e obter informações sobre os steps:
# for job in data['jobs']:
#     print(f'Job ID: {job["id"]}')
#     print(f'Job name: {job["name"]}')
#     print(f'Status: {job["status"]}')
#     print(f'Conclusion: {job["conclusion"]}')
#     print('Steps:')
#     for step in job['steps']:
#         print(f'  - {step["name"]}')
#         print(f'  - {step["status"]}')
#         print(f'  - {step["conclusion"]}')
#         print(f'  - {step["number"]}')
#         print(f'  - {step["started_at"]}')
#         print(f'  - {step["completed_at"]}')
#         print(f'  ----------------------')
