from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess
from itemparser import settings
from itemparser.spiders.lm import LmSpider


if __name__ == '__main__':
    item_settings = Settings()
    item_settings.setmodule(settings)
    process = CrawlerProcess(settings=item_settings)
    process.crawl(LmSpider, query= 'РЕСПИРАТОРЫ И ЗАЩИТНЫЕ МАСКИ')
    process.start()
