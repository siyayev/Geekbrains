# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field()
    salary = scrapy.Field()
    min_salary = scrapy.Field()
    max_salary = scrapy.Field()
    salary_opt = scrapy.Field()
    salary_currency = scrapy.Field()
    link = scrapy.Field()
    link_origin = scrapy.Field()

