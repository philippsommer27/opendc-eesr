import pandas as pd
from entsoe import mappings
from entsoe_caching import cached_query_generation, cached_query_crossborder_flows, cached_query_wind_and_solar_forecast

def calc_total_prod(df: pd.DataFrame):
    if 'total_prod' in df:
        df.drop('total_prod', axis=1, inplace=True)

    df['total_prod'] = df.loc[:, df.columns.isin(list(PROD_CAT))].sum(axis=1)

def _fetch_cross_border(df: pd.DataFrame, key_path, country, start: pd.Timestamp, end:pd.Timestamp):

    for neighbour_code in mappings.NEIGHBOURS['country']:
        neighbour_flow = cached_query_crossborder_flows(country, neighbour_code, start, end)
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
        

def fetch_energy_prod(start: pd.Timestamp, end: pd.Timestamp, key_path, country='NL', get_bordering=True):
    
    df = cached_query_generation(country, start, end, key_path)

    # Cleanup

    df = df.fillna(0)
    df.loc[:, (df != 0).any(axis=0)]
    df.drop(list(df.filter(regex = 'Consumption')), axis = 1, inplace = True)

    df.columns = df.columns.droplevel(-1)

    if get_bordering():
        _fetch_cross_border(df, country, start, end)

    return df

def fetch_generation_forecast_csv(start: pd.Timestamp, end: pd.Timestamp, key_path, out, country='NL'):

    df = cached_query_wind_and_solar_forecast(country_code=country, start=start, end=end)
    df = df.fillna(0)

    df.to_csv(out)

def merge_dc_grid(df_grid: pd.DataFrame, df_dc: pd.DataFrame):
    assert(df_grid.index[0] == df_dc.index[0], "DC start time does not match grid start time")
    assert(df_grid.index[-1] == df_dc.index[-1], "DC end time does nto match grid end time")
    pass

def compute_energy_prod_ratios(df: pd.DataFrame):
    columns = df.columns()

    calc_total_prod(df)

    df['renewable_total'] = 0
    df['non_renewable_total'] = 0
    df['green_total'] = 0
    df['non_green_total'] = 0

    for column in columns:
        if column in PROD_CAT.keys():
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


def compute_dc_energy_prod_ratios(df: pd.DataFrame):
    columns = df.columns()

    calc_total_prod(df)

    df['dc_renewable_total'] = 0
    df['dc_non_renewable_total'] = 0
    df['dc_green_total'] = 0
    df['dc_non_green_total'] = 0

    for column in columns:
        if 'dc_cons_' in column:
            prod_type = column[8:-1]
            if PROD_CAT[prod_type]['renewable']:
                df['dc_renewable_total'] += df[column]
            else:
                df['dc_non_renewable_total'] += df[column]


            if PROD_CAT[prod_type]['green']:
                df['dc_green_total'] += df[column]
            else:
                df['dc_non_green_total'] += df[column]



def compute_dc_cons_by_type_naive(df: pd.DataFrame):
    assert('dc_power_total' in df, "Dataframe does not contain data center power consumption, consider calling merge_dc_grid()")

    calc_total_prod(df)

    for column in df.columns():
        if column in PROD_CAT.keys():
            df['dc_cons_' + column] = (df[column] / df['total_prod']) * df['dc_power_total']

def compute_apcren(df: pd.DataFrame):
    assert('dc_power_total' in df, "Dataframe does not contain DC power usage")
    assert('renewable_total' in df, "Dataframe does not contain grid renewable consumption")

    dc_sum_consumption_mw = df['dc_power_total'] / 1000
    grid_sum_renewable_production = df['renewable_total']
    K = dc_sum_consumption_mw.sum() / grid_sum_renewable_production.sum()
    
    numerator = abs((K * grid_sum_renewable_production) - dc_sum_consumption_mw).sum()
    APCren = 1 - (numerator / dc_sum_consumption_mw)

    return APCren


def compute_total_co2(df: pd.DataFrame, assume):
    if assume == 'best':
        co2_df = pd.read_csv("opendc-eesr/analysis/data/LCA_CO2_BEST.csv")
    elif assume == 'worst':
        co2_df = pd.read_csv("opendc-eesr/analysis/data/LCA_CO2_Worst.csv")

    df['total_co2'] = 0

    for column in df.columns():
        if 'dc_cons_' in column:
            df['total_co2'] = df['total_co2'] + (co2_df.loc[[column[8:-1], 'CO2 [gCO2/kWh]']] * df[column])

    return df['total_co2'].sum()
   

def compute_power_cost(df: pd.DataFrame):
    pass

def compute_gec_green(df: pd.DataFrame):
    return df['cd_green_total'].sum() / df['dc_power_total'].sum()

def compute_gec_renewable(df: pd.DataFrame):
    return df['dc_renewable_total'].sum() / df['dc_power_total'].sum()

def compute_cue(df: pd.DataFrame):
    df['cue'] = df['total_co2'] / df['it_power_total']

    return df['cue'].mean()

def compute_nenr():
    pass

def compute_sustainability_metrics(df: pd.DataFrame, out):
    pass

def save_df():
    pass

PROD_CAT = {
    'Mixed' : {'renewable' : False, 'green' : False},
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
}

if __name__ == "__main__":
    start = pd.Timestamp('20181123', tz='Europe/Amsterdam')
    end = pd.Timestamp('20190111', tz='Europe/Amsterdam')
    fetch_energy_prod(start, end, key_path="G:\My Drive\VU Amsterdam\Year 3\Bachelor Project\entsoe_token.txt")

