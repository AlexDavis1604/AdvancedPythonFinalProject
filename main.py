from data_loader import CryptoDataLoader
from data_processing import DataProcessor
from visualizer import CryptoVisualizer
import numpy as np
import pandas as pd

# Data Source:
# https://www.kaggle.com/datasets/sudalairajkumar/cryptocurrencypricehistory?resource=download

viz = CryptoVisualizer()
data = CryptoDataLoader()

datasets = data.load_all_datasets()
analyzer = DataProcessor(datasets)

def recursive_menu():
    while True:
        print('Select Option:' \
        '\n0) Quit' \
        '\n1) View Price Chart' \
        '\n2) View Volume Chart' \
        '\n3) Compare Cryptocurreny Price Chart (Log Scale)' \
        '\n4) Compare Cryptocurreny Performance' \
        '\n5) Compare Price vs Volume of Cryptocurrency' \
        '\n6) Compare Cryptocurrency Volatility' \
        '\n7) View Cryptocurrency Correlation Heatmap' \
        '\n8) Average Normalized Volume by Weekday' )
        choice = input('Type Selection: ')
        
        if choice == '0':
            return
        
        elif choice == '1':
            price_chart()
        
        elif choice == '2':
            volume_chart()

        elif choice == '3':
            price_chart_comparison()

        elif choice == '4':
            price_performance_comparison()

        elif choice == '5':
            price_volume_comparison()

        elif choice == '6':
            volatility_comparison()
        
        elif choice == '7':
            correlation_heatmap()
        
        elif choice == '8':
            weekday_normalized_volume()

def correlation_heatmap():
    price_matrix = analyzer.align_datasets(join='inner')
    try:
        viz.plot_crypto_correlation_heatmap(price_matrix)
    except Exception as e:
        print(f"Error plotting correlation heatmap: {e}")

    recursive_menu()

def price_volume_comparison():
    print('\nOptions:')
    print(', '.join(sorted(datasets.keys())))

    symbol = input('Type symbol of desired cryptocurrency: ')

    symbol = symbol.strip().upper()

    df = datasets.get(symbol)
    if df is None:
        print(f'Dataset for {symbol} not found.\n ')
        recursive_menu()
        return

    symbol_name = df['Symbol'].iloc[0]

    prices_series = analyzer.prepare_series(symbol)
    dates = prices_series.index
    prices = prices_series.values
    volume = df['Volume'].values

    try:
        viz.plot_volume_vs_price(dates, symbol_name, prices, volume)
    except Exception as e:
        print(f"Error plotting volume vs price: {e}")

    recursive_menu()

def price_chart():
    print('\nOptions:')
    print(', '.join(sorted(datasets.keys())))

    symbol = input('Type symbol of desired cryptocurrency: ')

    symbol = symbol.strip().upper()

    df = datasets.get(symbol)
    if df is None:
        print(f'Dataset for {symbol} not found.\n')
        recursive_menu()
        return

    symbol_name = df['Symbol'].iloc[0]
    prices_series = analyzer.prepare_series(symbol)
    dates = prices_series.index
    prices = prices_series.values

    try:
        viz.plot_price(dates, symbol_name, prices)
    except Exception as e:
        print(f"Error plotting price chart: {e}")

    recursive_menu()

def price_performance_comparison():
    print('\nOptions:')
    print(', '.join(sorted(datasets.keys())))

    symbol1 = input('Type symbol of first choice: ')
    symbol2 = input('Type symbol of second choice: ')

    symbol1 = symbol1.strip().upper()
    symbol2 = symbol2.strip().upper()

    df1 = datasets.get(symbol1)
    df2 = datasets.get(symbol2)

    if df1 is None or df2 is None:
        print('One or both datasets not found.\n')
        recursive_menu()
        return

    # Use analyzer to prepare return series (percent)
    r1 = analyzer.prepare_series(symbol1, returns=True, percent=True)
    r2 = analyzer.prepare_series(symbol2, returns=True, percent=True)

    r1, r2 = r1.align(r2, join='inner')

    dates = r1.index
    asset1_vals = r1.values
    asset2_vals = r2.values

    try:
        viz.plot_compare_asset_performance(dates, asset1_vals, asset2_vals, symbol1, symbol2)
    except Exception as e:
        print(f"Error plotting asset performance comparison: {e}")

    recursive_menu()

def volatility_comparison():
    print('\nOptions:')
    print(', '.join(sorted(datasets.keys())))

    symbol1 = input('Type symbol of first choice: ')
    symbol2 = input('Type symbol of second choice: ')

    symbol1 = symbol1.strip().upper()
    symbol2 = symbol2.strip().upper()

    df1 = datasets.get(symbol1)
    df2 = datasets.get(symbol2)

    if df1 is None or df2 is None:
        print('One or both datasets not found.\n')
        recursive_menu()
        return

    # Use analyzer to get decimal returns (not percent)
    r1 = analyzer.prepare_series(symbol1, returns=True, percent=False)
    r2 = analyzer.prepare_series(symbol2, returns=True, percent=False)

    # Rolling window (days) for volatility
    try:
        window_in = input('Enter rolling window in days [default 30] (Press Enter to skip): ')
        window = int(window_in) if window_in.strip() != '' else 30 # Weird way of doing this
    except Exception:
        window = 30

    # Annualize by sqrt(252) and convert to percent (252 Trading Days Annually)
    vol1 = r1.rolling(window=window).std() * (252 ** 0.5) * 100
    vol2 = r2.rolling(window=window).std() * (252 ** 0.5) * 100

    # Align vol series and drop initial NaNs from rolling
    vol1, vol2 = vol1.align(vol2, join='inner')

    dates = vol1.index

    try:
        viz.plot_compare_volatility(dates, vol1.values, vol2.values, symbol1, symbol2, window)
    except Exception as e:
        print(f"Error plotting volatility comparison: {e}")

    recursive_menu()

def weekday_normalized_volume():

    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    series_dict = {}

    for symbol, df in datasets.items():
        df_local = df.copy()
        # Filter out non-positive
        vol = df_local[pd.to_numeric(df_local['Volume'], errors='coerce') > 0]
        
        rolling_med = vol['Volume'].rolling(30).median()

        # Avoid division by zero or inf by converting zero medians to NaN
        rolling_med = rolling_med.replace(0, np.nan)
        vol_norm = np.log(vol['Volume'] / rolling_med)

        # Only keep rows where vol_norm is finite
        valid = vol_norm.replace([np.inf, -np.inf], np.nan).dropna()

        day_names = pd.to_datetime(df_local.loc[valid.index, 'Date']).dt.day_name()

        df_tmp = pd.DataFrame({'day': day_names, 'norm': vol_norm.loc[valid.index]})
        weekday_avg = df_tmp.groupby('day')['norm'].mean()

        weekday_avg = weekday_avg.reindex(days_order)

        series_dict[symbol] = weekday_avg

    if not series_dict:
        print('No valid volume data available to plot.')
        recursive_menu()

    avg_df = pd.DataFrame(series_dict)

    try:
        viz.plot_weekday_normalized_volume(avg_df)
    except Exception as e:
        print(f"Error plotting weekday normalized volume: {e}")

    recursive_menu()
            
def price_chart_comparison():
    print('\nOptions:')
    print(', '.join(sorted(datasets.keys())))

    symbol1 = input('Type symbol of first choice: ')
    symbol2 = input('Type symbol of second choice: ')

    symbol1 = symbol1.strip().upper()
    symbol2 = symbol2.strip().upper()

    df1 = datasets.get(symbol1)
    df2 = datasets.get(symbol2)

    if df1 is None or df2 is None:
        print('One or both datasets not found.\n')
        recursive_menu()

    s1 = analyzer.prepare_series(symbol1)
    s2 = analyzer.prepare_series(symbol2)

    s1, s2 = s1.align(s2, join='inner')

    # Normalize both series to start at 1.0 (so comparisons are relative)
    s1_norm = s1 / s1.iloc[0]
    s2_norm = s2 / s2.iloc[0]


    # Useful for daily data but can cause problems when working on a smaller time frame
    log1 = np.log(s1_norm)
    log2 = np.log(s2_norm)

    dates = s1.index

    try:
        viz.plot_compare_log_price(dates, log1.values, log2.values, symbol1, symbol2)
    except Exception as e:
        print(f"Error plotting log price comparison: {e}")

    recursive_menu()

def volume_chart():
    print('\nOptions:')
    print(', '.join(sorted(datasets.keys())))

    symbol = input('Type symbol of desired cryptocurrency: ')

    symbol = symbol.strip().upper()

    df = datasets.get(symbol)
    if df is None:
        print(f'Dataset for {symbol} not found.\n')
        recursive_menu()
        return

    symbol = df['Symbol'].iloc[0]
    dates = df['Date']
    volume = df['Volume']

    try:
        viz.plot_volume_barchart(dates, symbol, volume)
    except Exception as e:
        print(f"Error plotting volume chart: {e}")

    recursive_menu()

def main():
    # print(f'Loaded datasets: {', '.join(sorted(datasets.keys()))}')
    correlation_heatmap()

if __name__ == '__main__':
    # main()
    recursive_menu()