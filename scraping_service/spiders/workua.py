from urllib.parse import urljoin

import scrapy
from scrapy.http import Response

from scraping_service.utils.workua_parsers import (
    get_skills_info,
    get_salary_info,
    get_experience_info,
    get_work_style_and_location_info
)


WORKUA_URL = "https://www.work.ua"


class WorkuaSpider(scrapy.Spider):
    name = "workua"
    allowed_domains = ["work.ua", "www.work.ua"]
    start_urls = [
        "https://www.work.ua/jobs-python",
        "https://www.work.ua/jobs-java",
        "https://www.work.ua/jobs-javascript"
    ]

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

        is_next_page_disabled = response.css(
            "li.add-left-default::attr(class)"
        ).get().split(" ")[1]
        if is_next_page_disabled != "disabled":
            next_page_number = int(
                response.css(".pagination > .active > span::text").get()
            ) + 1
            next_page = response.urljoin(f"?page={next_page_number}")
            yield response.follow(next_page, callback=self.parse)

    def parse_job_page_info(self, response: Response):
        specialization = response.meta["specialization"]
        title = response.css("h1.my-0::text").get()
        company = response.css(
            "ul.list-unstyled > li > a.inline > span.strong-500::text"
        ).get()
        skills = get_skills_info(response)
        salary = get_salary_info(response)
        years_of_experience = get_experience_info(response, salary)
        remote, office, location = get_work_style_and_location_info(
            response,
            salary
        )

        yield {
            "specialization": specialization,
            "title": title,
            "company": company,
            "salary": salary,
            "location": location,
            "office": office,
            "remote": remote,
            "years_of_experience": years_of_experience,
            "skills": skills
        }
