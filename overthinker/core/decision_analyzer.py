"""
Decision Analyzer Module for Overthinker AI
Provides thoughtful, context-aware analysis for daily life decisions
"""
from .scenario_parser import ScenarioParser
from .intent_classifier import IntentClassifier, ContextExtractor
import random


class DecisionAnalyzer:
    def __init__(self):
        self.parser = ScenarioParser()
        self.intent_classifier = IntentClassifier()
        self.context_extractor = ContextExtractor()
        
        # Transportation options database
        self.transport_options = {
            'car': {'cost': 'medium', 'comfort': 'high', 'time': 'variable', 
                   'convenience': 'high', 'icon': '🚗'},
            'public_transport': {'cost': 'low', 'comfort': 'medium', 'time': 'fixed', 
                                'convenience': 'medium', 'icon': '🚌'},
            'bike': {'cost': 'very low', 'comfort': 'low', 'time': 'medium', 
                    'convenience': 'high', 'icon': '🚴'},
            'walking': {'cost': 'none', 'comfort': 'low', 'time': 'high', 
                       'convenience': 'medium', 'icon': '🚶'},
            'rideshare': {'cost': 'high', 'comfort': 'high', 'time': 'variable', 
                         'convenience': 'high', 'icon': '🚕'}
        }
        
        # Purchase considerations
        self.purchase_considerations = [
            "Evaluate your actual need versus want for this item",
            "Consider the long-term value and durability",
            "Research alternative options and compare prices",
            "Think about the opportunity cost (what else you could do with the money)",
            "Check reviews and product reliability from multiple sources",
            "Consider the environmental impact of your purchase",
            "Look for warranty and after-sales support",
            "Calculate cost per use if it's a durable item"
        ]
    
    def analyze_decision(self, question: str) -> str:
        """
        Main method to analyze a decision question
        Uses intent classification and context extraction for better accuracy
        """
        # Parse the question
        parsed = self.parser.parse(question)
        
        # Classify intent with confidence
        intent, confidence = self.intent_classifier.classify_intent(question, parsed)
        
        # Extract context and constraints
        constraints = self.context_extractor.extract_constraints(parsed, question)
        
        # Low confidence fallback to general analysis
        if confidence < 0.35:
            return self.general_analysis(question, parsed, constraints)
        
        # Route to specific analyzer based on intent
        if intent == 'transportation':
            return self.analyze_transportation(question, parsed, constraints)
        elif intent == 'purchase':
            return self.analyze_purchase(question, parsed, constraints)
        elif intent == 'food':
            return self.analyze_food(question, parsed, constraints)
        elif intent == 'career':
            return self.analyze_career(question, parsed, constraints)
        elif intent == 'health':
            return self.analyze_health(question, parsed, constraints)
        elif intent == 'relationship':
            return self.analyze_relationship(question, parsed, constraints)
        else:
            return self.general_analysis(question, parsed, constraints)
    
    def analyze_transportation(self, question: str, parsed: dict, 
                               constraints: dict) -> str:
        """Analyze transportation decisions with context awareness"""
        entities = [ent['text'] for ent in parsed['entities']]
        sentiment = parsed.get('sentiment', 0)
        
        analysis = [
            "🚗 TRANSPORTATION DECISION ANALYSIS",
            "=" * 50,
            f"📍 Destination: {', '.join(entities) if entities else 'Not specified'}",
            ""
        ]
        
        # Context-based recommendations
        primary_concern = constraints.get('primary_concern')
        
        if constraints['time_sensitive']:
            analysis.extend([
                "⏰ TIME-PRIORITY RECOMMENDATIONS:",
                "",
                "1. 🚕 Rideshare (Uber/Ola)",
                "   ✓ Fastest door-to-door option",
                "   ✓ No parking hassles",
                "   ✗ Higher cost (₹₹₹)",
                "",
                "2. 🚗 Personal Car",
                "   ✓ Direct route control",
                "   ✓ Leave immediately",
                "   ✗ Traffic & parking variables",
                "",
                "3. 🏍️ Bike Taxi (Rapido)",
                "   ✓ Excellent for traffic",
                "   ✓ Cost-effective",
                "   ✗ Weather dependent"
            ])
        
        elif constraints['budget_conscious']:
            analysis.extend([
                "💰 BUDGET-PRIORITY RECOMMENDATIONS:",
                "",
                "1. 🚌 Public Transport (Bus/Metro)",
                "   ✓ Most economical (₹10-50)",
                "   ✓ Predictable cost",
                "   ✗ Fixed routes & timing",
                "",
                "2. 🚴 Bike/Bicycle",
                "   ✓ Zero ongoing cost",
                "   ✓ Health benefits",
                "   ✗ Physical effort required",
                "",
                "3. 🚶 Walking (if < 2km)",
                "   ✓ Completely free",
                "   ✓ Exercise included",
                "   ✗ Time consuming"
            ])
        
        elif constraints['quality_focused'] or constraints['convenience_focused']:
            analysis.extend([
                "⭐ COMFORT-PRIORITY RECOMMENDATIONS:",
                "",
                "1. 🚕 Premium Rideshare",
                "   ✓ Maximum comfort",
                "   ✓ Professional drivers",
                "   ✓ AC & music",
                "",
                "2. 🚗 Personal Car",
                "   ✓ Privacy & control",
                "   ✓ Your own space",
                "   ✗ Driving stress in traffic"
            ])
        
        else:
            # Balanced recommendation
            analysis.extend([
                "⚖️ BALANCED RECOMMENDATIONS:",
                "",
                "Consider these key factors:",
                "",
                "🕐 TIME: How urgent is your trip?",
                "   • Urgent → Rideshare/Car",
                "   • Flexible → Public transport",
                "",
                "💵 COST: What's your budget?",
                "   • Tight budget → Bus/Metro/Bike",
                "   • Moderate → Shared rides",
                "   • Flexible → Private cab/Car",
                "",
                "🌤️ WEATHER: Check current conditions",
                "   • Rain/Heat → Covered transport",
                "   • Pleasant → Walk/Bike option",
                "",
                "📏 DISTANCE:",
                "   • < 2km → Walk/Bike",
                "   • 2-10km → Public transport/Bike",
                "   • > 10km → Car/Rideshare"
            ])
        
        # Sentiment-based advice
        if sentiment < -0.3:
            analysis.extend([
                "",
                "💡 STRESS DETECTED: You seem stressed. Consider:",
                "   • Taking a comfortable, relaxing option",
                "   • Avoiding driving in traffic yourself",
                "   • Maybe a rideshare where you can relax"
            ])
        elif sentiment > 0.3:
            analysis.extend([
                "",
                "😊 POSITIVE MOOD: Great energy! Consider:",
                "   • An active option like biking/walking",
                "   • Enjoying the journey, not just destination"
            ])
        
        return "\n".join(analysis)
    
    def analyze_purchase(self, question: str, parsed: dict, 
                        constraints: dict) -> str:
        """Analyze purchase decisions with financial wisdom"""
        entities = [ent['text'] for ent in parsed['entities']]
        budget = constraints.get('budget_amount')
        
        analysis = [
            "🛒 PURCHASE DECISION ANALYSIS",
            "=" * 50,
            f"🎯 Item: {', '.join(entities) if entities else 'Considering purchase'}",
        ]
        
        if budget:
            analysis.append(f"💰 Budget: {budget}")
        
        analysis.append("")
        
        # Context-based advice
        if constraints['budget_conscious']:
            analysis.extend([
                "💡 BUDGET-CONSCIOUS APPROACH:",
                "",
                "1. ⏸️ PAUSE & REFLECT:",
                "   • Sleep on it for 24-48 hours",
                "   • Is this a need or a want?",
                "   • Can you afford this without stress?",
                "",
                "2. 🔍 FIND ALTERNATIVES:",
                "   • Check refurbished/open-box options",
                "   • Look for sales and discounts",
                "   • Consider previous generation models",
                "   • Compare prices across platforms",
                "",
                "3. 💸 FINANCIAL CHECK:",
                "   • Will this impact your emergency fund?",
                "   • Any upcoming essential expenses?",
                "   • Can you pay in full or need EMI?"
            ])
        
        elif constraints['quality_focused']:
            analysis.extend([
                "⭐ QUALITY-FOCUSED APPROACH:",
                "",
                "1. 🔍 DEEP RESEARCH:",
                "   • Read professional reviews (not just ads)",
                "   • Check long-term reliability reports",
                "   • Look for warranty & service quality",
                "   • Join user forums/communities",
                "",
                "2. 💎 VALUE ASSESSMENT:",
                "   • Quality often costs more upfront",
                "   • Calculate cost per year of use",
                "   • Good products have better resale value",
                "   • Consider brand reputation",
                "",
                "3. 🎯 MAKE THE INVESTMENT:",
                "   • If quality is proven, don't compromise",
                "   • Buy once, use for years approach",
                "   • Avoid cheap alternatives that break"
            ])
        
        else:
            # Balanced purchase analysis
            analysis.extend([
                "🤔 KEY CONSIDERATIONS:",
                ""
            ])
            
            # Add 4-5 relevant considerations (not random anymore)
            key_considerations = [
                self.purchase_considerations[0],  # Need vs want
                self.purchase_considerations[1],  # Long-term value
                self.purchase_considerations[2],  # Compare prices
                self.purchase_considerations[4],  # Reviews
                self.purchase_considerations[7],  # Cost per use
            ]
            
            for i, consideration in enumerate(key_considerations, 1):
                analysis.append(f"{i}. {consideration}")
            
            analysis.extend([
                "",
                "📊 FINANCIAL PERSPECTIVE:",
                "",
                "• Budget Impact: Does this fit your monthly budget?",
                "• Opportunity Cost: What else could this money do?",
                "• ROI Timeline: How long will you use this?",
                "• Depreciation: Will it hold value?",
                "",
                "💭 THE 30-DAY RULE:",
                "For expensive items (>₹10,000):",
                "→ Wait 30 days while researching",
                "→ If you still want it after a month, likely worth it",
                "→ Often you'll find you don't need it",
                "",
                "✅ DECISION FRAMEWORK:",
                "• Immediate need + good reviews + fits budget = BUY",
                "• Can wait + expensive + uncertain need = WAIT",
                "• Want not need + tight budget = SKIP"
            ])
        
        return "\n".join(analysis)
    
    def analyze_food(self, question: str, parsed: dict, 
                    constraints: dict) -> str:
        """Analyze food and dining decisions"""
        analysis = [
            "🍽️ FOOD DECISION ANALYSIS",
            "=" * 50,
            ""
        ]
        
        if constraints['budget_conscious']:
            analysis.extend([
                "💰 BUDGET-FRIENDLY RECOMMENDATION:",
                "",
                "🏠 COOK AT HOME:",
                "✓ Much cheaper (3-5x cost savings)",
                "✓ Healthier ingredients control",
                "✓ Larger portions, leftovers possible",
                "✗ Time & effort required",
                "✗ Cleanup needed",
                "",
                "💡 TIP: Batch cook for the week to save time!"
            ])
        
        elif constraints['time_sensitive']:
            analysis.extend([
                "⏰ TIME-SAVING RECOMMENDATION:",
                "",
                "📱 ORDER FOOD:",
                "✓ Delivered in 30-45 mins",
                "✓ No cooking or cleanup",
                "✓ Wide variety options",
                "✗ Higher cost (₹₹₹)",
                "✗ Less healthy usually",
                "",
                "💡 TIP: Keep healthy quick snacks for busy days!"
            ])
        
        else:
            analysis.extend([
                "⚖️ BALANCED ANALYSIS:",
                "",
                "🏠 COOKING AT HOME:",
                "PROS:",
                "• Cost: ₹50-100 per meal",
                "• Health: You control ingredients",
                "• Skill: Improve cooking abilities",
                "• Satisfaction: Accomplished feeling",
                "",
                "CONS:",
                "• Time: 30-60 mins total",
                "• Energy: After work fatigue",
                "• Cleanup: Dishes to wash",
                "",
                "📱 ORDERING FOOD:",
                "PROS:",
                "• Convenience: Zero effort",
                "• Variety: Try new cuisines",
                "• Time: Use for other activities",
                "",
                "CONS:",
                "• Cost: ₹200-500 per meal",
                "• Health: Usually more oily/salty",
                "• Habit: Can become expensive routine",
                "",
                "🎯 RECOMMENDATION:",
                "• Cook 5 days, order 2 days (80-20 rule)",
                "• Keep quick recipes handy (15-min meals)",
                "• Order when genuinely tired/busy",
                "• Meal prep on weekends helps"
            ])
        
        return "\n".join(analysis)
    
    def analyze_career(self, question: str, parsed: dict, 
                      constraints: dict) -> str:
        """Analyze career and job decisions"""
        entities = [ent['text'] for ent in parsed['entities']]
        
        analysis = [
            "💼 CAREER DECISION ANALYSIS",
            "=" * 50,
            ""
        ]
        
        # Check for money entities (salary information)
        money_entities = [e['text'] for e in parsed['entities'] 
                         if e['label'] == 'MONEY']
        
        if money_entities:
            analysis.append(f"💰 Salary Consideration: {', '.join(money_entities)}")
            analysis.append("")
        
        analysis.extend([
            "🎯 KEY CAREER FACTORS TO EVALUATE:",
            "",
            "1. 💵 FINANCIAL GROWTH:",
            "   • Salary increase percentage",
            "   • Long-term earning potential",
            "   • Benefits & perks package",
            "   • Bonus & ESOP opportunities",
            "",
            "2. 📈 CAREER PROGRESSION:",
            "   • Learning opportunities",
            "   • Skill development scope",
            "   • Promotion timeline",
            "   • Industry reputation",
            "",
            "3. ⚖️ WORK-LIFE BALANCE:",
            "   • Working hours & flexibility",
            "   • Remote work options",
            "   • Leave policies",
            "   • Commute time",
            "",
            "4. 🏢 COMPANY FACTORS:",
            "   • Company stability & growth",
            "   • Work culture fit",
            "   • Team & manager quality",
            "   • Job security",
            "",
            "5. 🎓 PERSONAL GROWTH:",
            "   • Matches your career goals?",
            "   • Exit opportunities later",
            "   • Industry relevance",
            "   • Network expansion",
            "",
            "⚠️ RED FLAGS TO WATCH:",
            "• Very high attrition rate",
            "• Unclear job responsibilities",
            "• Extremely long working hours",
            "• Negative online reviews",
            "• Pressure during interview",
            "",
            "✅ GREEN FLAGS:",
            "• Clear growth path",
            "• Positive employee testimonials",
            "• Structured onboarding",
            "• Transparent communication",
            "• Good work-life balance reputation",
            "",
            "🤔 DECISION FRAMEWORK:",
            "• If 30%+ salary hike → Strong consider",
            "• If better learning → Worth it even for lateral move",
            "• If toxic current workplace → Leave ASAP",
            "• If happy currently → Needs 40%+ hike to switch"
        ])
        
        return "\n".join(analysis)
    
    def analyze_health(self, question: str, parsed: dict, 
                      constraints: dict) -> str:
        """Analyze health and fitness decisions"""
        analysis = [
            "🏥 HEALTH DECISION ANALYSIS",
            "=" * 50,
            "",
            "⚠️ IMPORTANT DISCLAIMER:",
            "This is general guidance only. For serious health concerns,",
            "always consult a qualified medical professional.",
            "",
            "=" * 50,
            ""
        ]
        
        # Check if it's about seeing a doctor
        if any(word in question.lower() for word in ['doctor', 'hospital', 'sick', 'pain', 'hurt']):
            analysis.extend([
                "🏥 MEDICAL CONSULTATION GUIDANCE:",
                "",
                "SEE A DOCTOR IMMEDIATELY IF:",
                "⚠️ Severe/persistent pain",
                "⚠️ High fever (>103°F / 39.4°C)",
                "⚠️ Difficulty breathing",
                "⚠️ Sudden vision/speech changes",
                "⚠️ Severe injury",
                "⚠️ Symptoms worsen rapidly",
                "",
                "CAN MONITOR AT HOME:",
                "✓ Minor cold/cough (< 3 days)",
                "✓ Mild headache",
                "✓ Small cuts/bruises",
                "✓ Mild stomach upset",
                "",
                "💡 WHEN IN DOUBT, CONSULT!",
                "Better safe than sorry with health."
            ])
        
        # Check if it's about exercise/gym
        elif any(word in question.lower() for word in ['gym', 'exercise', 'workout', 'fitness']):
            analysis.extend([
                "💪 FITNESS DECISION GUIDANCE:",
                "",
                "🏋️ JOIN GYM IF:",
                "✓ Need equipment/weights",
                "✓ Want structured environment",
                "✓ Enjoy group motivation",
                "✓ Can commit to membership cost",
                "",
                "🏃 HOME WORKOUT IF:",
                "✓ Prefer convenience/privacy",
                "✓ Have time constraints",
                "✓ Want to save money",
                "✓ Bodyweight exercises sufficient",
                "",
                "🎯 GETTING STARTED:",
                "• Start small (3 days/week)",
                "• Focus on consistency > intensity",
                "• Warm up & cool down always",
                "• Rest days are important",
                "• Track progress to stay motivated",
                "",
                "💡 FREE RESOURCES:",
                "• YouTube fitness channels",
                "• Mobile workout apps",
                "• Walking/running (zero cost)",
                "• Home bodyweight routines"
            ])
        
        else:
            # General health advice
            analysis.extend([
                "🌟 GENERAL HEALTH PRIORITIES:",
                "",
                "1. 😴 SLEEP (7-9 hours):",
                "   • Foundation of all health",
                "   • Consistent sleep schedule",
                "   • No screens 1 hour before bed",
                "",
                "2. 🥗 NUTRITION:",
                "   • Balanced meals",
                "   • More vegetables & fruits",
                "   • Stay hydrated (2-3L water)",
                "   • Limit processed foods",
                "",
                "3. 🏃 MOVEMENT:",
                "   • 30 mins daily activity",
                "   • Walking is excellent start",
                "   • Reduce sitting time",
                "   • Take stairs when possible",
                "",
                "4. 🧘 MENTAL HEALTH:",
                "   • Stress management",
                "   • Social connections",
                "   • Hobbies & relaxation",
                "   • Seek help when needed",
                "",
                "💡 REMEMBER:",
                "Small consistent changes > Big temporary efforts"
            ])
        
        return "\n".join(analysis)
    
    def analyze_relationship(self, question: str, parsed: dict, 
                            constraints: dict) -> str:
        """Analyze relationship decisions"""
        analysis = [
            "💝 RELATIONSHIP DECISION ANALYSIS",
            "=" * 50,
            "",
            "🤔 IMPORTANT NOTE:",
            "Relationships are deeply personal. This is general guidance",
            "to help you think through your situation.",
            "",
            "=" * 50,
            ""
        ]
        
        analysis.extend([
            "💭 KEY QUESTIONS TO ASK YOURSELF:",
            "",
            "1. 🎯 CLARITY:",
            "   • What do I truly want?",
            "   • Am I ready for this commitment?",
            "   • Are my expectations realistic?",
            "",
            "2. 💬 COMMUNICATION:",
            "   • Can we talk openly and honestly?",
            "   • Do we listen to each other?",
            "   • Can we handle disagreements maturely?",
            "",
            "3. 🤝 COMPATIBILITY:",
            "   • Shared values and life goals?",
            "   • Respect each other's differences?",
            "   • Enjoy spending time together?",
            "",
            "4. 🚩 RED FLAGS:",
            "   • Controlling behavior",
            "   • Lack of trust or respect",
            "   • Constant negativity",
            "   • Makes you feel bad about yourself",
            "",
            "5. ✅ GREEN FLAGS:",
            "   • Mutual respect and support",
            "   • Healthy communication",
            "   • Brings out your best self",
            "   • Shared laughter and joy",
            "",
            "💡 GENERAL WISDOM:",
            "",
            "• Take your time - don't rush major decisions",
            "• Trust your instincts - they usually know",
            "• Talk to trusted friends/family",
            "• Prioritize your wellbeing and happiness",
            "• It's okay to walk away from what's not working",
            "",
            "🎯 REMEMBER:",
            "A healthy relationship should add to your life,",
            "not complicate it or drain your energy."
        ])
        
        return "\n".join(analysis)
    
    def general_analysis(self, question: str, parsed: dict, 
                        constraints: dict) -> str:
        """Provide general analysis for other types of questions"""
        analysis = [
            "🤔 DECISION ANALYSIS",
            "=" * 50,
            "",
            "Let me help you think through this decision from multiple angles:",
            ""
        ]
        
        # Always use the same perspectives (not random) for consistency
        perspectives = [
            ("🎯 Practical Perspective", 
             "What's the most efficient and feasible solution?"),
            
            ("💰 Financial Perspective", 
             "What makes the most economic sense long-term?"),
            
            ("😊 Emotional Perspective", 
             "What would make you happiest and most fulfilled?"),
            
            ("🔮 Long-term Perspective", 
             "How will this decision affect your future (1-5 years)?"),
            
            ("👥 Social Perspective", 
             "How does this impact others around you?"),
        ]
        
        for title, description in perspectives:
            analysis.append(f"{title}:")
            analysis.append(f"  {description}")
            analysis.append("")
        
        # Add constraint-based guidance
        if constraints['time_sensitive']:
            analysis.extend([
                "⏰ URGENCY FACTOR:",
                "Since this seems time-sensitive, prioritize:",
                "• What can be decided/acted on quickly?",
                "• What are the immediate consequences of waiting?",
                "• Can some aspects be decided now, others later?",
                ""
            ])
        
        if constraints['budget_conscious']:
            analysis.extend([
                "💰 BUDGET FACTOR:",
                "Since cost is a concern, consider:",
                "• What are the actual costs (not just initial price)?",
                "• Any hidden or ongoing expenses?",
                "• Can you achieve 80% of the goal for 50% of cost?",
                ""
            ])
        
        # Decision framework
        analysis.extend([
            "📋 DECISION FRAMEWORK:",
            "",
            "1. CLARIFY: What exactly am I deciding?",
            "2. OPTIONS: What are all possible choices?",
            "3. CRITERIA: What matters most to me here?",
            "4. EVALUATE: How does each option score on my criteria?",
            "5. DECIDE: Choose and commit with confidence",
            "6. ACT: Take the first step immediately",
            "",
            "💡 HELPFUL TECHNIQUES:",
            "",
            "• Pros & Cons List: Classic but effective",
            "• 10-10-10 Rule: How will I feel in 10 mins, 10 months, 10 years?",
            "• Regret Minimization: What will I regret NOT doing?",
            "• Flip a Coin: Your reaction to the result reveals your true preference",
            "",
            "🎯 FINAL ADVICE:",
            "Trust yourself. You know your situation better than anyone.",
            "Make the best decision you can with current information,",
            "then commit to making that decision work."
        ])
        
        return "\n".join(analysis)
