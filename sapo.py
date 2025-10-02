import time
from datetime import datetime
from urllib.parse import urlencode
from selenium.webdriver.common.by import By

from utils import (
    load_config, check_url_active, set_page,
    build_driver, save_csv, save_json
)


SITE_NAME = "sapo"
HEADER = ["Title", "Link", "Company", "Location", "Type", "Date Posted", "Description"]


def build_url(config):
    base = "https://emprego.sapo.pt/offers"
    query_params = {
        "local": config["query"]["local"],
        "pesquisa": config["query"]["pesquisa"],
        "hora": config["query"]["hora"],
        "pagina": 1,
        "ordem": config["query"]["ordem"],
        "data-de-publicacao": config["query"]["data-de-publicacao"]
    }
    return f"{base}?{urlencode(query_params)}"


def max_page(url, config):
    driver = build_driver(config)
    driver.implicitly_wait(config["wait_time"])
    try:
        driver.get(url)
        pagination_elements = driver.find_elements(By.CSS_SELECTOR, "ul li a")
        numbers = [int(el.text.strip()) for el in pagination_elements if el.text.strip().isdigit()]
        return max(numbers) if numbers else 1
    finally:
        driver.quit()


def parse_jobs(driver, current_page_url):
    jobs = driver.find_elements(By.CSS_SELECTOR, "ul.unstyled.column-group.half-gutters.no-top-space > li")
    results = []

    for job in jobs:
        if not job.find_elements(By.CSS_SELECTOR, "h3 a"):
            continue

        title_el = job.find_element(By.CSS_SELECTOR, "h3 a")
        title = title_el.text.strip()
        link = title_el.get_attribute("href")

        company = job.find_element(By.CSS_SELECTOR, "li.name a").text.strip() \
            if job.find_elements(By.CSS_SELECTOR, "li.name a") else None

        location = job.find_element(By.CSS_SELECTOR, "li.location").text.strip() \
            if job.find_elements(By.CSS_SELECTOR, "li.location") else None

        job_type = job.find_element(By.CSS_SELECTOR, "li.time").text.strip() \
            if job.find_elements(By.CSS_SELECTOR, "li.time") else None

        date_posted = job.find_element(By.CSS_SELECTOR, "li.date").text.strip() \
            if job.find_elements(By.CSS_SELECTOR, "li.date") else None

        description = job.find_element(By.CSS_SELECTOR, "p.quarter-bottom-space").text.strip() \
            if job.find_elements(By.CSS_SELECTOR, "p.quarter-bottom-space") else None

        results.append([title, link, company, location, job_type, date_posted, description])

    return results


def run_scraper():
    config = load_config()
    today_str = datetime.now().strftime("%d-%m-%Y")
    pesquisa = config["query"]["pesquisa"].replace(" ", "_")

    url = build_url(config)
    all_results = []
    total_jobs = 0

    print(f"\n🔍 Starting {SITE_NAME} scraping: {url}")
    if check_url_active(url):
        total_pages = max_page(url, config)
        for page_num in range(1, total_pages + 1):
            driver = build_driver(config)
            driver.implicitly_wait(config["wait_time"])
            current_page_url = set_page(url, page_num)
            driver.get(current_page_url)

            results = parse_jobs(driver, current_page_url)
            driver.quit()

            if not results:
                print(f"⚠️ No results on page {page_num}, stopping early.")
                break

            all_results.extend(results)
            total_jobs += len(results)
            print(f"🪨 ⛏️  Page {page_num}: {len(results)} jobs")
            time.sleep(config["rate_limit"])

    if all_results:
        if "csv" in config.get("output_formats", []):
            save_csv(all_results, HEADER, SITE_NAME, pesquisa, today_str)
        if "json" in config.get("output_formats", []):
            save_json(all_results, HEADER, SITE_NAME, pesquisa, today_str)

    print(f"\n📦 Finished {SITE_NAME}! Total jobs: {total_jobs}")
