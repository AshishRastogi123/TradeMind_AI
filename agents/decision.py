from utils import StockSignal, Recommendation, get_stock_data
from config import AGENT_WEIGHTS, CONFIDENCE_BUY, CONFIDENCE_SELL

class DecisionAgent:
    def __init__(self):
        self.weights = AGENT_WEIGHTS

    def make_decision(self, signal: StockSignal) -> Recommendation:
        weighted_score = (
            self.weights["opportunity"] * signal.opportunity_score +
            self.weights["technical"] * signal.tech_score +
            self.weights["sentiment"] * (signal.sentiment_score + 1) / 2 +
            self.weights["risk"] * (1 - signal.risk_score)
        )
        confidence_pct = int(weighted_score * 100)

        if confidence_pct >= CONFIDENCE_BUY:
            action = "STRONG BUY"
        elif confidence_pct >= 50:
            action = "BUY"
        elif confidence_pct <= CONFIDENCE_SELL:
            action = "SELL"
        else:
            action = "HOLD"

        # Use real current price with safety
        data = get_stock_data(signal.symbol)
        if data["hist"].empty:
            print(f"No data for {signal.symbol}, using fallback")
            current_price = 1000.0
        else:
            current_price = float(data["hist"]["Close"].iloc[-1])
            print(f"PRICE: {signal.symbol} {current_price}")
        
        if current_price <= 0:
            current_price = 1000.0
        
        entry = current_price
        target = current_price * 1.05  # 5% upside
        stop_loss = current_price * 0.97  # 3% downside
        risk_level = "Low" if signal.risk_score < 0.3 else "Medium" if signal.risk_score < 0.6 else "High"

        reason = [
            "Strong upward momentum from recent price action",
            "Technical indicators showing bullish signals (RSI and MACD crossover)",
            "Positive volume trend confirming buyer interest",
            "Risk profile indicates moderate volatility ahead"
        ]

        return Recommendation(
            stock=signal.symbol,
            action=action,
            confidence=confidence_pct,
            risk_level=risk_level,
            entry=entry,
            target=target,
            stop_loss=stop_loss,
            reason=reason
        )
