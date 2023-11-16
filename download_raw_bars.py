import os
from datetime import datetime

import jsonpickle
from alpaca.data import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.trading import TradingClient
from alpaca.trading.requests import GetAssetsRequest

stock_client = StockHistoricalDataClient(os.environ["APCA-API-KEY-ID"], os.environ["APCA-API-SECRET-KEY"])
trading_client = TradingClient(os.environ["APCA-API-KEY-ID"], os.environ["APCA-API-SECRET-KEY"])

# Get all symbols
assets = trading_client.get_all_assets(filter=GetAssetsRequest(is_active=True, asset_class="us_equity"))
assets = [asset for asset in assets if asset.tradable]

print(f"Found {len(assets)} assets")

# Chunk assets into groups of CHUNK_SIZE
CHUNK_SIZE = 5_000
asset_chunks = [assets[x:x+CHUNK_SIZE] for x in range(0, len(assets), CHUNK_SIZE)]
bar_chunks = []

for i, asset_chunk in enumerate(asset_chunks):
    # Get bar for every symbol today during market hours
    request_params = StockBarsRequest(
        symbol_or_symbols=[asset.symbol for asset in asset_chunk],
        timeframe=TimeFrame.Day,
        start=datetime(2023, 1, 1),
        end=datetime.date(datetime.now()),
    )

    bars = stock_client.get_stock_bars(request_params)
    bar_chunks.append(bars)

    print(f"Finished fetching chunk {i + 1} of {len(asset_chunks)}")

# Flatten map bar_chunks into a single map of bars
bars = {}
for bar_chunk in bar_chunks:
    for symbol, bar_list in bar_chunk.data.items():
        if symbol not in bars:
            bars[symbol] = []

        bars[symbol].extend(bar_list)

print(f"Fetched bars: {len(bars)}")

# Dump raw bars to 2023.json
with open("2023.json", "w", encoding='utf-8') as f:
    f.write(jsonpickle.encode(bars))
