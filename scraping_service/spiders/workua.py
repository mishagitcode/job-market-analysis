from urllib.parse import urljoin

import scrapy
from scrapy.http import Response


WORKUA_URL = "https://www.work.ua"


class WorkuaSpider(scrapy.Spider):
    name = "workua"
    allowed_domains = ["work.ua", "www.work.ua"]
    start_urls = ["https://www.work.ua/jobs-it-python"]

    def parse(self, response: Response, **kwargs):
        links_to_job_pages = response.css(".my-0 > a::attr(href)").getall()
        for job_page_link in links_to_job_pages:
            absolute_url = urljoin(WORKUA_URL, job_page_link)
            yield scrapy.Request(url=absolute_url, callback=self.parse_job_page_info)

        next_page_disabled = response.css("li.add-left-default::attr(class)").get().split(" ")[1]
        if next_page_disabled != "disabled":
            next_page_number = int(response.css(".pagination > .active > span::text").get()) + 1
            next_page = response.urljoin(f"?page={next_page_number}")
            yield response.follow(next_page, callback=self.parse)

    def parse_job_page_info(self, response: Response):
        yield {
            "links": response
        }
