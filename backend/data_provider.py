

import random
import time
from datetime import datetime, timedelta

def get_historical_data(candles=200):
    """Generates a list of historical OHLCV candles."""
    now = datetime.now()
    data = []
    price = 100
    for i in range(candles):
        dt = now - timedelta(minutes=(candles - i))
        open_price = price + random.uniform(-1, 1)
        high_price = open_price + random.uniform(0, 2)
        low_price = open_price - random.uniform(0, 2)
        close_price = random.uniform(low_price, high_price)
        volume = random.uniform(1000, 5000)
        
        data.append({
            "time": dt.strftime('%Y-%m-%d %H:%M:%S'),
            "open": round(open_price, 2),
            "high": round(high_price, 2),
            "low": round(low_price, 2),
            "close": round(close_price, 2),
            "volume": round(volume, 2)
        })
        price = close_price
        
    return data

def generate_new_candle(last_candle):
    """Generates a new candle based on the last one."""
    last_close = last_candle["close"]
    
    open_price = last_close + random.uniform(-1, 1)
    high_price = max(open_price, last_close) + random.uniform(0, 2)
    low_price = min(open_price, last_close) - random.uniform(0, 2)
    close_price = random.uniform(low_price, high_price)
    volume = random.uniform(1000, 5000)
    
    # The time for the new candle should be the next interval
    last_time = datetime.strptime(last_candle["time"], '%Y-%m-%d %H:%M:%S')
    new_time = last_time + timedelta(minutes=1)

    return {
        "time": new_time.strftime('%Y-%m-%d %H:%M:%S'),
        "open": round(open_price, 2),
        "high": round(high_price, 2),
        "low": round(low_price, 2),
        "close": round(close_price, 2),
        "volume": round(volume, 2)
    }

if __name__ == '__main__':
    # For testing purposes
    historical_data = get_historical_data()
    print(f"Generated {len(historical_data)} historical candles.")
    print("Last 2 historical candles:")
    print(historical_data[-2:])
    
    print("\n--- Generating new candle ---")
    new_candle = generate_new_candle(historical_data[-1])
    print("New candle:")
    print(new_candle)

