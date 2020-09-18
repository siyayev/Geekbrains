from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import re
import unicodedata
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
#v_divs = soup.prettify(formatter=lambda s: s.replace(u'\xa0', ''))

title = []
salaryMIN = []
salaryMAX = []
salaryCUR = []
link = []
origin = []



def salary_fine(sal):
    min = None
    max = None
    cur = None
    if len(sal)==0:
        return [min,max,cur]
    else:
        sal = sal.replace(u'\xa0',u'')
        cur = sal.split()[-1]
        sal = ' '.join(sal.split()[:-1])
        if 'от' in sal:
            val = sal.split(' ')
            min = val[1]
            max = None
        elif 'до' in sal:
            val = sal.split(' ')
            min = None
            max = val[1]
        else:
            val = sal.split('-')
            min = val[0]
            max = val[1]
        return [min, max, cur]

for n in range(len(v_divs)):
    v_children = v_divs[n].findChildren(recursive=False)
    title.append(v_children[0].getText())
    salary_result = salary_fine(v_children[1].getText())
    salaryMIN.append(salary_result[0])
    salaryMAX.append(salary_result[1])
    salaryCUR.append(salary_result[2])
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
            salary_result = salary_fine(v_children[1].getText())
            salaryMIN.append(salary_result[0])
            salaryMAX.append(salary_result[1])
            salaryCUR.append(salary_result[2])
            link.append(main_site + v_children[0].find('a').get('href'))
            origin.append(main_link)
    else:
        break


df = pd.DataFrame({
    'VacancyTile': title,
    'VacancySalaryMin': salaryMIN,
    'VacancySalaryMax': salaryMAX,
    'VacancySalaryCur': salaryCUR,
    'VacancyLink': link,
    'VacancyOrigin': origin})

dc = df.to_dict()
print(dc)

#df.to_csv('vacancies_hh.csv', encoding="utf-8")
total_v= len(df.index)

print('Загружено ',total_v, ' вакансий')

