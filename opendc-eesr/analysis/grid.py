import pandas as pd
from entsoe import EntsoePandasClient, mappings
from pyparsing import col

def get_key(path):
    with open(path, "r") as file:
        return file.read().strip()


def fetch_energy_prod_type(start_time, end_time, key_path, timezone='Europe/Amsterdam', country_code='NL'):
    client = EntsoePandasClient(api_key=get_key(key_path))

    start = pd.Timestamp(start_time, tz=timezone)
    end = pd.Timestamp(end_time, tz=timezone)
    
    df = client.query_generation(country_code, start=start, end=end)

    # Cleanup

    df = df.fillna(0)
    df.loc[:, (df != 0).any(axis=0)]
    df.drop(list(df.filter(regex = 'Consumption')), axis = 1, inplace = True)

    df.columns = df.columns.droplevel(-1)

    df['total_prod'] = df.sum(axis=1)

    return df

def add_cross_border():
    pass

def calc_additional_energy_prod(df: pd.DataFrame):
    columns = df.columns()

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



if __name__ == "__main__":
    fetch_energy_prod_type(start_time='20181123', end_time='20190111', key_path="G:\My Drive\VU Amsterdam\Year 3\Bachelor Project\entsoe_token.txt")


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