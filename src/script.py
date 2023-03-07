
import json
import requests
import os
from datetime import datetime
from dotenv import load_dotenv
import csv

load_dotenv()

token = os.environ["token"]
url = os.environ["github_api_url"]
repositories = []


def teste_pullrequest(pr_number):
    
    query = """
      query ($owner: String!, $repo: String!, $prNumber: Int!) {
        repository(owner: $owner, name: $repo) {
          pullRequest(number: $prNumber) {
            title
            body
            state
            merged
            additions
            deletions
            comments {
              totalCount
            }
            reviews(first: 10) {
              nodes {
                body
                author {
                  login
                }
                state
              }
            }
            commits(last: 10) {
              nodes {
                commit {
                  message
                  author {
                    name
                    email
                  }
                }
                url
              }
            }
          }
        }
      }
      """


    variables = {"owner": "microsoft", "repo": "vscode", "prNumber": pr_number, "itemTypes": [
        "ISSUE_COMMENT",
        "PULL_REQUEST_REVIEW_COMMENT"
    ]}

    headers = {"Authorization": "Bearer " + token}

    response = requests.post("https://api.github.com/graphql", json={"query": query, 'variables': variables}, headers=headers)
    data = json.loads(response.text)

    print(json.dumps(data, indent=4))


query = """
  query {
    repository(owner: "microsoft", name: "vscode") {
      ref(qualifiedName: "main") {
        target {
          ... on Commit {
            history(first: 50) {
              nodes {
                oid
                messageHeadline
                author {
                  name
                  email
                  date
                }
                associatedPullRequests(first: 1) {
                  nodes {
                    title
                    number
                  }
                }
                checkSuites(first: 1) {
                  nodes {
                    status
                    conclusion
                    checkRuns(first: 1) {
                      nodes {
                        status
                        conclusion
                        detailsUrl
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
"""



headers = {"Authorization": "Bearer " + token}

response = requests.post("https://api.github.com/graphql", json={"query": query}, headers=headers)

if response.status_code == 200:
    data = json.loads(response.text)
    nodes = data['data']['repository']['ref']['target']['history']['nodes']
    for node in nodes:
        check_suite = node['checkSuites']['nodes'][0] if node['checkSuites']['nodes'] else None
        if check_suite and check_suite['status'] == 'COMPLETED' and check_suite['conclusion'] != 'SUCCESS':
            commit_url = f"https://github.com/microsoft/vscode/commit/{node['oid']}"
            print(f"Commit: {node['oid']}")
            print(f"Autor: {node['author']['name']} ({node['author']['email']})")
            print(f"Mensagem: {node['messageHeadline']}")
            print(f"Link para o pull request: https://github.com/microsoft/vscode/pull/{node['associatedPullRequests']['nodes'][0]['number']}")
            check_run = check_suite['checkRuns']['nodes'][0]
            print(f"Status do pipeline: {check_run['status']}")
            print(f"Conclusão do pipeline: {check_run['conclusion']}")
            print(f"Link para o registro do pipeline: {check_run['detailsUrl']}")
            teste_pullrequest(node['associatedPullRequests']['nodes'][0]['number'])
            print()
else:
    print("Erro na requisição: ", response.status_code)

