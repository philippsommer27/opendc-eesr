import pandas as pd
import json
from entsoe import mappings
from analysis import cached_query_generation, cached_query_crossborder_flows, cached_query_wind_and_solar_forecast, ensure_freq

class GridAnalysis:

    def __init__(self, 
    df_dc:pd.DataFrame,
    start: pd.Timestamp,
    end: pd.Timestamp,
    key_path,
    country='NL',
    true_time=True,
    freq='15T',
    caching=True,
    green_ratio=None,
    ) -> None:
        self.df_dc = df_dc
        self.start = start
        self.end = end
        self.key_path = key_path
        self.country = country
        self.freq = freq
        self.caching = caching
        self.green_ratio=green_ratio
        self.df = self.fetch_energy_prod(country, get_bordering=True)
        self.df = self.df.fillna(0)
        self.df.loc[:, (self.df != 0).any(axis=0)]    

        self.merge_dc_grid(true_time=true_time)

    def calc_total_prod(self):
        if 'total_prod' in self.df:
            self.df.drop('total_prod', axis=1, inplace=True)

        self.df['total_prod'] = self.df.loc[:, self.df.columns.isin(list(PROD_CAT))].sum(axis=1)

    def _fetch_cross_border(self, df):

        for neighbour_code in mappings.NEIGHBOURS[self.country]:
            # print("Doing neighbour", neighbour_code)
            neighbour_flow = cached_query_crossborder_flows(self.country, neighbour_code, self.start, self.end, self.key_path, self.caching)
            if neighbour_flow is None or neighbour_flow.sum() == 0:
                print("Skipping neighbour...")
                continue
            neighbour_flow = ensure_freq(neighbour_flow, self.freq)

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

            df = df.fillna(0)
            df.loc[:, (df != 0).any(axis=0)]         

    def fetch_energy_prod(self, country, get_bordering=True):
        
        df = cached_query_generation(country, self.start, self.end, self.key_path, self.caching)

        # Cleanup
        
        df = df.fillna(0)
        df.loc[:, (df != 0).any(axis=0)]        

        df.drop(list(df.filter(regex = 'Consumption')), axis = 1, inplace = True)

        try:
            df.columns = df.columns.droplevel(-1)
        except:
            print("Only one level for prod fetch")

        df = ensure_freq(df, self.freq)

        if get_bordering:
            self._fetch_cross_border(df)
        
        return df

    def merge_dc_grid(self, true_time: bool):
        # print(f"GRID {self.df.index[0]} - {self.df.index[-1]}")
        # print(f"DC {self.df_dc.index[0]} - {self.df_dc.index[-1]}")

        assert abs(len(self.df) - len(self.df_dc)) < 100, f"Timeframes do not match: GRID {len(self.df)} DC {len(self.df_dc)}"

        #Truncate to match timeframe
        diff = abs(len(self.df) - len(self.df_dc))
        if len(self.df) > len(self.df_dc):
            self.df.drop(self.df.tail(len(diff).index, inplace = True))
        elif len(self.df) < len(self.df_dc):
            self.df_dc.drop(self.df_dc.tail( diff).index, inplace = True)
            
        assert len(self.df) == len(self.df_dc), f"Timeframes do not match: GRID {len(self.df)} DC {len(self.df_dc)}"

        if not true_time:
            assert self.df.index[0] == self.df_dc.index[0], "DC start time does not match grid start time" 
            assert self.df.index[-1] == self.df_dc.index[-1], "DC end time does not match grid end time"
            self.df = pd.concat([self.df, self.df_dc], axis=1)

        self.df['dc_power_total'] = self.df_dc.iloc[:,0].to_numpy()
        self.df['it_power_total'] = self.df_dc.iloc[:,1].to_numpy()

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
                prod_type = column[8:]
                if PROD_CAT[prod_type]['renewable']:
                    self.df['dc_renewable_total'] += self.df[column]
                else:
                    self.df['dc_non_renewable_total'] += self.df[column]


                if PROD_CAT[prod_type]['green']:
                    self.df['dc_green_total'] += self.df[column]
                else:
                    self.df['dc_non_green_total'] += self.df[column]


    def compute_dc_cons_by_type(self):
        assert 'dc_power_total' in self.df, "Dataframe does not contain data center power consumption, consider calling merge_dc_grid()"
        
        self.calc_total_prod()
        

        #Calc based on assumed 'greeness'
        if self.green_ratio is not None:
            difference_ren = self.green_ratio - self.df['renewable_perc']
            difference_non_ren = 1 - difference_ren
            assert not any(difference_ren<0), "Not all time entries had less than green_ratio"
            assert not any(difference_non_ren<0), "Not all time entries had less than green_ratio"
            
            self.df['temp_total'] = 0 

            for column in self.df.columns:
                if column in PROD_CAT.keys():
                    ratio = self.df[column] / self.df['total_prod']
                    if PROD_CAT[column]['renewable']:
                        new_ratio = (((ratio * difference_ren) / self.df['renewable_perc']) + ratio)
                        self.df['dc_cons_' + column] = new_ratio * self.df['dc_power_total']
                    else:
                        new_ratio = (ratio - ((ratio * difference_non_ren) / self.df['non_renewable_perc']))
                        self.df['dc_cons_' + column] =  new_ratio * self.df['dc_power_total']

                    self.df['temp_total'] += self.df['dc_cons_' + column]
            print(self.df['dc_power_total'].head(10))
            print(self.df['temp_total'].head(10))
        #Naive
        else:
            for column in self.df.columns:
                if column in PROD_CAT.keys():
                    self.df['dc_cons_' + column] = (self.df[column] / self.df['total_prod']) * self.df['dc_power_total']

    def compute_apcren(self):
        assert 'dc_power_total' in self.df, "Dataframe does not contain DC power usage" 
        assert 'renewable_total' in self.df, "Dataframe does not contain grid renewable consumption" 

        dc_sum_consumption_mw = self.df['dc_power_total'] / 1000
        grid_sum_renewable_production = self.df['renewable_total']
        K = dc_sum_consumption_mw.sum() / grid_sum_renewable_production.sum()
       
        numerator = abs((K * grid_sum_renewable_production) - dc_sum_consumption_mw)
        APCren = 1 - (numerator.sum() / dc_sum_consumption_mw.sum())

        return APCren


    def compute_total_co2(self, assume='best'):
        if assume == 'best':
            co2_df = pd.read_csv("analysis/data/LCA_CO2_BEST.csv")
        elif assume == 'worst':
            co2_df = pd.read_csv("analysis/data/LCA_CO2_Worst.csv")

        self.df['total_co2'] = 0

        for column in self.df.columns:
            if 'dc_cons_' in column:
                self.df['total_co2'] = self.df['total_co2'] + (co2_df.loc[co2_df['TYPE'] == column[8:], 'CO2 [gCO2/kWh]'].values[0] * self.df[column])

        return self.df['total_co2'].sum() / 1000
  
    def compute_gec_green(self):
        return self.df['dc_green_total'].sum() / self.df['dc_power_total'].sum()

    def compute_gec_renewable(self):
        return self.df['dc_renewable_total'].sum() / self.df['dc_power_total'].sum()

    def compute_cue(self):
        self.df['cue'] = self.df['total_co2'] / self.df['it_power_total']

        return self.df['cue'].mean()
    
    def compute_total_power(self):
        return self.df['dc_power_total'].sum() / 1000

    def analyze(self, out, assume='best'):
        self.compute_energy_prod_ratios()
        self.compute_dc_cons_by_type()
        self.compute_dc_energy_prod_ratios()
        APCren = self.compute_apcren()
        CO2 = self.compute_total_co2(assume)
        GEC = self.compute_gec_renewable()
        CUE = self.compute_cue()
        power = self.compute_total_power()

        res = {
            "builtin_metrics" : {
                "CO2" : CO2,
                "GEC" : GEC,
                "APCr" : APCren,
                "CUE" : CUE
            },
            "domain" : [
                {
                    "name" : "Total Energy Use (MWh)",
                    "value" : power
                }
            ]
        }

        with open(out, 'w') as fp:
            json.dump(res, fp)

def fetch_generation_forecast_csv(start: pd.Timestamp, end: pd.Timestamp, out, key, country='NL', freq='15Min', caching=True):

    df = cached_query_wind_and_solar_forecast(country_code=country, start=start, end=end, key_path=key, caching=caching)
    df = ensure_freq(df, freq)
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
    'Waste' : {'renewable' : False, 'green' : False},
    'Wind Offshore' : {'renewable' : True, 'green' : True},
    'Wind Onshore' : {'renewable' : True, 'green' : True},
    'Other' : {'renewable' : False, 'green' : False},
}

if __name__ == "__main__":
    pass