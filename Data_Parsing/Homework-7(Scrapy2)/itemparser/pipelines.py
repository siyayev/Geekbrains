# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import scrapy
import os
from urllib.parse import urlparse
from itemparser import settings
import shutil
from pymongo import MongoClient


class ItemparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.ads

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        item['deflist'] = {item['term'][a] : item['definition'][a] for a in range(len(item['term']))} #пробегаемся по элемантам характеристик товара и кидаем их в словарь deflist, потом удаляем ненужное
        del item['term']
        del item['definition']
        collection.insert_one(item)
        return item


class LmPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['images']:
            for img in item['images']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(f'Ошибка{e}')

    def file_path(self, request, response=None, info=None):
        return os.path.basename(urlparse(request.url).path) #сохраняем файлы просто по имени в корневую папку

    def item_completed(self, results, item, info):
        for i in results: #Создаем папку по имени товар и кидаем туда уже сохраненные картинки
            if i[0]:
                old_path = os.path.join(os.getcwd(), settings.IMAGES_STORE, i[1]['path'])
                new_folder = os.path.join(os.getcwd(), settings.IMAGES_STORE, item['name'])
                new_path = os.path.join(new_folder, i[1]['path'])
                if not os.path.exists(new_folder):
                    try:
                        os.mkdir(new_folder)
                    except Exception as e:
                        print(e)
                        pass
                shutil.move(old_path, new_path)
        item['images'] = [i[1] for i in results if i[0]] #генерируем новый список для картинок
        return item
