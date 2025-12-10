import os
import glob
import pandas as pd

class CryptoDataLoader:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = None

    def load_data(self):
        self.data = pd.read_csv(self.filepath)
        self.data.columns = [
            "Index", "Name", "Symbol", "Date",
            "Open", "High", "Low", "Close",
            "Volume", "Marketcap"
        ]
        self.data['Date'] = pd.to_datetime(self.data['Date'])
        return self.data
    
    def clean_data(self):
        self.data = self.data.dropna()
        return self.data
    
    def align_data(self, df1, df2):
        df1 = df1.set_index('Date')['Close'].sort_index()
        df2 = df2.set_index('Date')['Close'].sort_index()

        start = max(df1.index.min(), df2.index.min())
        end = min(df1.index.max(), df2.index.max())

        df1 = df1.loc[start:end]
        df2 = df2.loc[start:end]

        return df1, df2
    
    def get_closing_prices(self):
        dates_np = self.data["Date"].to_numpy()
        close_np = self.data["Close"].to_numpy(dtype=float)
        return dates_np, close_np
    

def load_all_datasets(data_dir='data'):
    pattern = os.path.join(data_dir, 'coin_*.csv')
    files = sorted(glob.glob(pattern)) 
    # The glob module finds pathnames using pattern matching rules
    # Never used this before, useful for this application
    datasets = {}

    for fp in files:
        try:
            df = pd.read_csv(fp)
        except Exception:
            # Skips unreadable files
            continue

        df.columns = [
            "Index", "Name", "Symbol", "Date",
            "Open", "High", "Low", "Close",
            "Volume", "Marketcap"
        ]

        df['Date'] = pd.to_datetime(df['Date'])
        df = df.dropna()

        base = os.path.splitext(os.path.basename(fp))[0]
        key = base.replace('coin_', '')
        datasets[key] = df

    return datasets
    
