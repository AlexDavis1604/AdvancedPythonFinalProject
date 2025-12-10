from data_loader import load_all_datasets
from analyzer import CryptoAnalyzer
from visualizer import CryptoVisualizer
import numpy as np
import pandas as pd

# Data Source:
# https://www.kaggle.com/datasets/sudalairajkumar/cryptocurrencypricehistory?resource=download

viz = CryptoVisualizer()

datasets = load_all_datasets('data')

def recursive_menu():

    while True:
        print("Select Option:\n0) Quit\n1) View Price Chart\n2) View Volume Chart\n3) Compare Cryptocurreny Price Chart (Log Scale)\n4) Compare Cryptocurreny Performance\n5) Compare Price vs Volume of Cryptocurrency\n6) Compare Cryptocurrency Volatility\n7) View Cryptocurrency Correlation Heatmap")
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

        elif choice == "5":
            price_volume_comparison()

        elif choice == "6":
            volatility_comparison()
        
        elif choice == "7":
            correlation_heatmap()

def build_price_matrix(asset_dict):
    price_frames = []

    for symbol, df in asset_dict.items():
        temp = df[['Date', 'Close']].copy()
        temp['Date'] = pd.to_datetime(temp['Date'])
        temp = temp.set_index('Date').sort_index()
        temp.rename(columns={'Close': symbol}, inplace=True)
        price_frames.append(temp)

    price_matrix = pd.concat(price_frames, axis=1, join='inner')
    return price_matrix

def correlation_heatmap():
    price_matrix = build_price_matrix(datasets)
    viz.plot_crypto_correlation_heatmap(price_matrix)

    recursive_menu()

def price_volume_comparison():
    print("\nOptions:")
    print(', '.join(sorted(datasets.keys())))

    symbol = input("Type symbol of desired cryptocurrency: ")

    symbol = symbol.strip().upper()

    df = datasets.get(symbol)
    if df is None:
        print(f"Dataset for '{symbol}' not found.\n")
        recursive_menu()
        return

    symbol_name = df['Symbol'].iloc[0]
    dates = df['Date']
    prices = df['Close']
    volume = df['Volume']

    viz.plot_volume_vs_price(dates, symbol_name, prices, volume)

    recursive_menu()

def price_chart():
    print("\nOptions:")
    print(', '.join(sorted(datasets.keys())))

    symbol = input("Type symbol of desired cryptocurrency: ")

    symbol = symbol.strip().upper()

    df = datasets.get(symbol)
    if df is None:
        print(f"Dataset for '{symbol}' not found.\n")
        recursive_menu()
        return

    symbol_name = df['Symbol'].iloc[0]
    dates = df['Date']
    prices = df['Close']

    viz.plot_price(dates, symbol_name, prices)

    recursive_menu()

def price_performance_comparison():
    print("\nOptions:")
    print(', '.join(sorted(datasets.keys())))

    symbol1 = input("Type symbol of first choice: ")
    symbol2 = input("Type symbol of second choice: ")

    symbol1 = symbol1.strip().upper()
    symbol2 = symbol2.strip().upper()

    df1 = datasets.get(symbol1)
    df2 = datasets.get(symbol2)

    if df1 is None or df2 is None:
        print("One or both datasets not found.\n")
        recursive_menu()
        return

    s1 = df1.set_index('Date')['Close'].sort_index()
    s2 = df2.set_index('Date')['Close'].sort_index()

    s1, s2 = s1.align(s2, join='inner')

    s1 = s1.sort_index()
    s2 = s2.sort_index()

    # Compute percent changes
    r1 = s1.pct_change().dropna() * 100
    r2 = s2.pct_change().dropna() * 100

    dates = r1.index
    asset1_vals = r1.values
    asset2_vals = r2.values

    viz.plot_compare_asset_performance(dates, asset1_vals, asset2_vals, symbol1, symbol2)

    recursive_menu()

def volatility_comparison():
    print("\nOptions:")
    print(', '.join(sorted(datasets.keys())))

    symbol1 = input("Type symbol of first choice: ")
    symbol2 = input("Type symbol of second choice: ")

    symbol1 = symbol1.strip().upper()
    symbol2 = symbol2.strip().upper()

    df1 = datasets.get(symbol1)
    df2 = datasets.get(symbol2)

    if df1 is None or df2 is None:
        print("One or both datasets not found.\n")
        recursive_menu()
        return

    s1 = df1.set_index('Date')['Close'].sort_index()
    s2 = df2.set_index('Date')['Close'].sort_index()
    s1, s2 = s1.align(s2, join='inner')

    # Compute daily returns (decimal)
    r1 = s1.pct_change().dropna()
    r2 = s2.pct_change().dropna()

    # Rolling window (days) for volatility
    try:
        window_in = input("Enter rolling window in days [default 30] (Press Enter to skip): ")
        window = int(window_in) if window_in.strip() != '' else 30 # Weird way of doing this
    except Exception:
        window = 30

    # Annualize by sqrt(252) and convert to percent (252 Trading Days Annually)
    vol1 = r1.rolling(window=window).std() * (252 ** 0.5) * 100
    vol2 = r2.rolling(window=window).std() * (252 ** 0.5) * 100

    # Align vol series and drop initial NaNs from rolling
    vol1, vol2 = vol1.align(vol2, join='inner')
    vol1 = vol1.dropna()
    vol2 = vol2.dropna()

    dates = vol1.index

    viz.plot_compare_volatility(dates, vol1.values, vol2.values, symbol1, symbol2, window)

    recursive_menu()
            
def price_chart_comparison():
    print("\nOptions:")
    print(', '.join(sorted(datasets.keys())))

    symbol1 = input("Type symbol of first choice: ")
    symbol2 = input("Type symbol of second choice: ")

    symbol1 = symbol1.strip().upper()
    symbol2 = symbol2.strip().upper()

    df1 = datasets.get(symbol1)
    df2 = datasets.get(symbol2)

    if df1 is None or df2 is None:
        print("One or both datasets not found.\n")
        recursive_menu()
        return

    df1 = df1.set_index('Date')['Close'].sort_index()
    df2 = df2.set_index('Date')['Close'].sort_index()

    df1, df2 = df1.align(df2, join='inner')
 
    # Normalize both series to start at 1.0 (so comparisons are relative)
    df1_norm = df1 / df1.iloc[0]
    df2_norm = df2 / df2.iloc[0]

    # Plot natural-log of normalized prices
    # Useful for daily data but can cause problems when working on a smaller time frame
    log1 = np.log(df1_norm)
    log2 = np.log(df2_norm)

    dates = df1.index

    viz.plot_compare_log_price(dates, log1.values, log2.values, symbol1, symbol2)

    recursive_menu()

def volume_chart():
    print("\nOptions:")
    print(', '.join(sorted(datasets.keys())))

    symbol = input("Type symbol of desired cryptocurrency: ")

    symbol = symbol.strip().upper()

    df = datasets.get(symbol)
    if df is None:
        print(f"Dataset for '{symbol}' not found.\n")
        recursive_menu()
        return

    symbol = df['Symbol'].iloc[0]
    dates = df['Date']
    volume = df['Volume']

    viz.plot_volume_barchart(dates, symbol, volume)

    recursive_menu()

def main():
    # print(f"Loaded datasets: {', '.join(sorted(datasets.keys()))}")
    correlation_heatmap()

if __name__ == '__main__':
    # main()
    recursive_menu()