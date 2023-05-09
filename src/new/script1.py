import csv
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

token = os.environ["token"]
repositories = []


# Define a query para obter os 1000 repositórios mais populares
query = """
    query {
        search(query: "stars:>1", type: REPOSITORY, first: 100) {
            repositoryCount
            edges {
                node {
                    ... on Repository {
                        nameWithOwner
                        url
                    }
                }
            }
        }
    }
"""
headers = {
    'Authorization': f'Token {token}',
    'Content-Type': 'application/json'
}

# Faz a requisição para a API do GitHub
response = requests.post("https://api.github.com/graphql", json={"query": query}, headers=headers)

data = response.json()["data"]["search"]["edges"]

# Filtra os repositórios que usam GitHub Actions
filtered_repos = []
for repo in data:
    name_with_owner = repo["node"]["nameWithOwner"]
    url = repo["node"]["url"]
    repo_response = requests.get(f"{url}/tree/main/.github/workflows", headers=headers)
    if repo_response.status_code == 200:
        filtered_repos.append(name_with_owner)
        with open('repos_list.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name_with_owner])


# Imprime a lista dos repositórios que usam GitHub Actions
print(filtered_repos)
