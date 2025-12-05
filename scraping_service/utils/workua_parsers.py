from scrapy.http import Response


def get_skills_info(response: Response) -> int | list[str]:
    skills = response.css("ul.flex > li > span::text").getall()
    return 0 if not skills else skills


def get_salary_info(response: Response) -> int | str:
    salary = response.css(
        "ul.list-unstyled > li > span.strong-500::text"
    ).get()
    return 0 if not salary else (
        salary.replace("\u202f", "")
        .replace("\u2009", "")
        .replace(" грн", "")
    )


def get_experience_info(
        response: Response,
        salary: int | str
) -> int | str:
    item_number = 2 if salary == 0 else 3
    words = response.css("ul.list-unstyled > li.text-indent").xpath(
        "normalize-space(string())"
    ).getall()[item_number].split(" ")

    years_of_experience = "".join([
        word
        for word in words
        if word.isdigit()
    ])

    return 0 if not years_of_experience else years_of_experience


def get_work_style_and_location_info(
        response: Response,
        salary: int | str
) -> (int, int, int | str):
    is_hourly_salary = response.css(
        "ul.list-unstyled > li.text-indent > span::attr(title)"
    ).get()

    item_number = 1 if salary == 0 and is_hourly_salary != "Зарплата" else 2
    job_org = response.css(
        "ul.list-unstyled > li.text-indent"
    ).xpath("normalize-space(string())").getall()[item_number]

    remote = 1 if job_org == "Дистанційна робота" else 0
    office = 0 if job_org == "Дистанційна робота" else 1
    location = 0 if job_org == "Дистанційна робота" else job_org.split(",")[0]
    return remote, office, location
