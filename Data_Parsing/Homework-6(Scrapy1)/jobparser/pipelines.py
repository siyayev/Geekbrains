# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import re

class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost',27017)
        self.mongo_base = client.vacancies

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]

        if spider.name == 'hhru':
            if len(item['salary']) == 5:
                if 'до ' in item['salary']:
                    item['min_salary'] = None
                    max_salary_ind = item['salary'].index('до ') + 1
                    item['max_salary'] = ''.join(re.findall(r'\d+', item['salary'][max_salary_ind]))
                else:
                    min_salary_ind = item['salary'].index('от ') + 1
                    item['min_salary'] = ''.join(re.findall(r'\d+', item['salary'][min_salary_ind]))
                    item['max_salary'] = None
                item['salary_currency'] = item['salary'][3]  # Определяем валюту ЗП
                item['salary_opt'] = item['salary'][4]  # Определяем условие ЗП: на руки, до вычета налогов и др

            elif len(item['salary']) > 5:
                min_salary_ind = item['salary'].index('от ') + 1
                item['min_salary'] = ''.join(re.findall(r'\d+', item['salary'][min_salary_ind]))  # Определяем минимальную ЗП
                max_salary_ind = item['salary'].index(' до ') + 1
                item['max_salary'] = ''.join(re.findall(r'\d+', item['salary'][max_salary_ind]))  # Определяем максимальную ЗП
                item['salary_currency'] = item['salary'][-2]  # Определяем валюту ЗП
                item['salary_opt'] = item['salary'][-1]  # Определяем условие ЗП: на руки, до вычета налогов и др
            else:
                item['salary_opt'] = item['salary'][0]  # обрабатываем условие - з/п не указана  просто записываем в условие ЗП
            del item['salary']

        if spider.name == 'sjru':
            if len(item['salary']) > 1:
                if 'от' in item['salary']:
                    min_salary_ind = item['salary'].index('от') + 2
                    item['min_salary'] = ''.join(re.findall(r'\d+', item['salary'][min_salary_ind]))  # Определяем минимальную ЗП
                    item['max_salary'] = None  # Определяем максимальную ЗП

                elif 'до' in item['salary']:
                    max_salary_ind = item['salary'].index('до') + 2
                    item['min_salary'] = None  # Определяем максимальную ЗП
                    item['max_salary'] = ''.join(re.findall(r'\d+', item['salary'][max_salary_ind]))  # Определяем максимальную ЗП

                elif '—' in item['salary']:
                    item['min_salary'] = ''.join(re.findall(r'\d+', item['salary'][0]))
                    max_salary_ind = item['salary'].index('—') + 2
                    item['max_salary'] = ''.join(re.findall(r'\d+', item['salary'][max_salary_ind]))

                item['salary_currency'] = 'руб'  # Определяем валюту ЗП
                item['salary_opt'] = item['salary'][-1]  # Определяем условие ЗП: на руки, до вычета налогов и др
            else:
                item['salary_opt'] = item['salary'][0]  # обрабатываем условие - з/п не указана  просто записываем в условие ЗП
            del item['salary']

        collection.insert_one(item)


        return item