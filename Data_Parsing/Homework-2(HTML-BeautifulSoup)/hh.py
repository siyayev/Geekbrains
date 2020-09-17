from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
           'Accept': '*/*'
           }
job = input('Введите искомую вакансию: ')
main_site = 'https://hh.ru'
l = job.split()
job_fine = '+'.join(l)

main_link = main_site+'/search/vacancy?text='+job_fine
response =requests.get(main_link, headers=headers)
html = response.text
soup = bs(html,'html.parser')
v_divs = soup.find_all('div',{'class':'vacancy-serp-item__row vacancy-serp-item__row_header'})

title = []
salary = []
link = []
origin = []
print('1')

for n in range(len(v_divs)):
    v_children = v_divs[n].findChildren(recursive=False)
    title.append(v_children[0].getText())
    if len(v_children[1].getText()) > 0:
        salary.append(v_children[1].getText())
    else:
        salary.append('з/п не указана')
    link.append(v_children[0].find('a').get('href'))
    origin.append(main_link)

while len(soup.find_all('a',{'data-qa': 'pager-next'})) > 0:
    goon = input('Есть еще вакансии продолжить ? y/n: ')
    if goon == 'y':
        next_link = soup.find_all('a',{'data-qa': 'pager-next'})
        next_link_href = main_site + next_link[0].get('href')
        response = requests.get(next_link_href, headers=headers)
        html = response.text
        soup = bs(html, 'html.parser')
        v_divs = soup.find_all('div',{'class':'vacancy-serp-item__row vacancy-serp-item__row_header'})
        for n in range(len(v_divs)):
            v_children = v_divs[n].findChildren(recursive=False)
            title.append(v_children[0].getText())
            salary.append(v_children[1].getText())
            link.append(main_site + v_children[0].find('a').get('href'))
            origin.append(main_link)
    else:
        break


df = pd.DataFrame({
    'VacancyTile': title,
    'VacancySalary': salary,
    'VacancyLink': link,
    'VacancyOrigin': origin})
df.to_csv('vacancies_hh.csv', encoding="utf-8")
total_v= len(df.index)

print('Загружено ',total_v, ' вакансий')

