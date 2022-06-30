from sqlite3 import Timestamp
import pandas as pd
from entsoe import EntsoePandasClient, mappings
from pyparsing import col

def get_key(path):
    with open(path, "r") as file:
        return file.read().strip()


def _fetch_cross_border(df: pd.DataFrame, key_path, country, start: Timestamp, end:Timestamp):
    client = EntsoePandasClient(api_key=get_key(key_path))

    for neighbour_code in mappings.NEIGHBOURS['country']:
        neighbour_flow = client.query_crossborder_flows(country, neighbour_code, start, end)
        neighbour_prod = fetch_energy_prod(start, end, key_path, neighbour_code)

        assert(neighbour_flow.shape[0] == neighbour_prod.shape[0], "Fetch Border Error: Flow data and production data do not match")
        
        columns = neighbour_prod.columns()
        neighbour_prod['total_prod'] = neighbour_prod.sum(axis=1)

        for column in columns:
            neighbour_prod[column + '_perc'] = neighbour_prod[column] / neighbour_prod['total_prod']
            neighbour_prod[column + '_flow'] = neighbour_prod[column + '_perc'] * neighbour_flow

            if column in df.columns:
                df[column] = df[column] + neighbour_prod[column + '_flow']
            else:
                df[column] = neighbour_prod[column + '_flow']

        df.drop('total_prod', axis=1, inplace=True)
        

def fetch_energy_prod(start: Timestamp, end: Timestamp, key_path, country='NL', get_bordering=False):
    client = EntsoePandasClient(api_key=get_key(key_path))
    
    df = client.query_generation(country, start=start, end=end)

    # Cleanup

    df = df.fillna(0)
    df.loc[:, (df != 0).any(axis=0)]
    df.drop(list(df.filter(regex = 'Consumption')), axis = 1, inplace = True)

    df.columns = df.columns.droplevel(-1)

    if get_bordering():
        _fetch_cross_border(df, client, country, start, end)

    return df

def calc_energy_prod_ratios(df: pd.DataFrame):
    columns = df.columns()

    df['total_prod'] = df.sum(axis=1)

    df['renewable_total'] = 0
    df['non_renewable_total'] = 0
    df['green_total'] = 0
    df['non_green_total'] = 0

    for column in columns:
        if PROD_CAT[column]['renewable']:
            df['renewable_total'] += df[column]
        else:
            df['non_renewable_total'] += df[column]


        if PROD_CAT[column]['green']:
            df['green_total'] += df[column]
        else:
            df['non_green_total'] += df[column]

    df['renewable_perc'] = df['renewable_total'] / df['total_prod']
    df['non_renewable_perc'] = df['non_renewable_total'] / df['total_prod']
    df['green_perc'] = df['green_total'] / df['total_prod']
    df['non_green_perc'] = df['non_green_total'] / df['total_prod']



def fetch_generation_forecast_csv(start: Timestamp, end: Timestamp, key_path, out, country='NL'):
    client = EntsoePandasClient(api_key=get_key(key_path))

    df = client.query_wind_and_solar_forecast(country_code=country, start=start, end=end)
    df.to_csv(out)


def compute_apcren():
    pass

def compute_total_co2():
    pass

def compute_gec():
    pass

def compute_cue():
    pass

def compute_nenr():
    pass

def compute_sustainability_metrics(df: pd.DataFrame, out):
    pass

PROD_CAT = {
    'Mixed' : {'renewable' : False, 'green' : False},
    'Generation' : {'renewable' : False, 'green' : False},
    'Load' : {'renewable' : False, 'green' : False},
    'Biomass' : {'renewable' : True, 'green' : True},
    'Fossil Brown coal/Lignite' : {'renewable' : False, 'green' : False},
    'Fossil Coal-derived gas' : {'renewable' : False, 'green' : False},
    'Fossil Gas' : {'renewable' : False, 'green' : False},
    'Fossil Hard coal' : {'renewable' : False, 'green' : False},
    'Fossil Oil' : {'renewable' : False, 'green' : False},
    'Fossil Oil shale' : {'renewable' : False, 'green' : False},
    'Fossil Peat' : {'renewable' : False, 'green' : False},
    'Geothermal' : {'renewable' : True, 'green' : True},
    'Hydro Pumped Storage' : {'renewable' : True, 'green' : True},
    'Hydro Run-of-river and poundage' : {'renewable' : True, 'green' : True},
    'Hydro Water Reservoir' : {'renewable' : True, 'green' : True},
    'Marine' : {'renewable' : True, 'green' : True},
    'Nuclear' : {'renewable' : False, 'green' : True},
    'Other renewable' : {'renewable' : True, 'green' : True},
    'Solar' : {'renewable' : True, 'green' : True},
    'Waste' : {'renewable' : True, 'green' : True},
    'Wind Offshore' : {'renewable' : True, 'green' : True},
    'Wind Onshore' : {'renewable' : True, 'green' : True},
    'Other' : {'renewable' : False, 'green' : False},
    'AC Link' : {'renewable' : False, 'green' : False},
    'DC Link' : {'renewable' : False, 'green' : False},
    'Substation' : {'renewable' : False, 'green' : False},
    'Transformer' : {'renewable' : False, 'green' : False},
}

if __name__ == "__main__":
    start = pd.Timestamp('20181123', tz='Europe/Amsterdam')
    end = pd.Timestamp('20190111', tz='Europe/Amsterdam')
    fetch_energy_prod(start, end, key_path="G:\My Drive\VU Amsterdam\Year 3\Bachelor Project\entsoe_token.txt")

