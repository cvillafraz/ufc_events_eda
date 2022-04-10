import json
import pandas as pd


def parse_json(path):
    with open(path, "r") as f:
        data = json.loads(f.read())

    return pd.json_normalize(
        data, record_path="fights", meta=["event_name", "event_date", "event_location"]
    )
