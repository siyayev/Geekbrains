# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy
import os
import re
from scrapy.loader.processors import MapCompose, TakeFirst, Compose


def get_big_image(value): #подставляем ссылку для больших картинок
    big_image_link = 'https://res.cloudinary.com/lmru/image/upload/f_auto,q_auto,w_2000,h_2000,c_pad,b_white,d_photoiscoming.png/LMCode/'
    file =os.path.basename(value)
    return f'{big_image_link}{file}'


def clear_price(value):
    value = ''.join(re.findall(r'\d+', value))
    return value


def clear_item_specs(value):
    value = re.sub(r'\s\s', '', value)
    return value


class ItemparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())
    value = scrapy.Field(input_processor=MapCompose(clear_price), output_processor=TakeFirst())
    currency = scrapy.Field(output_processor=TakeFirst())
    unit = scrapy.Field(output_processor=TakeFirst())
    images = scrapy.Field(input_processor=MapCompose(get_big_image))
    term = scrapy.Field()
    definition = scrapy.Field(input_processor=MapCompose(clear_item_specs))
    deflist= scrapy.Field()


