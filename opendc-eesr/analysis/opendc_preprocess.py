import pandas as pd
import numpy as np
from datetime import timedelta

def process(path, offset_time=None):

    joule_to_kWh = lambda x: np.longdouble(x / (3.6e6))

    df = pd.read_csv(path)

    df = df.groupby(['timestamp']).agg(
        {
            'power_total':sum,
            'power_usage':sum,
        }
    )

    if offset_time is not None:
        df['timestamp'] = pd['timestamp'] + (pd.Timestamp(offset_time).timestamp * 1000)
    
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    df['power_total'] = joule_to_kWh(df['power_total'])