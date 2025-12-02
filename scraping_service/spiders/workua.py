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
            specialization = response.url.split("-")[-1].split("/")[0]

            yield scrapy.Request(
                url=absolute_url,
                callback=self.parse_job_page_info,
                meta={"specialization": specialization}
            )

        # next_page_disabled = response.css("li.add-left-default::attr(class)").get().split(" ")[1]
        # if next_page_disabled != "disabled":
        #     next_page_number = int(response.css(".pagination > .active > span::text").get()) + 1
        #     next_page = response.urljoin(f"?page={next_page_number}")
        #     yield response.follow(next_page, callback=self.parse)

    def parse_job_page_info(self, response: Response):
        specialization = response.meta["specialization"]
        title = response.css("h1.my-0::text").get()
        company = response.css(
            "ul.list-unstyled > li > a.inline > span.strong-500::text"
        ).get()

        salary = response.css(
            "ul.list-unstyled > li > span.strong-500::text"
        ).get()
        if salary:
            salary = salary.replace("\u202f", "").replace("\u2009", "").replace(" грн", "")
        else:
            salary = 0

        if salary == 0:
            experience = response.css(
                "ul.list-unstyled > li.text-indent"
            ).xpath(
                "normalize-space(string())"
            ).getall()[2].split(" від ")[1].replace(" років.", "")
        else:
            experience = response.css(
                "ul.list-unstyled > li.text-indent"
            ).xpath(
                "normalize-space(string())"
            ).getall()[3].split(" від ")[1].replace(" років.", "")

        skills = response.css("ul.flex > li > span::text").getall()

        remote, office, location = self.work_style_and_location_info(response)

        yield {
            "specialization": specialization,
            "title": title,
            "company": company,
            "salary": salary,
            "location": location,
            "office": office,
            "remote": remote,
            "min_experience_years": experience,
            "skills": skills
        }

    def work_style_and_location_info(self, response: Response):
        work_style = response.css(
            "ul.list-unstyled > li.text-indent"
        ).xpath("normalize-space(string())").getall()[2]

        if work_style == "Дистанційна робота":
            remote = 1
            office = 0
            location = 0
            return remote, office, location
        else:
            remote = 0
            office = 1
            location = work_style
            return remote, office, location
