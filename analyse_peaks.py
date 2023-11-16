import csv
import matplotlib.pyplot as plt


# 2023.csv example
# symbol, inital_close, 7d_close, 7d_close_diff, 7d_high, initial_timestamp
# CDIO,0.68,1.06,1.5588235294117647,2.34,2023-11-06 05:00:00+00:00

class Stock:
    def __init__(self, symbol, initial_close, seven_day_close, seven_day_close_diff, seven_day_high, seven_day_high_diff, initial_timestamp):
        self.symbol = symbol
        self.initial_close = initial_close
        self.seven_day_close = seven_day_close
        self.seven_day_close_diff = seven_day_close_diff
        self.seven_day_high = seven_day_high
        self.seven_day_high_diff = seven_day_high_diff
        self.initial_timestamp = initial_timestamp

    def __str__(self):
        return f"Stock(symbol={self.symbol}, initial_close={self.initial_close}, seven_day_close={self.seven_day_close}, seven_day_close_diff={self.seven_day_close_diff}, seven_day_high={self.seven_day_high}, seven_day_high_diff={self.seven_day_high_diff}, initial_timestamp={self.initial_timestamp})"

    def __repr__(self):
        return self.__str__()


with open('2023.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    data = list(reader)

    # Map data to stocks
    stocks = []
    for row in data[1:]:
        stocks.append(Stock(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

    x = [float(stock.seven_day_close_diff) for stock in stocks]
    plt.hist(x, bins=50, range=(0, 3))
    plt.savefig("graphs/diff.png")
    plt.clf()

    # Plot frequency of 7d_high into high.png
    x = [float(stock.seven_day_high_diff) for stock in stocks]
    plt.hist(x, bins=50, range=(1, 5))
    plt.savefig("graphs/high.png")
    plt.clf()

    # Stocks where 7d_high_diff is greater than 2
    stoploss = 2
    stocks_stoplossed = [stock for stock in stocks if float(stock.seven_day_high_diff) > stoploss]
    stocks_not_stoplossed = [stock for stock in stocks if float(stock.seven_day_high_diff) <= stoploss]
    for stock in stocks_stoplossed:
        stock.seven_day_close_diff = stoploss

    # Combine stocks with stoploss and stocks without stoploss
    stocks = stocks_stoplossed + stocks_not_stoplossed

    # Plot frequency of stock 7d_close_diff into diff.png
    x = [float(stock.seven_day_close_diff) for stock in stocks]
    plt.hist(x, bins=20, range=(0, stoploss))
    plt.savefig("graphs/diff-stoplossed.png")
    plt.clf()

    # Plot frequency of 7d_high into high.png
    x = [float(stock.seven_day_high_diff) for stock in stocks]
    plt.hist(x, bins=50, range=(1, 5))
    plt.savefig("graphs/high-stoplossed.png")
    plt.clf()

    # Count number of stocks with negative 7d_close_diff
    count = 0
    for stock in stocks:
        if float(stock.seven_day_close_diff) < 1:
            count += 1

    print(f"Number of stocks with negative 7d_close_diff: {count}/{len(stocks)} ({count / len(stocks) * 100}%)")

    # Mean average 7d_close_diff
    total = 0
    for stock in stocks:
        total += float(stock.seven_day_close_diff)

    print(f"Mean average 7d_close_diff: {total / len(stocks)}")

    # Median average 7d_close_diff
    x.sort()

    if len(x) % 2 == 0:
        median = (x[len(x) // 2] + x[len(x) // 2 - 1]) / 2
    else:
        median = x[len(x) // 2]

    print(f"Median average 7d_close_diff: {median}")