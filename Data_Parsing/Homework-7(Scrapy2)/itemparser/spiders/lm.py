import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from itemparser.items import ItemparserItem


class LmSpider(scrapy.Spider):
    name = 'lm'
    allowed_domains = ['leroymerlin.ru']
    #start_urls = ['']

    def __init__(self, query):
        super(LmSpider, self).__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={query}']

    def parse(self, response:HtmlResponse):
        ads_links = response.xpath("//product-card/@data-product-url").extract()
        for link in ads_links:
            yield response.follow(link, callback=self.ad_parse)
        next_page = response.xpath("//div[@class='next-paginator-button-wrapper']/a[@rel='next']//@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def ad_parse(self, response:HtmlResponse):
        loader = ItemLoader(item=ItemparserItem(), response=response)
        loader.add_css('name', "h1::text")
        loader.add_xpath('images', "//img[@slot='thumbs']/@src")
        loader.add_xpath('value', "//uc-pdp-price-view[@slot='primary-price']/span[@slot='price']/text()")
        loader.add_xpath('currency', "//uc-pdp-price-view[@slot='primary-price']/span[@slot='currency']/text()")
        loader.add_xpath('unit', "//uc-pdp-price-view[@slot='primary-price']/span[@slot='unit']/text()")
        loader.add_xpath('term', "//dt[@class='def-list__term']/text()")
        loader.add_xpath('definition', "//dd[@class='def-list__definition']/text()")
        loader.add_value('link', response.url)
        yield loader.load_item()

        #ad_images = response.xpath("//img[@slot='thumbs']/@src").extract()
        #ad_name = response.css("h1::text").extract_first()
        #price_value = response.xpath("//uc-pdp-price-view[@slot='primary-price']/span[@slot='price']/text()").extract_first()
        #price_currency = response.xpath("//uc-pdp-price-view[@slot='primary-price']/span[@slot='currency']/text()").extract_first()
        #price_unit = response.xpath("//uc-pdp-price-view[@slot='primary-price']/span[@slot='unit']/text()").extract_first()
        #yield ItemparserItem(name=ad_name, link=response.url, images=ad_images, value=price_value, currency=price_currency, unit=price_unit)