"""
Decision Analyzer Module for Overthinker AI
Provides thoughtful analysis for daily life decisions
"""
from .scenario_parser import ScenarioParser
import random

class DecisionAnalyzer:
    def __init__(self):
        self.parser = ScenarioParser()
        self.transport_options = {
            'car': {'cost': 'medium', 'comfort': 'high', 'time': 'variable', 'convenience': 'high'},
            'public_transport': {'cost': 'low', 'comfort': 'medium', 'time': 'fixed', 'convenience': 'medium'},
            'bike': {'cost': 'very low', 'comfort': 'low', 'time': 'medium', 'convenience': 'high'},
            'walking': {'cost': 'none', 'comfort': 'low', 'time': 'high', 'convenience': 'medium'},
            'rideshare': {'cost': 'high', 'comfort': 'high', 'time': 'variable', 'convenience': 'high'}
        }
        
        self.purchase_considerations = [
            "Evaluate your actual need versus want for this item",
            "Consider the long-term value and durability",
            "Research alternative options and compare prices",
            "Think about the opportunity cost (what else you could do with the money)",
            "Check reviews and product reliability",
            "Consider the environmental impact of your purchase"
        ]
    
    def analyze_decision(self, question):
        """Main method to analyze a decision question"""
        parsed = self.parser.parse(question)
        
        # Check what type of decision this is
        if any(word in question.lower() for word in ['go', 'travel', 'commute', 'get to']):
            return self.analyze_transportation(question)
        elif any(word in question.lower() for word in ['buy', 'purchase', 'acquire', 'get']):
            return self.analyze_purchase(question)
        else:
            return self.general_analysis(question)
    
    def analyze_transportation(self, question):
        """Analyze transportation decisions"""
        parsed = self.parser.parse(question)
        entities = [ent['text'] for ent in parsed['entities']]
        
        # Generate thoughtful analysis
        analysis = [
            "Based on your question, here's a balanced perspective:",
            f"I've detected references to: {', '.join(entities) if entities else 'your destination'}"
        ]
        
        # Add specific considerations
        analysis.append("When considering how to get somewhere, think about:")
        analysis.append("1. Time efficiency vs. cost savings")
        analysis.append("2. Environmental impact of your choice")
        analysis.append("3. Health benefits of more active options")
        
        # Suggest options based on context
        if any(word in question.lower() for word in ['fast', 'quick', 'urgent']):
            analysis.append("Since time seems important, consider rideshare or car for direct routing.")
        elif any(word in question.lower() for word in ['cheap', 'save', 'budget']):
            analysis.append("For cost-effective options, public transport or biking might be best.")
        else:
            analysis.append("For a balanced approach, consider which factor matters most: time, cost, or comfort.")
        
        return "\n".join(analysis)
    
    def analyze_purchase(self, question):
        """Analyze purchase decisions"""
        parsed = self.parser.parse(question)
        entities = [ent['text'] for ent in parsed['entities']]
        
        analysis = [
            "Purchase decisions require careful consideration:",
            f"You mentioned: {', '.join(entities) if entities else 'this item'}"
        ]
        
        # Add thoughtful considerations
        analysis.append("Here are some points to ponder:")
        for i, consideration in enumerate(random.sample(self.purchase_considerations, 3), 1):
            analysis.append(f"{i}. {consideration}")
        
        # Financial advice
        analysis.append("From a financial perspective:")
        analysis.append("- Consider if this purchase aligns with your budget and financial goals")
        analysis.append("- Think about the cost per use if it's a durable item")
        analysis.append("- Remember that sometimes spending more for quality saves money long-term")
        
        return "\n".join(analysis)
    
    def general_analysis(self, question):
        """Provide general analysis for other types of questions"""
        parsed = self.parser.parse(question)
        
        analysis = [
            "Let me help you think through this:",
            "Here are different perspectives to consider:"
        ]
        
        # Add different perspectives
        perspectives = [
            "Practical perspective: What's the most efficient solution?",
            "Financial perspective: What makes the most economic sense?",
            "Emotional perspective: What would make you happiest?",
            "Long-term perspective: How will this decision affect your future?",
            "Social perspective: How does this impact others around you?"
        ]
        
        for perspective in random.sample(perspectives, 3):
            analysis.append(f"- {perspective}")
        
        analysis.append("")
        analysis.append("My suggestion: Weigh these perspectives based on your current priorities.")
        
        return "\n".join(analysis)