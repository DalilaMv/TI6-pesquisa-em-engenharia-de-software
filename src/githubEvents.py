import requests
import os
from dotenv import load_dotenv


# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém o valor da variável de ambiente "token"
token = os.getenv("ACCESS_TOKEN")

#Cria uma sessão com a chave de acesso
session = requests.Session()
session.auth = ("TOKEN", token)

#Nome do proprietário do repositório
owner = "java-native-access"

#Nome do repositório
repo = "jna"

#Faz uma requisição para obter informações sobre as builds
response = session.get(f"https://api.github.com/repos/{owner}/{repo}/actions/runs", params={"include": "user","event__in": "pull_request, push"})
data = response.json()
#print(data)

for run in data["workflow_runs"]:
    print(f"Nome: {run['name']}")
    print(f"Evento: {run['event']}")
    print(f"ID do build: {run['id']}")
    print(f"Status: {run['status']}")
    print(f"Conclusão: {run['conclusion']}")
    print(f"Data de início: {run['created_at']}")
    print(f"Data de término: {run['updated_at']}")
    print(f"Usuário que iniciou: {run['actor']['login']}")
    print(f"Tipo do usuário: {run['actor']['type']}")
    print(f"É usuário administrador: {run['actor']['site_admin']}")
    print(f"Pull Requests: {len(run['pull_requests'])}")
    print(f"ID commit: {run['head_commit']['id']}")
    print(f"Message commit: {run['head_commit']['message']}")
    print(f"Timestamp commit: {run['head_commit']['timestamp']}")
    print("---------------------")