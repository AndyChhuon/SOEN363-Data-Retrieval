import json

# read language json
with open('populate-csv/language.json', 'r') as f:
    languageJson = json.load(f)

# convert to csv
with open('populate-csv/language.csv', 'w') as f:
    for language in languageJson:
        f.write(f"{languageJson[language]},{language}\n")