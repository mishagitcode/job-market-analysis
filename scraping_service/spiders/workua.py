import scrapy
from scrapy.http import Response


class WorkuaSpider(scrapy.Spider):
    name = "workua"
    allowed_domains = ["www.work.ua"]
    start_urls = ["https://www.work.ua/jobs-it-python/"]

    def parse(self, response: Response):
        pass
