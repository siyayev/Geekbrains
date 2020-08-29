import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&noGeo=1']

    def parse(self, response: HtmlResponse):
        vacancy_links = response.xpath("//a[contains(@href,'vakansii')]//@href").extract()
        for link in vacancy_links:
            yield response.follow(link, callback=self.vacancy_parse)
        next_page = response.xpath("//a[contains(@class,'f-test-button-dalshe')]//@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)


    def vacancy_parse(self, response: HtmlResponse):
        vacancy_name = response.css("h1::text").extract_first()
        vacancy_salary = response.xpath("//h1/../span//text()").extract()

        yield JobparserItem(name=vacancy_name, salary=vacancy_salary, link=response.url, link_origin=self.name)