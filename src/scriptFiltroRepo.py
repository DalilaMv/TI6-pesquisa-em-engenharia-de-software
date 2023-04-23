import csv
import math
import requests
import os
from datetime import datetime
from dateutil import parser
from dotenv import load_dotenv

load_dotenv()

headers = {"Authorization": "Bearer " + os.environ["ACCESS_TOKEN"]}
url = 'https://api.github.com/graphql'
variables = {"after": None, 'queryString': 'stars:>100 sort:stars-desc'}
total_count = 0

query = '''
query ($queryString: String!, $after: String) {
    search(query: $queryString, type: REPOSITORY, first: 20, after: $after) {
        pageInfo {
            endCursor
        }
        nodes {
            ... on Repository {
                nameWithOwner
                url
                createdAt
            }
        }
    }
}
'''

# cria o arquivo csv para salvar os resultados
with open('allRepositories.csv', mode='w', newline='') as csv_file:
    fieldnames = ['nameWithOwner', 'url', 'createdAt']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for i in range(50):
        r = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)
        data = r.json()
        # repos = data['data']['search']['nodes']
        result = data['data']['search']
        endCursor = result['pageInfo']['endCursor']
        variables["after"] = endCursor
        repositories = result["nodes"]

        try:
            for repo in repositories:
                writer.writerow({
                    'nameWithOwner': repo['nameWithOwner'],
                    'url': repo['url'],
                    'createdAt': repo['createdAt']})
                print(repo['nameWithOwner'])
                print(total_count)
                total_count += 1
        except KeyError:
            print(data)
