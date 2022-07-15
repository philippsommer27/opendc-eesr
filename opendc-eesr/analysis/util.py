from pandas import DataFrame, infer_freq, DateOffset

def ensure_freq(df: DataFrame, wanted_freq):
    freq = infer_freq(df.index)
    if freq != wanted_freq:
        resample(df, wanted_freq)


def resample(df: DataFrame, freq):
    