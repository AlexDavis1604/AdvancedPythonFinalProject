from typing import Dict, Optional, Union

import numpy as np
import pandas as pd


class DataProcessor:
    def __init__(self, data, name: Optional[str] = None):
        if isinstance(data, pd.DataFrame):
            if name is None:
                name = "series"
            self.data: Dict[str, pd.DataFrame] = {name: data.copy()}
        else:
            # shallow copy to avoid mutating caller's frames
            self.data = {k: v.copy() for k, v in data.items()}

        self.validate_inputs()

    def validate_inputs(self):
        for key, df in list(self.data.items()):
            if "Date" in df.columns:
                df = df.copy()
                df["Date"] = pd.to_datetime(df["Date"])
                df.set_index("Date", inplace=True)
            else:
                raise ValueError(f"DataFrame for '{key}' must have a DatetimeIndex or a 'Date' column")

            df = df.sort_index()
            self.data[key] = df

    def align_datasets(self, join: str = "inner") -> pd.DataFrame:
        series_list = []
        for name, df in self.data.items():
            series = df["Close"].rename(name)
            series_list.append(series)

        if not series_list:
            return pd.DataFrame()

        aligned = pd.concat(series_list, axis=1, join=join)
        return aligned

    def convert_to_returns(self, df, method: str = "simple", percent: bool = False) -> pd.DataFrame:
        if df is None:
            df = self.align_datasets()

        if method == "simple":
            rets = df.pct_change()
        elif method == "log":
            rets = np.log(df).diff()
        else:
            raise ValueError("Unknown return method. Use 'simple' or 'log'.")

        if percent:
            rets = rets * 100

        return rets.dropna(how="all")

    def aligned_returns(self, how: str = "inner", method: str = "simple", percent: bool = False) -> pd.DataFrame:
        aligned = self.align_datasets(how=how)
        return self.convert_to_returns(aligned, method=method, percent=percent)

    def prepare_series(self, name: str, start: Optional[str] = None, end: Optional[str] = None, returns: bool = False, method: str = "simple", percent: bool = False, fill_method: Optional[str] = None) -> pd.Series:
        if name not in self.data:
            raise KeyError(f"No series named '{name}' loaded into processor")

        s = self.data[name]["Close"].copy()

        if start or end:
            s = s.loc[start:end]

        if fill_method:
            s = s.fillna(method=fill_method)

        if returns:
            if method == "simple":
                out = s.pct_change()
            elif method == "log":
                out = np.log(s).diff()
            else:
                raise ValueError("Unknown return method. Use 'simple' or 'log'.")

            if percent:
                out = out * 100

            return out.dropna()

        return s