NSE_SYMBOLS = [
    'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'HINDUNILVR.NS',
    'ICICIBANK.NS', 'KOTAKBANK.NS', 'BHARTIARTL.NS', 'ITC.NS', 'SBIN.NS'
]

AGENT_WEIGHTS = {
    "opportunity": 0.25,
    "technical": 0.30,
    "sentiment": 0.25,
    "risk": 0.20
}

CONFIDENCE_BUY = 60
CONFIDENCE_SELL = 40

HINDI_PROMPT = """
Translate this English financial analysis to simple Hindi for Indian investors.
Keep technical terms in English, explain simply.
Text: {text}
"""

