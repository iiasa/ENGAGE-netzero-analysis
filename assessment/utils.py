import pandas as pd
from pyam import IamDataFrame


def get_netzero_data(df, meta, default_year):
    """Reformat an IamDataFrame selecting the year via a meta column"""

    lst = []

    # iterate over scenarios and retrieve timeseries data for the year given by `meta`
    for model, scenario in df.index:
        try:
            y = int(df.meta.loc[(model, scenario), meta])
        except ValueError:
            y = default_year

        _df = df.filter(model=model, scenario=scenario)
        _df.interpolate(y, inplace=True)
        lst.append(_df.filter(year=y)._data)

    # concatenate single-year timeseries data and cast to IamDataFrame
    data = pd.concat(lst).reset_index()
    data.year = 0
    return IamDataFrame(data)