import re
import time
from datetime import datetime
from urllib.parse import urlencode, urljoin
from selenium.webdriver.common.by import By

from utils import (
    load_config, check_url_active, set_page,
    build_driver, save_csv, save_json
)


SITE_NAME = "netempregos"
HEADER = ["Title", "Link", "Company", "Location", "Category", "Date Posted"]


def build_url(config):
    base = "https://www.net-empregos.com/pesquisa-empregos.asp"
    query_params = {
        "chaves": config["query"]["pesquisa"],
        "cidade": config["query"]["local"],
        "categoria": config["query"]["categoria"],
        "zona": config["query"]["zona"],
        "tipo": config["query"]["tipo"],
    }
    return f"{base}?{urlencode(query_params)}"


def max_page(url, config):
    driver = build_driver(config)
    driver.implicitly_wait(config["wait_time"])
    try:
        driver.get(url)
        h3_text = driver.find_element(By.CSS_SELECTOR, "h3").text.strip()
        match = re.search(r'/\s*(\d+)', h3_text)
        return int(match.group(1)) if match else 1
    finally:
        driver.quit()


def parse_jobs(driver, current_page_url):
    jobs = driver.find_elements(By.CSS_SELECTOR, "div.job-item.media")
    results = []

    for job in jobs:
        if not job.find_elements(By.CSS_SELECTOR, "h2 a.oferta-link"):
            continue

        title_el = job.find_element(By.CSS_SELECTOR, "h2 a.oferta-link")
        title = title_el.text.strip()
        link = urljoin(current_page_url, title_el.get_attribute("href"))

        date_posted = (
            job.find_element(By.CSS_SELECTOR, "li i.flaticon-calendar")
            .find_element(By.XPATH, "./..")
            .text.strip()
            if job.find_elements(By.CSS_SELECTOR, "li i.flaticon-calendar")
            else None
        )

        location = (
            job.find_element(By.CSS_SELECTOR, "li i.flaticon-pin")
            .find_element(By.XPATH, "./..")
            .text.strip()
            if job.find_elements(By.CSS_SELECTOR, "li i.flaticon-pin")
            else None
        )

        category = (
            job.find_element(By.CSS_SELECTOR, "li i.fa-tags")
            .find_element(By.XPATH, "./..")
            .text.strip()
            if job.find_elements(By.CSS_SELECTOR, "li i.fa-tags")
            else None
        )

        company = (
            job.find_element(By.CSS_SELECTOR, "li i.flaticon-work")
            .find_element(By.XPATH, "./..")
            .text.strip()
            if job.find_elements(By.CSS_SELECTOR, "li i.flaticon-work")
            else None
        )

        results.append([title, link, company, location, category, date_posted])

    return results


def run_scraper(search_term=None):
    config = load_config()
    today_str = datetime.now().strftime("%d-%m-%Y")

    if search_term:
        config["query"]["pesquisa"] = search_term

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
                print(f"⚠️  No results on page {page_num}, stopping early.")
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
