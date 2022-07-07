import pandas as pd
from entsoe import mappings
from analysis import cached_query_generation, cached_query_crossborder_flows, cached_query_wind_and_solar_forecast

class GridAnalysis:

    def __init__(self, df_dc, start: pd.Timestamp, end: pd.Timestamp, key_path, country='NL', true_time=True) -> None:
        self.df_dc = df_dc
        self.start = start
        self.end = end
        self.key_path = key_path
        self.country = country
        self.df = self.fetch_energy_prod(country)
        self.merge_dc_grid(true_time=true_time)

    def calc_total_prod(self):
        if 'total_prod' in self.df:
            self.df.drop('total_prod', axis=1, inplace=True)

        self.df['total_prod'] = self.df.loc[:, self.df.columns.isin(list(PROD_CAT))].sum(axis=1)

    def _fetch_cross_border(self, df):

        for neighbour_code in mappings.NEIGHBOURS[self.country]:
            neighbour_flow = cached_query_crossborder_flows(self.country, neighbour_code, self.start, self.end, self.key_path)
            if neighbour_flow is None:
                continue
            
            neighbour_prod = self.fetch_energy_prod(neighbour_code, False)

            assert neighbour_flow.shape[0] == neighbour_prod.shape[0], f"Fetch Border Error: {neighbour_flow.shape[0]} and {neighbour_prod.shape[0]} do not match" 
            
            columns = neighbour_prod.columns
            neighbour_prod['total_prod'] = neighbour_prod.sum(axis=1)

            for column in columns:
                neighbour_prod[column + '_perc'] = neighbour_prod[column] / neighbour_prod['total_prod']
                neighbour_prod[column + '_flow'] = neighbour_prod[column + '_perc'] * neighbour_flow

                if column in df.columns:
                    df[column] = df[column] + neighbour_prod[column + '_flow']
                else:
                    df[column] = neighbour_prod[column + '_flow']
        

    def fetch_energy_prod(self, country, get_bordering=True):
        
        df = cached_query_generation(country, self.start, self.end, self.key_path)

        # Cleanup

        df = df.fillna(0)
        df.loc[:, (df != 0).any(axis=0)]
        df.drop(list(df.filter(regex = 'Consumption')), axis = 1, inplace = True)

        df.columns = df.columns.droplevel(-1)

        if get_bordering:
            self._fetch_cross_border(df)

        return df

    def merge_dc_grid(self, true_time: bool):
        assert len(self.df) == len(self.df_dc), "Timeframes do not match"
        if not true_time:
            assert self.df.index[0] == self.df_dc.index[0], "DC start time does not match grid start time" 
            assert self.df.index[-1] == self.df_dc.index[-1], "DC end time does not match grid end time"
            self.df = pd.concat([self.df, self.df_dc], axis=1)

        self.df['dc_total_power'] = self.df_dc['dc_total_power']
        self.df['it_total_power'] = self.df_dc['it_total_power']


    def compute_energy_prod_ratios(self):
        columns = self.df.columns

        self.calc_total_prod()

        self.df['renewable_total'] = 0
        self.df['non_renewable_total'] = 0
        self.df['green_total'] = 0
        self.df['non_green_total'] = 0

        for column in columns:
            if column in PROD_CAT.keys():
                if PROD_CAT[column]['renewable']:
                    self.df['renewable_total'] += self.df[column]
                else:
                    self.df['non_renewable_total'] += self.df[column]

                if PROD_CAT[column]['green']:
                    self.df['green_total'] += self.df[column]
                else:
                    self.df['non_green_total'] += self.df[column]

        self.df['renewable_perc'] = self.df['renewable_total'] / self.df['total_prod']
        self.df['non_renewable_perc'] = self.df['non_renewable_total'] / self.df['total_prod']
        self.df['green_perc'] = self.df['green_total'] / self.df['total_prod']
        self.df['non_green_perc'] = self.df['non_green_total'] / self.df['total_prod']


    def compute_dc_energy_prod_ratios(self):
        columns = self.df.columns

        self.calc_total_prod()

        self.df['dc_renewable_total'] = 0
        self.df['dc_non_renewable_total'] = 0
        self.df['dc_green_total'] = 0
        self.df['dc_non_green_total'] = 0

        for column in columns:
            if 'dc_cons_' in column:
                prod_type = column[8:-1]
                if PROD_CAT[prod_type]['renewable']:
                    self.df['dc_renewable_total'] += self.df[column]
                else:
                    self.df['dc_non_renewable_total'] += self.df[column]


                if PROD_CAT[prod_type]['green']:
                    self.df['dc_green_total'] += self.df[column]
                else:
                    self.df['dc_non_green_total'] += self.df[column]


    def compute_dc_cons_by_type_naive(self):
        assert 'dc_power_total' in self.df, "Dataframe does not contain data center power consumption, consider calling merge_dc_grid()"

        self.calc_total_prod()

        for column in self.df.columns:
            if column in PROD_CAT.keys():
                self.df['dc_cons_' + column] = (self.df[column] / self.df['total_prod']) * self.df['dc_power_total']

    def compute_apcren(self):
        assert 'dc_power_total' in self.df, "Dataframe does not contain DC power usage" 
        assert 'renewable_total' in self.df, "Dataframe does not contain grid renewable consumption" 

        dc_sum_consumption_mw = self.df['dc_power_total'] / 1000
        grid_sum_renewable_production = self.df['renewable_total']
        K = dc_sum_consumption_mw.sum() / grid_sum_renewable_production.sum()
        
        numerator = abs((K * grid_sum_renewable_production) - dc_sum_consumption_mw).sum()
        APCren = 1 - (numerator / dc_sum_consumption_mw)

        return APCren


    def compute_total_co2(self, assume):
        if assume == 'best':
            co2_df = pd.read_csv("opendc-eesr/analysis/data/LCA_CO2_BEST.csv")
        elif assume == 'worst':
            co2_df = pd.read_csv("opendc-eesr/analysis/data/LCA_CO2_Worst.csv")

        self.df['total_co2'] = 0

        for column in self.df.columns:
            if 'dc_cons_' in column:
                self.df['total_co2'] = self.df['total_co2'] + (co2_df.loc[[column[8:-1], 'CO2 [gCO2/kWh]']] * self.df[column])

        return self.df['total_co2'].sum()
  

    def compute_power_cost(self):
        pass


    def compute_gec_green(self):
        return self.df['cd_green_total'].sum() / self.df['dc_power_total'].sum()

    def compute_gec_renewable(self):
        return self.df['dc_renewable_total'].sum() / self.df['dc_power_total'].sum()

    def compute_cue(self):
        self.df['cue'] = self.df['total_co2'] / self.df['it_power_total']

        return self.df['cue'].mean()

    def compute_nenr(self):
        pass

    def analyze(self, out):
        self.fetch_energy_prod()
        self.compute_dc_cons_by_type_naive()
        self.compute_energy_prod_ratios()
        self.compute_dc_energy_prod_ratios()
        APCren = self.compute_apcren()
        CO2 = self.compute_total_co2()
        GEC = self.compute_gec_renewable()
        CUE = self.compute_cue

        res = {
            "builtin_metrics" : {
                "CO2" : CO2,
                "GEC" : GEC,
                "APCr" : APCren,
                "CUE" : CUE
            }
        }

        return res



def fetch_generation_forecast_csv(start: pd.Timestamp, end: pd.Timestamp, out, country='NL'):

    df = cached_query_wind_and_solar_forecast(country_code=country, start=start, end=end)
    df = df.fillna(0)

    df.to_csv(out)

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

    grid_analysis = GridAnalysis()