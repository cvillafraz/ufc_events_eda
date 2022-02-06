import logging
import requests
import ufc_events_eda.utils.paths as path
from scrapinghub import ScrapinghubClient
from config import cloud_config

logging.basicConfig(level=10)


def _get_last_job_key() -> str:
    client = ScrapinghubClient(cloud_config["API_KEY"])
    spider = client.get_project(580548).spiders.get("ufc_spider")
    return list(spider.jobs.iter_last())[0].get("key")


def get_data():
    job_key = _get_last_job_key()
    url = f'https://storage.scrapinghub.com/items/{job_key}?apikey={cloud_config["API_KEY"]}&format=json&saveas=ufc_events.json'
    res = requests.get(url)
    raw_path = path.data_raw_dir("ufc_events.json")
    if res.status_code == 200:
        with open(raw_path, "w", encoding="utf-8") as f:
            f.write(res.content.decode("utf-8"))
            logging.info(f"Saved file to path {raw_path}")


if __name__ == "__main__":
    get_data()
