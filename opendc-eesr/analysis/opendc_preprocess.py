import pandas as pd
import numpy as np
from datetime import timedelta

def process(path, offset_time=None, PUE=1):

    joule_to_kWh = lambda x: np.longdouble(x / (3.6e6))

    df = pd.read_csv(path)

    df = df.groupby(['timestamp']).agg(
        {
            'it_power_total':sum,
        }
    )

    df.reset_index(inplace=True)

    if offset_time is not None:
        df['timestamp'] = df['timestamp'] + (pd.Timestamp(offset_time).timestamp() * 1000)
    
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    df['it_power_total'] = joule_to_kWh(df['it_power_total'])

    df['dc_power_total'] = df['dc_power_total'] * PUE

    df.set_index('timestamp', inplace=True)

    return df