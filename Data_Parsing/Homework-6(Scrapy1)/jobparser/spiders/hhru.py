import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?area=&fromSearchLine=true&st=searchVacancy&text=Python']

    def parse(self, response:HtmlResponse):
        vacancy_links = response.xpath("//a[@class='bloko-link HH-LinkModifier']/@href").extract()
        for link in vacancy_links:
            yield response.follow(link, callback=self.vacancy_parse)
        next_page = response.css("a.HH-Pager-Controls-Next::attr(href)").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def vacancy_parse(self, response:HtmlResponse):
        vacancy_name = response.css("h1::text").extract_first()
        vacancy_salary = response.css("p.vacancy-salary span::text").extract()
        yield JobparserItem(name=vacancy_name, salary=vacancy_salary, link=response.url, link_origin=self.name)
