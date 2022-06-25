import pandas as pd
from entsoe import EntsoePandasClient
import os

def get_key(path):
    with open(path, "r") as file:
        return file.read().strip()


def fetch_energy_production_type(start_time, end_time, key_path, timezone='Europe/Amsterdam', country_code='NL', ):
    client = EntsoePandasClient(api_key=get_key(key_path))

    start = pd.Timestamp(start_time, tz=timezone)
    end = pd.Timestamp(end_time, tz=timezone)
    
    df = client.query_generation(country_code, start=start, end=end)

    # Cleanup

    df.loc[:, (df != 0).any(axis=0)]
    df.drop(list(df.filter(regex = 'Consumption')), axis = 1, inplace = True)

    df.columns = df.columns.droplevel(-1)

    return df


def analyze_sustainability_naive(df):
    pass

if __name__ == "__main__":
    fetch_energy_production_type(start_time='20181123', end_time='20190111', key_path="G:\My Drive\VU Amsterdam\Year 3\Bachelor Project\entsoe_token.txt")