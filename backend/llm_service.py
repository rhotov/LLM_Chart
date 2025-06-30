
import random
import json

def get_llm_analysis(kline_data):
    """
    Simulates a call to an LLM API for market analysis.
    
    Args:
        kline_data (list): A list of recent k-line data points (dictionaries).
        
    Returns:
        dict: A JSON-like dictionary with the analysis result.
    """
    if not kline_data:
        return {"error": "No data provided"}

    # Simulate some basic analysis
    last_close = kline_data[-1]['close']
    prev_close = kline_data[-2]['close'] if len(kline_data) > 1 else last_close

    # Randomly decide on a signal
    signal_type = random.choice(["bullish", "bearish", "neutral"])
    confidence = round(random.uniform(0.6, 0.95), 2)
    
    if signal_type == "bullish":
        message = f"Price shows bullish momentum. Potential breakout above {last_close + 5}."
        target_price = last_close * (1 + random.uniform(0.01, 0.03))
    elif signal_type == "bearish":
        message = f"Price shows bearish signs. Potential drop below {last_close - 5}."
        target_price = last_close * (1 - random.uniform(0.01, 0.03))
    else:
        message = "Market seems to be consolidating. No clear signal."
        target_price = last_close

    analysis = {
        "signal": signal_type,
        "target_price": round(target_price, 2),
        "confidence": confidence,
        "message": message,
        "timestamp": kline_data[-1]['time'] # Tie analysis to the last candle time
    }
    
    return analysis

if __name__ == '__main__':
    # For testing purposes
    mock_data = [
        {'time': '2025-06-30 10:00:00', 'open': 100, 'high': 102, 'low': 99, 'close': 101, 'volume': 1500},
        {'time': '2025-06-30 10:01:00', 'open': 101, 'high': 103, 'low': 100, 'close': 102, 'volume': 1800}
    ]
    
    llm_result = get_llm_analysis(mock_data)
    print("Simulated LLM Analysis:")
    print(json.dumps(llm_result, indent=2))
