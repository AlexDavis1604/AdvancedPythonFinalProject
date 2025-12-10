import numpy as np

class CryptoAnalyzer:
    def __init__(self, df):
        self.df = df

    def get_daily_returns(self):
        return self.df["Close"].pct_change().dropna() * 100

    # def compute_volatility(self):
    #     return np.std(self.df['Return'].dropna())

    # def get_price_stats(self):
    #     return {
    #         "max_price": self.df['Close'].max(),
    #         "min_price": self.df['Close'].min(),
    #         "average_price": self.df['Close'].mean()
    #     }

    # # Recursive peak finder
    # def recursive_find_peak(self, prices, index=1):
    #     if index >= len(prices) - 1:
    #         return None  
    #     if prices[index] > prices[index - 1] and prices[index] > prices[index + 1]:
    #         return index
    #     return self.recursive_find_peak(prices, index + 1)