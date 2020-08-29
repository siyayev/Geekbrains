from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess
from jobparser import settings
from jobparser.spiders.hhru import HhruSpider
from jobparser.spiders.sjru import SjruSpider

if __name__ == '__main__':
    job_settings = Settings()
    job_settings.setmodule(settings)
    process = CrawlerProcess(settings=job_settings)
    process.crawl(HhruSpider)
    process.crawl(SjruSpider)

    process.start()
