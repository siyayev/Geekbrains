import requests
import json
headers = {'User-Agent': 'my-test-app/0.0.1',
           'Accept': 'application/vnd.github.v3+json'
           }
user_name = input('Введите имя пользователя: ')
main_link = 'https://api.github.com/users/' + user_name
repo_link = main_link+'/repos'

response = requests.get(main_link, headers=headers)

if response.status_code == 404:
    user_name = input('Пользователь не найден, повторите попытку')
else:
    repos = requests.get(repo_link, headers=headers)
    repo = repos.json()
    print('Список репозиториев пользователя ', user_name)
    for i in range(len(repo)):
        print(repo[i]['name'])
    with open(user_name+'_repos.json', 'w') as outfile:
        json.dump(repos.json(), outfile)
    print('Список репозитеориев успешно сохранен в файле ', user_name+'_repos.json')