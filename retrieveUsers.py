import requests
import json 

PER_PAGE = 100
startid = 0
users = []

with open('users.json', 'r') as f:
    users = json.load(f)

def main():
    startid = users[-1]['id']
    res = requests.get(f'https://api.github.com/users?since={startid}&per_page={PER_PAGE}')
    newUsers = res.json()
    for user in newUsers:
        print(user['id'])
    users.extend(newUsers)

    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)

for i in range(20):
    try:
        main()
    except Exception as e:
        print(e)
        break
