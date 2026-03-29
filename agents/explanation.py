from utils import Recommendation, translate_to_hindi
from langchain_groq import ChatGroq
import config

class ExplanationAgent:
    def __init__(self, groq_api_key: str):
        self.llm = ChatGroq(groq_api_key=groq_api_key, model="llama-3.3-70b-versatile")

    def generate_explanation(self, rec: Recommendation, lang: str = "en") -> str:
        prompt = f"""Generate simple human-readable explanation for Indian investor:
Stock: {rec.stock}
Action: {rec.action}
Confidence: {rec.confidence}%
Risk: {rec.risk_level}

Return bullet point reasoning chain."""
        explanation = self.llm.invoke(prompt).content
        if lang == "hi":
            explanation += "\n\nहिंदी अनुवाद:\n" + translate_to_hindi(self.llm, explanation)
        return explanation

