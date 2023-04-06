import os
import requests
from dotenv import load_dotenv


# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém o valor da variável de ambiente "token"
token = os.getenv("ACCESS_TOKEN")


headers = {"Authorization": "Bearer " + token}

#Nome do proprietário do repositório
owner = "java-native-access"

#Nome do repositório
repo = "jna"


# ID da build
buildId = 3913589087;


url = f"https://api.github.com/repos/{owner}/{repo}/actions/runs/{buildId}"
response = requests.get(url, headers=headers)
build_data = response.json()


#obter o ID do commit
commit_id = build_data["head_commit"]["id"]

# substitua "OWNER", "REPO" e "commit" pelos valores corretos
url = f"https://api.github.com/repos/{owner}/{repo}/commits/{commit_id}"
response = requests.get(url, headers=headers)
commit_data = response.json()
print(commit_data)
#
#
# commit = commit_data["commit"]
# author = commit["author"]
# files = commit_data["files"]
#
# print(f"Autor commit: {author['name']}")
# print(f"Mensagem commit: {commit['message']}")
#
# total_changes = 0
# total_additions = 0
# total_deletions = 0
# for file in files:
#     total_changes += file['changes']
#     total_additions += file['additions']
#     total_deletions += file['deletions']
#
# print(f"Total de mudanças: {total_changes}")
# print(f"Total de adições: {total_additions}")
# print(f"Total de deleções: {total_deletions}")
#
#
#
#
#
