from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import re
import unicodedata

job = input('Введите искомую вакансию: ')
main_site = 'https://russia.superjob.ru'
l = job.split()
job_fine = '%20'.join(l)

main_link = main_site+'/vacancy/search/?keywords='+job_fine
response =requests.get(main_link)
html = response.text
soup = bs(html,'html.parser')
v_divs = soup.find_all('div',{'class':'jNMYr GPKTZ _1tH7S'})

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
    if 'По' in sal:
        return [min,max,cur]
    else:
        #sal = sal.replace(u'\xa0',u'')
        cur = sal.split()[-1]
        sal = ' '.join(sal.split()[:-1])
        if 'от' in sal:

            min = ''.join(re.findall(r'\d+',sal))
            max = None
        elif 'до' in sal:

            min = None
            max = ''.join(re.findall(r'\d+',sal))
        elif '—' in sal:
            val = sal.split('—')
            min = ''.join(re.findall(r'\d+', val[0]))
            max = ''.join(re.findall(r'\d+', val[1]))
        else:
            min = ''.join(re.findall(r'\d+', sal))
            max = ''.join(re.findall(r'\d+', sal))

    return [min, max, cur]



for n in range(len(v_divs)):
    v_children = v_divs[n].findChildren(recursive=False)
    title.append(v_children[0].getText())
    salary_result = salary_fine(v_children[1].getText())
    salaryMIN.append(salary_result[0])
    salaryMAX.append(salary_result[1])
    salaryCUR.append(salary_result[2])
    link.append(main_site+v_children[0].find('a').get('href'))
    origin.append(main_link)

while len(soup.find_all('a',{'rel':'next'})) > 0:
    goon = input('Есть еще вакансии продолжить ? y/n: ')
    if goon == 'y':
        next_link = soup.find_all('a',{'rel':'next'})
        next_link_href = main_site + next_link[0].get('href')
        response = requests.get(next_link_href)
        html = response.text
        soup = bs(html, 'html.parser')
        v_divs = soup.find_all('div', {'class': 'jNMYr GPKTZ _1tH7S'})
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
df.to_csv('vacancies_sj.csv', encoding="utf-8")
total_v= len(df.index)

print('Загружено ',total_v, ' вакансий')

