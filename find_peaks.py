import jsonpickle
import csv

with open("2023.json", "r", encoding='utf-8') as f:
    bars = jsonpickle.decode(f.read())

with open("2023.csv", "w", newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["symbol", "inital_close", "7d_close", "7d_close_diff", "7d_high", "7d_high_diff", "initial_timestamp"])

    for symbol, bars in bars.items():
        # Add diff field (close / open)
        # iterate over bars with value and index
        for i, bar in enumerate(bars):
            diff = bar.close / bar.open

            if diff < 1.5:
                continue

            if len(bars) <= i + 7:
                continue

            # Get future bar
            future_bar = bars[i + 7]

            # Get high of next 7 days
            high = max([bar.high for bar in bars[i:i+7]])

            writer.writerow([symbol, bar.close, future_bar.close, future_bar.close / bar.close, high, high / bar.close, bar.timestamp])
