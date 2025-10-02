import csv
import json
import os
import time
import yaml

from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


def load_config():
    with open("settings.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)["scraper"]


def check_url_active(url):
    try:
        with urlopen(url) as response:
            return response.status == 200
    except HTTPError as e:
        print(f"HTTP error: {e.code} - {e.reason}")
    except URLError:
        print("The server could not be found!")
    return False


def set_page(url, page_number):
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    query["pagina"] = [str(page_number)]
    return urlunparse(parsed._replace(query=urlencode(query, doseq=True)))


def build_driver(config):
    options = Options()
    if config["headless"]:
        options.add_argument("--headless=new")

    options.add_argument(f"user-agent={config['user_agent']}")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument(f"--log-level={config['logging']['log_level']}")

    log_path = "NUL" if os.name == "nt" else "/dev/null"
    service = Service(
        config["driver_path"] or None,
        log_path=log_path if config["logging"]["suppress_chrome"] else None
    )
    return webdriver.Chrome(service=service, options=options)


def output_dir():
    # ( ͡° ͜ʖ ͡°) sure...
    output_files = "Output files"
    if not os.path.exists(output_files):
        os.makedirs(output_files)
    return output_files

def save_csv(all_results, header, site_name, pesquisa, today_str, delimiter=";"):
    folder = output_dir()
    filename_csv = os.path.join(folder, f"{pesquisa}_{site_name}_jobs_{today_str}.csv")
    with open(filename_csv, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, delimiter=delimiter)
        writer.writerow(header)
        writer.writerows(all_results)
    print(f"📄 CSV saved → {filename_csv}")
    return filename_csv

def save_json(all_results, header, site_name, pesquisa, today_str):
    folder = output_dir()
    filename_json = os.path.join(folder, f"{pesquisa}_{site_name}_jobs_{today_str}.json")
    json_data = [dict(zip(header, row)) for row in all_results]
    with open(filename_json, "w", encoding="utf-8") as jf:
        json.dump(json_data, jf, indent=2, ensure_ascii=False)
    print(f"📑 JSON saved → {filename_json}")
    return filename_json