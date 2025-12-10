from data_loader import CryptoDataLoader
from analyzer import CryptoAnalyzer
from visualizer import CryptoVisualizer
import numpy as np

# Data Source:
# https://www.kaggle.com/datasets/sudalairajkumar/cryptocurrencypricehistory?resource=download

crypto_symbols = ["AAVE", "BNB", "BTC", "ADA", "LINK", "ATOM", "CRO", "DOGE", "EOS", "ETH", "MIOTA", "LTC", "XMR", "XEM", "DOT", "SOL", "XLM", "USDT", "TRX", "UNI", "USDC", "WBTC", "XRP"]
viz = CryptoVisualizer()

def recursive_menu():

    while True:
        print("Select Option:\n0) Quit\n1) View Price Chart\n2) View Volume Chart\n3) Compare Cryptocurreny Price Chart (Log Scale)\n4) Compare Cryptocurreny Performance")
        choice = input("Type Selection: ")
        
        if choice == "0":
            return
        
        elif choice == "1":
            price_chart()
        
        elif choice == "2":
            volume_chart()

        elif choice == "3":
            price_chart_comparison()

        elif choice == "4":
            price_performance_comparison()

def price_chart():
    print("\nOptions:")
    print(*crypto_symbols, sep=', ')

    symbol = input("Type symbol of desired cryptocurrency: ")

    symbol = symbol.strip().upper()

    loader = CryptoDataLoader(f"data/coin_{symbol}.csv")

    df = loader.load_data()
    df = loader.clean_data()

    symbol_name = df['Symbol'].iloc[0]
    dates = df['Date']
    prices = df['Close']

    viz.plot_price(dates, symbol_name, prices)

    recursive_menu()

def price_performance_comparison():
    print("\nOptions:")
    print(*crypto_symbols, sep=', ')

    symbol1 = input("Type symbol of first choice: ")
    symbol2 = input("Type symbol of second choice: ")

    symbol1 = symbol1.strip().upper()
    symbol2 = symbol2.strip().upper()

    filepath1 = f"data/coin_{symbol1}.csv"
    filepath2 = f"data/coin_{symbol2}.csv"

    loader1 = CryptoDataLoader(filepath1)
    df1 = loader1.load_data()
    df1 = loader1.clean_data()

    loader2 = CryptoDataLoader(filepath2)
    df2 = loader2.load_data()
    df2 = loader2.clean_data()

    s1 = df1.set_index('Date')['Close'].sort_index()
    s2 = df2.set_index('Date')['Close'].sort_index()

    start = max(s1.index.min(), s2.index.min())
    end = min(s1.index.max(), s2.index.max())

    s1 = s1.loc[start:end]
    s2 = s2.loc[start:end]

    r1 = s1.pct_change() * 100
    r2 = s2.pct_change() * 100

    dates = r1.index
    asset1_vals = r1.values
    asset2_vals = r2.values

    viz.plot_compare_asset_performance(dates, asset1_vals, asset2_vals, symbol1, symbol2)

    recursive_menu()
            
def price_chart_comparison():
    print("\nOptions:")
    print(*crypto_symbols, sep=', ')

    symbol1 = input("Type symbol of first choice: ")
    symbol2 = input("Type symbol of second choice: ")

    symbol1 = symbol1.strip().upper()
    symbol2 = symbol2.strip().upper()

    filepath1 = f"data/coin_{symbol1}.csv"
    filepath2 = f"data/coin_{symbol2}.csv"

    loader1 = CryptoDataLoader(filepath1)
    df1 = loader1.load_data()
    df1 = loader1.clean_data()

    loader2 = CryptoDataLoader(filepath2)
    df2 = loader2.load_data()
    df2 = loader2.clean_data()

    df1 = df1.set_index('Date')['Close'].sort_index()
    df2 = df2.set_index('Date')['Close'].sort_index()

    start = max(df1.index.min(), df2.index.min())
    end = min(df1.index.max(), df2.index.max())

    df1 = df1.loc[start:end]
    df2 = df2.loc[start:end]

    # Normalize both series to start at 1.0 (so comparisons are relative)
    df1_norm = df1 / df1.iloc[0]
    df2_norm = df2 / df2.iloc[0]

    # Plot natural-log of normalized prices so both series start at 0
    # Useful for daily data but can cause problems when working on a smaller time frame
    log1 = np.log(df1_norm)
    log2 = np.log(df2_norm)

    dates = df1.index

    viz.plot_compare_log_price(dates, log1.values, log2.values, symbol1, symbol2)

    recursive_menu()

def volume_chart():
    print("\nOptions:")
    print(*crypto_symbols, sep=', ')

    symbol = input("Type symbol of desired cryptocurrency: ")

    symbol = symbol.strip().upper()

    loader = CryptoDataLoader(f"data/coin_{symbol}.csv")

    df = loader.load_data()
    df = loader.clean_data()

    symbol = df['Symbol'].iloc[0]
    dates = df['Date']
    volume = df['Volume']

    viz.plot_volume_barchart(dates, symbol, volume)

    recursive_menu()

def main():
    loader = CryptoDataLoader('data/coin_BTC.csv')
    df = loader.load_data()
    df = loader.clean_data()

if __name__ == '__main__':
    recursive_menu()