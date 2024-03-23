import requests
import json 
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

with open('users.json', 'r') as f:
    users = json.load(f)
with open('repos.json', 'r') as f:
    repos = json.load(f)
with open('retrievedUsers.json', 'r') as f:
    retrievedUsers = json.load(f)


count = 0

for user in users:
    if user["node_id"] in retrievedUsers:
        print(f'{user["login"]} already retrieved')
        continue
    retrievedUsers.append(user["node_id"])
    res = requests.post(f'https://api.github.com/graphql', json={
        "query": f'''
        {{
            user(login: "{user['login']}") {{
                id
                login
                repositories(first: 100) {{
                totalCount
                nodes {{
                    primaryLanguage {{
                    name
                    }}
                    languages(first: 100) {{
                    nodes {{
                        name
                    }}
                    }}
                    nameWithOwner
                    description
                    url
                    createdAt
                    stargazerCount
                    forkCount
                    isArchived
                    isFork
                    isDisabled
                    isSecurityPolicyEnabled
                    hasVulnerabilityAlertsEnabled
                    licenseInfo{{
                    key
                    name
                    }}
                    watchers{{
                    totalCount
                    }}
                    issues(first:100){{
                    totalCount
                    }}
                                    
                    
                }}
                }}

            }}
        }}
        '''
    }, headers={
        "Authorization": f"Bearer {GITHUB_TOKEN}"
    })

    data = res.json()
    # print headers
    print(res.request.headers)

    if "errors" in data:
        print(data["errors"])
        continue
    repos[user["node_id"]] = data


    #save data every 5 users
    count += 1
    if count % 5 == 0:
        with open('repos.json', 'w') as f:
            json.dump(repos, f, indent=4)
        with open('retrievedUsers.json', 'w') as f:
            json.dump(retrievedUsers, f, indent=4)
        print('Data saved')

    print(f'{user["login"]} retrieved')
    