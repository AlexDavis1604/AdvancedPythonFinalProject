import matplotlib.pyplot as plt
import numpy as np

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
    
    def plot_volume_vs_price(self, dates, symbol, asset_prices, asset_volume):
        plt.figure(figsize=(12,6))

        ax1 = plt.gca()
        ax1.plot(dates, asset_prices, color='blue', label='Close Price')
        ax1.set_xlabel("Date")
        ax1.set_ylabel("Price (USD)", color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')

        # --- Secondary axis: Volume (bars) ---
        ax2 = ax1.twinx()
        ax2.bar(dates, asset_volume, color='gray', width=1.0, alpha=0.6, label='Volume')
        ax2.set_ylabel("Volume", color='gray')
        ax2.tick_params(axis='y', labelcolor='gray')

        # Title + grid
        plt.title(f"{symbol} — Price vs Volume Over Time")
        ax1.grid(True, linestyle='--', alpha=0.5)

        plt.tight_layout()
        plt.show()

    def plot_compare_volatility(self, dates, vol1, vol2, asset1_symbol, asset2_symbol, window=30):
        plt.figure(figsize=(12,6))

        plt.plot(dates, vol1, label=f"{asset1_symbol} ({window}-day)")
        plt.plot(dates, vol2, label=f"{asset2_symbol} ({window}-day)")

        plt.title(f"Rolling {window}-Day Annualized Volatility: {asset1_symbol} vs {asset2_symbol}")
        plt.xlabel("Date")
        plt.ylabel("Annualized Volatility (%)")
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.show()

    def plot_crypto_correlation_heatmap(self, price_matrix):
        symbols = price_matrix.columns.tolist()

        # Convert to numpy
        aligned = price_matrix.values

        # Compute correlation matrix
        corr_matrix = np.corrcoef(aligned.T).round(2)

        n = len(symbols)

        fig, ax = plt.subplots(figsize=(10, 8))

        # Create heatmap
        im = ax.imshow(corr_matrix, cmap="Spectral", vmin=-1, vmax=1)

        # Axis labels
        ax.set_xticks(np.arange(n))
        ax.set_yticks(np.arange(n))
        ax.set_xticklabels(symbols, rotation=45, ha="right", rotation_mode='anchor')
        ax.set_yticklabels(symbols)

        ax.set_ylim(n - 0.5, -0.5)

        # Annotate cells
        for i in range(n):
            for j in range(n):
                val = corr_matrix[i, j]
                ax.text(
                    j, i, f"{val:.2f}",
                    ha='center', va='center',
                    color='black' if abs(val) < 0.7 else 'white',
                    fontsize='8'
                )

        cbar = ax.figure.colorbar(im, ax=ax, format='%.2f')
        cbar.set_label("Correlation", rotation=270, labelpad=15)

        plt.title("Correlation of Cryptocurrency Daily Closing Prices", fontsize=14)
        plt.tight_layout()
        plt.show()

    def plot_weekday_normalized_volume(self, avg_df):

        days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        # Reindex to guarantee order
        avg_df = avg_df.reindex(days_order)

        fig, ax = plt.subplots(figsize=(12, 6))

        for col in avg_df.columns:
            ax.plot(days_order, avg_df[col].values, marker='o', label=col, linewidth=1)

        ax.set_title("Average Normalized Volume by Weekday")
        ax.set_xlabel("Day of Week")
        ax.set_ylabel("Average Normalized Volume")
        ax.set_xticks(days_order)
        ax.set_xticklabels(days_order, rotation=45)
        ax.grid(True, linestyle='--', alpha=0.4)
        ax.legend(loc='upper right', fontsize='small', ncol=2)

        plt.tight_layout()
        plt.show()