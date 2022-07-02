from pathlib import Path
import pickle
from entsoe import EntsoePandasClient
from dataclasses import dataclass
from pandas import DataFrame, Timestamp, read_pickle
from requests import get


@dataclass(frozen=True, eq=True)
class CacheEntry:
    doc_type: str
    country_from: str
    start: Timestamp
    end: Timestamp
    country_to: str = None

def get_key(path):
    with open(path, "r") as file:
        return file.read().strip()

def load_map() -> dict:
    file = Path("analysis/cache/cache_map.pkl")

    if file.exists() :
        with open(file, 'rb') as f:
            cache_map = pickle.load(f)
        return cache_map
    else:
        return {}

def store_map(map: dict):
    file = Path("analysis/cache/cache_map.pkl")

    with open(file, 'wb') as f:
        pickle.dump(map, f)

def cache_lookup(query: CacheEntry) -> DataFrame:
    cache_map = load_map()

    res = cache_map.get(query)

    if res is not None:
        return read_pickle(res)

    return res

def cache_entry(query: CacheEntry, res: DataFrame):
    cache = load_map()

    pickle_path = "opendc-eesr/analysis/cache/" + str(abs(query.__hash__())) + ".pkl"
    res.to_pickle(pickle_path)

    cache[query] = pickle_path

    store_map(cache)


def cached_query_generation(country, start: Timestamp, end: Timestamp, key_path):
    query = CacheEntry('A75', country, start, end)
    
    res = cache_lookup(query)

    if res is None:
        client = EntsoePandasClient(api_key=get_key(key_path))

        res = client.query_generation(country, start=start, end=end)
        cache_entry(query, res)

    return res

def cached_query_crossborder_flows(country_from, country_to, start: Timestamp, end: Timestamp, key_path):
    query = CacheEntry('A11', country_from, start, end, country_to)

    res = cache_lookup(query)

    if res is None:
        client = EntsoePandasClient(api_key=get_key(key_path))

        res = client.query_crossborder_flows(country_from, country_to, start, end)
        cache_entry(query, res)

    return res

def cached_query_wind_and_solar_forecast(country, start: Timestamp, end: Timestamp, key_path):
    query = CacheEntry('A69', country, start, end)

    res = cache_lookup(query)

    if res is None:
        client = EntsoePandasClient(api_key=get_key(key_path))

        res = client.query_wind_and_solar_forecast(country, start, end)
        cache_entry(query, res)

    return res