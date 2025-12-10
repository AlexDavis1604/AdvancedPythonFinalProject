import matplotlib.pyplot as plt

class CryptoVisualizer:

    def plot_price(self, dates, symbol, prices):
        plt.figure(figsize=(12, 6))

        plt.plot(dates, prices, label=f"{symbol} Closing Prices")

        plt.title(f"{symbol} Closing Prices")
        plt.xlabel("Date")
        plt.ylabel("Price (USD)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def plot_compare_asset_performance(self, dates, asset1_returns, asset2_returns, asset1_symbol, asset2_symbol):
        plt.figure(figsize=(12,6))

        plt.plot(dates, asset1_returns, label=asset1_symbol)
        plt.plot(dates, asset2_returns, label=asset2_symbol)

        plt.title(f"Daily Percent Change Comparison: {asset1_symbol} vs {asset2_symbol}")
        plt.xlabel("Date")
        plt.ylabel("Daily Percent Change")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def plot_compare_log_price(self, dates, asset1_prices, asset2_prices, asset1_symbol, asset2_symbol):
        plt.figure(figsize=(12,6))

        plt.plot(dates, asset1_prices, label=f"{asset1_symbol} Price (log)")
        plt.plot(dates, asset2_prices, label=f"{asset2_symbol} Price (log)")

        plt.title(f"Log Price Comparison: {asset1_symbol} vs {asset2_symbol}")
        plt.xlabel("Date")
        plt.ylabel("Log Price (in USD)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def plot_volume_barchart(self, dates, symbol, asset_volume):
        plt.figure(figsize=(12,6))

        plt.bar(dates, asset_volume, width=1) # Width=1 for daily bars

        plt.title(f"{symbol} Volume")
        plt.xlabel("Date")
        plt.ylabel("Volume")
        plt.legend()
        plt.tight_layout()
        plt.show()