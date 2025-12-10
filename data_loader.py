import os
import glob
import pandas as pd

class CryptoDataLoader:
    def load_all_datasets(self, data_dir='data'):
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