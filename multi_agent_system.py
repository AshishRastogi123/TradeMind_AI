import asyncio
import json
from typing import List
from dotenv import load_dotenv
import os

from agents.opportunity_radar import OpportunityRadarAgent
from agents.technical_analysis import TechnicalAnalysisAgent
from agents.sentiment import SentimentAgent
from agents.risk import RiskAgent
from agents.decision import DecisionAgent
from agents.explanation import ExplanationAgent
from utils import StockSignal, Recommendation

load_dotenv()

class MultiAgentSystem:
    def __init__(self, groq_api_key: str):
        self.groq_key = groq_api_key
        self.opportunity = OpportunityRadarAgent()
        self.tech = TechnicalAnalysisAgent()
        self.sentiment = SentimentAgent(groq_api_key)
        self.risk = RiskAgent()
        self.decision = DecisionAgent()
        self.explanation = ExplanationAgent(groq_api_key)

    async def analyze(self) -> List[Recommendation]:
        recs = []
        symbols = self.opportunity.scan_opportunities()

        for symbol in symbols:
            opp_score = self.opportunity.score_opportunity(symbol)
            tech_data = self.tech.analyze(symbol)
            tech_score = tech_data["tech_score"]
            sent_score = await asyncio.to_thread(self.sentiment.analyze_sentiment, symbol)
            risk_data = self.risk.assess_risk(symbol)
            risk_score = risk_data["risk_score"]

            signal = StockSignal(symbol, opp_score, tech_score, sent_score, risk_score)
            rec = self.decision.make_decision(signal)
            
            # Generate dynamic, stock-specific explanation
            explanation = self.explanation.generate_explanation(rec)
            rec.reason = [line.strip('• ') for line in explanation.split('\n') if line.strip()]
            recs.append(rec)
        return recs

    def format_recs_json(self, recs: List[Recommendation]) -> str:
        return json.dumps([rec.__dict__ for rec in recs], indent=2, default=str)
