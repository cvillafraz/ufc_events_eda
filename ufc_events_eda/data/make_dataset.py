import logging
import time
import requests
import pandas as pd
from scrapinghub import ScrapinghubClient
from config import cloud_config

logging.basicConfig(level=10)


def run_spider_job() -> str:
    client = ScrapinghubClient(cloud_config["API_KEY"])
    spider = client.get_project(580548).spiders.get("ufc_spider")
    job = spider.jobs.run()
    while not job.metadata.get("state") == "finished":
        logging.info("Waiting for spider job to finish")
        time.sleep(60)
    return job.key


def get_data(job_key: str):
    url = f'https://storage.scrapinghub.com/items/{job_key}?apikey={cloud_config["API_KEY"]}&format=json&saveas=ufc_events.json'
    res = requests.get(url)
    with open("save.json", "w", encoding="utf-8") as f:
        f.write(res.content.decode("utf-8"))


if __name__ == "__main__":
    job_key = run_spider_job()
    get_data("job_key")
