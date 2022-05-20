import ufc_events_eda.utils.paths as path
from ufc_events_eda.data.parse_json import parse_json
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter


def _geocode_df_cities(df: pd.DataFrame) -> pd.DataFrame:
    """Generate latitude and longitude for each city in a dataframe."""
    lat, lon = [], []
    for city in df["event_location"]:
        geocoded = _geocode_city(city)
        lat.append(geocoded[0])
        lon.append(geocoded[1])
    df["latitude"] = lat
    df["longitude"] = lon
    return df


def _geocode_city(city: str) -> tuple[float, float]:
    """Return latitude and longitude from a city."""
    geocoder = Nominatim(user_agent="ufc_events_eda")
    geocode = RateLimiter(geocoder.geocode, min_delay_seconds=1)
    geocoded = geocode(city)
    return geocoded.latitude, geocoded.longitude


def main():
    """Read raw dataframe, geocode cities, and save geocoded cities dataframe."""
    df = parse_json(path.data_raw_dir("ufc_events.json"))
    df_city = pd.DataFrame(
        data=df[df["event_location"].str.contains("USA")]["event_location"].unique(),
        columns=["event_location"],
    )
    df_city = _geocode_df_cities(df_city)
    df_city.to_parquet(path.data_interim_dir("cities.parquet"))


if __name__ == "__main__":
    main()
