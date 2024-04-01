import pandas as pd
import os
import json
# read language json
with open('populate-csv/language.json', 'r') as f:
    languageJson = json.load(f)
#read repos csv file
reposDf = pd.read_csv('populate-csv/repos.csv')
# read supply language csv file
supplyLanguageDf = pd.read_csv('populate-csv/supply_language.csv')
# read repos.json
with open('populate-csv/repos.json', 'r') as f:
    reposJson = json.load(f)
# get coveredIds
with open('populate-csv/coveredIds.json', 'r') as f:
    coveredIds = json.load(f)

# indexes of next value to append at
repoIndex = len(reposDf)
languageIndex = len(languageJson) + 1
supplyLanguageIndex = len(supplyLanguageDf)
count = 0


# go through each repo in repos.json
for userId in reposJson:
    if userId in coveredIds:
        print('skipping ' + userId)
        continue
    print('processing ' + userId)
    # go through each repo in user
    for repo in reposJson[userId]["data"]["user"]["repositories"]["nodes"]:
        name = repo["nameWithOwner"]
        numIssues = repo["issues"]["totalCount"]
        numWatchers = repo["watchers"]["totalCount"]

        # get languages
        languages = repo["languages"]["nodes"]
        for language in languages:
            languageName = language["name"]
            if languageName not in languageJson:
                languageJson[languageName] = languageIndex
                languageIndex += 1
                print(languageName + ' added to languageJson')
                with open('populate-csv/language.json', 'w') as f:
                    json.dump(languageJson, f)
            supplyLanguageDf.loc[supplyLanguageIndex] = [repoIndex, languageJson[languageName]]
            supplyLanguageIndex += 1
        
        # add repo to repos.csv
        reposDf.loc[repoIndex] = [repoIndex, name, numIssues, numWatchers]
        repoIndex += 1

    # save repos to csv
    reposDf.to_csv('populate-csv/repos.csv', index=False)

    # save supply language to csv
    supplyLanguageDf.to_csv('populate-csv/supply_language.csv', index=False)
    
    coveredIds.append(userId)
    with open('populate-csv/coveredIds.json', 'w') as f:
        json.dump(coveredIds, f)
    count += 1

    # backups every 100 users
    if count % 100 == 0:
        reposDf.to_csv('populate-csv/backup/repos.csv', index=False)
        supplyLanguageDf.to_csv('populate-csv/backup/supply_language.csv', index=False)
        with open('populate-csv/backup/coveredIds.json', 'w') as f:
            json.dump(coveredIds, f)
        with open('populate-csv/backup/language.json', 'w') as f:
            json.dump(languageJson, f)
        print('backed up')
            
            
