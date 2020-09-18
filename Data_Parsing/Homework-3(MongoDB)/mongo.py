from pymongo import MongoClient
from bs4 import BeautifulSoup as bs
import requests
import re
from pprint import pprint

client = MongoClient('127.0.0.1',27017)
db = client['jobs']
jj = db.jj

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
           'Accept': '*/*'
           }
job_list = []

#****HH****
def parse_job(job):
    main_site = 'https://hh.ru'
    l = job.split()
    job_fine = '+'.join(l)

    main_link = main_site+'/search/vacancy?text='+job_fine
    response = requests.get(main_link, headers=headers)
    html = response.text
    soup = bs(html, 'html.parser')
    v_divs = soup.find_all('div', {'class':'vacancy-serp-item__row vacancy-serp-item__row_header'})
    jobs = {}



    def salary_fine_hh(sal):
        min = 0
        max = 0
        cur = None
        if len(sal) == 0:
            return [min, max, cur]
        else:
            sal = sal.replace(u'\xa0', u'')
            cur = sal.split()[-1]
            sal = ' '.join(sal.split()[:-1])
            if 'от' in sal:
                val = sal.split(' ')
                min = val[1]
                max = 0
            elif 'до' in sal:
                val = sal.split(' ')
                min = 0
                max = val[1]
            else:
                val = sal.split('-')
                min = val[0]
                max = val[1]
            return [min, max, cur]

    for n in range(len(v_divs)):
        jobs.pop('_id', None)
        v_children = v_divs[n].findChildren(recursive=False)
        jb = v_children[0].getText()
        salary_result = salary_fine_hh(v_children[1].getText())
        jsmin = int(salary_result[0])
        jsmax = int(salary_result[1])
        jsc = salary_result[2]
        jlin = v_children[0].find('a').get('href')
        jo = main_link
        jobs = {'title':jb,'salaryMIN':jsmin,'salaryMAX':jsmax,'salaryCUR':jsc,'link':jlin,'origin': jo}
        job_list.append(jobs)

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
                jobs.pop('_id', None)
                v_children = v_divs[n].findChildren(recursive=False)
                jb = v_children[0].getText()
                salary_result = salary_fine_hh(v_children[1].getText())
                jsmin = int(salary_result[0])
                jsmax = int(salary_result[1])
                jsc = salary_result[2]
                jlin = v_children[0].find('a').get('href')
                jo = main_link
                jobs = {'title': jb, 'salaryMIN': jsmin, 'salaryMAX': jsmax, 'salaryCUR': jsc, 'link': jlin,
                        'origin': jo}
                job_list.append(jobs)

        else:
            break

    #***SUPERJOB

    sj_site = 'https://russia.superjob.ru'
    l = job.split()
    job_fine = '%20'.join(l)

    sj_link = sj_site+'/vacancy/search/?keywords='+job_fine
    response = requests.get(sj_link)
    html = response.text
    soup = bs(html,'html.parser')
    v_divs = soup.find_all('div',{'class':'jNMYr GPKTZ _1tH7S'})

    def salary_fine(sal):
        min = 0
        max = 0
        cur = None
        if 'По' in sal:
            return [min, max, cur]
        else:
            cur = sal.split()[-1]
            sal = ' '.join(sal.split()[:-1])
            if 'от' in sal:
                min = ''.join(re.findall(r'\d+',sal))
                max = 0
            elif 'до' in sal:
                min = 0
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
        jobs.pop('_id', None)
        v_children = v_divs[n].findChildren(recursive=False)
        jb = v_children[0].getText()
        salary_result = salary_fine(v_children[1].getText())
        jsmin = int(salary_result[0])
        jsmax = int(salary_result[1])
        jsc = salary_result[2]
        jlin = sj_site + v_children[0].find('a').get('href')
        jo = sj_link
        jobs = {'title': jb, 'salaryMIN': jsmin, 'salaryMAX': jsmax, 'salaryCUR': jsc, 'link': jlin, 'origin': jo}
        job_list.append(jobs)

    while len(soup.find_all('a',{'rel':'next'})) > 0:
        goon = input('Есть еще вакансии продолжить ? y/n: ')
        if goon == 'y':
            next_link = soup.find_all('a',{'rel':'next'})
            next_link_href = sj_site + next_link[0].get('href')
            response = requests.get(next_link_href)
            html = response.text
            soup = bs(html, 'html.parser')
            v_divs = soup.find_all('div', {'class': 'jNMYr GPKTZ _1tH7S'})
            for n in range(len(v_divs)):
                jobs.pop('_id', None)
                v_children = v_divs[n].findChildren(recursive=False)
                jb = v_children[0].getText()
                salary_result = salary_fine(v_children[1].getText())
                jsmin = int(salary_result[0])
                jsmax = int(salary_result[1])
                jsc = salary_result[2]
                jlin = sj_site + v_children[0].find('a').get('href')
                jo = sj_link
                jobs = {'title': jb, 'salaryMIN': jsmin, 'salaryMAX': jsmax, 'salaryCUR': jsc, 'link': jlin,
                        'origin': jo}
                job_list.append(jobs)

        else:
            break
    ttl_jobs = len(job_list)
    print('Спарсено ', ttl_jobs, 'вакансий')
    return job_list

job = input('Введите искомую вакансию: ')
parse_job(job)

def find_job(max_salary):
    for jobs in jj.find({'salaryMAX':{'$gt':max_salary}}).sort('salaryMAX',-1).limit(5):
        pprint(jobs)
    for jobs in jj.find({'salaryMIN':{'$gt':max_salary}}).sort('salaryMIN',-1).limit(5):
        pprint(jobs)

def add_jobs_all(jl):
    jj.insert_many(jl)


def only_new(jl):
    for n in range(len(jl)):
        search_link = jl[n]['link']
        sl = jj.find_one({'link': search_link})
        if not sl:
            jj.insert_one(jl[n])


add_all = input('Добавить в базу вакансии ? y/n')
if add_all == 'y':
    add_jobs_all(job_list)


next_op = input('Добавить в базу только новые вакансии ? y/n')
if next_op == 'y':
    only_new(job_list)


max_salary = int(input('Введите минимальную зарплату'))
find_job(max_salary)


