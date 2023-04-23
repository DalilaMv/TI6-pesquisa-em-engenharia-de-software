import requests
import json


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
  'Authorization': 'Bearer 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',
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

# Imprime a lista dos repositórios que usam GitHub Actions
print(filtered_repos)