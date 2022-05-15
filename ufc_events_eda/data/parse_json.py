import json
from pathlib import Path
import pandas as pd


def parse_json(path: Path) -> pd.DataFrame:
    """Parse a JSON file into a pandas DataFrame"""
    with open(path, "r") as f:
        data = json.loads(f.read())

    return pd.json_normalize(
        data, record_path="fights", meta=["event_name", "event_date", "event_location"]
    )
