import csv
import requests
import json
import os
from dotenv import load_dotenv
import random

load_dotenv()

tokens = [os.environ["token"], os.environ["token3"], os.environ["token5"]]
token = random.choice(tokens)
repositories = []

# Define a query para obter os 1000 repositórios mais populares
query = """
    query($after: String) {
    search(query: "stars:>1 sort:stars-desc", type: REPOSITORY, first: 100, after: $after) {
            nodes {
                ... on Repository {
                    nameWithOwner
                    url
                    stargazerCount
                    primaryLanguage {
                        name
                    }
                    createdAt
                }
            }
            pageInfo {
                endCursor
                hasNextPage
            }
        }
    }
"""

variables = {
    "after": None,
}

headers = {
    'Authorization': f'Token {token}',
    'Content-Type': 'application/json'
}

count = 0
data = []

while count < 1000:
    try:
        # Faz a requisição para a API do GitHub
        response = requests.post("https://api.github.com/graphql",
                                 json={"query": query, "variables": variables}, headers=headers)
    except Exception as ex:
        if response.status_code > 202:
            token = random.choice(tokens)
        continue
    print(variables["after"])

    data = response.json()['data']['search']['nodes']
    page_info = response.json()['data']['search']['pageInfo']

    # Filtra os repositórios que usam GitHub Actions
    for repo in data:
        name_with_owner = repo['nameWithOwner']
        url = repo['url']
        stars = repo['stargazerCount']
        language = repo['primaryLanguage']['name'] if repo['primaryLanguage'] else 'Unknown'
        created_at = repo['createdAt']
        repo_response_main = requests.get(
            f"{url}/tree/main/.github/workflows", headers=headers)
        repo_response_master = requests.get(
            f"{url}/tree/master/.github/workflows", headers=headers)
        if (repo_response_main.status_code == 200 or repo_response_master.status_code == 200):
            if repo_response_main.status_code == 200:
                branch_name = 'main'
            else:
                branch_name = 'master'
            with open('repos_list.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(
                    [name_with_owner, stars, language, created_at, branch_name])
                count += 1

    if not page_info['hasNextPage']:
        break
    variables['after'] = page_info['endCursor']
