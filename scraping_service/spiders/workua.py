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

        next_page_disabled = response.css("li.add-left-default::attr(class)").get().split(" ")[1]
        if next_page_disabled != "disabled":
            next_page_number = int(response.css(".pagination > .active > span::text").get()) + 1
            next_page = response.urljoin(f"?page={next_page_number}")
            yield response.follow(next_page, callback=self.parse)

    def parse_job_page_info(self, response: Response):
        specialization = response.meta["specialization"]
        title = response.css("h1.my-0::text").get()

        company = response.css(
            "ul.list-unstyled > li > a.inline > span.strong-500::text"
        ).get()

        skills = self.get_skills_info(response)
        salary = self.get_salary_info(response)
        years_of_experience = self.get_experience_info(response, salary)
        remote, office, location = self.get_work_style_and_location_info(
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

    def get_skills_info(self, response: Response) -> int | list[str]:
        skills = response.css("ul.flex > li > span::text").getall()
        if not skills:
            return 0
        else:
            return skills

    def get_salary_info(self, response: Response) -> int | str:
        salary = response.css(
            "ul.list-unstyled > li > span.strong-500::text"
        ).get()

        if salary:
            return (salary.replace("\u202f", "")
                    .replace("\u2009", "").replace(" грн", ""))
        else:
            return 0

    def get_experience_info(
            self,
            response: Response,
            salary: int | None
    ) -> str | int:
        i = 0
        if salary == 0:
            i = 2
        else:
            i = 3

        words = response.css("ul.list-unstyled > li.text-indent").xpath(
            "normalize-space(string())"
        ).getall()[i].split(" ")

        years_of_experience = "".join([
            word
            for word in words
            if word.isdigit()
        ])
        if not years_of_experience:
            return 0
        else:
            return years_of_experience

    def get_work_style_and_location_info(
            self,
            response: Response,
            salary: str | int
    ) -> (int, int, int):
        i = 0
        check_for_hourly_salary = response.css(
            "ul.list-unstyled > li.text-indent > span::attr(title)"
        ).get()

        if salary == 0:
            if check_for_hourly_salary == "Зарплата":
                i = 2
            else:
                i = 1
        else:
            i = 2

        work_style = response.css(
            "ul.list-unstyled > li.text-indent"
        ).xpath("normalize-space(string())").getall()[i]

        if work_style == "Дистанційна робота":
            remote = 1
            office = 0
            location = 0
            return remote, office, location
        else:
            remote = 0
            office = 1
            location = work_style.split(",")[0]
            return remote, office, location
