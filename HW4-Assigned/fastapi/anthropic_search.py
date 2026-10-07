import datetime

from playwright.sync_api import sync_playwright

from qualification_parser import retreive_qualification
from gemini_summarizer import return_gemini_summaries


def retrieve_anthropic_jobs(url: str, role: str) -> list:
    if not url.startswith("http"):
        url = "https://" + url

    jobs = []
    qualifications = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(url)
        page.wait_for_selector("main")

        search_box = page.get_by_placeholder("Search roles")
        search_box.fill(role)

        page.wait_for_selector('a[class*="jobItem"]')
        page.wait_for_timeout(1500)

        job_links = page.locator('a[class*="jobItem"]')

        for i in range(job_links.count()):
            job = job_links.nth(i)

            title = job.inner_text().strip()
            link = job.get_attribute("href")

            if not link:
                continue

            if link.startswith("/"):
                link = "https://www.anthropic.com" + link

            qualification = retreive_qualification(link)

            jobs.append({
                "title": title,
                "link": link,
                "date": datetime.date.today().strftime("%Y-%m-%d"),
                "qualification": qualification,
            })

            qualifications.append(qualification)

        browser.close()

    skills = return_gemini_summaries(qualifications)

    for job, skill in zip(jobs, skills):
        job["skills"] = skill

    return jobs