"""
Intent Classifier Module
Classifies user questions into decision categories with confidence scores
"""
from typing import Dict, Tuple, List


class IntentClassifier:
    """Classifies decision intents using multi-factor scoring"""
    
    def __init__(self):
        # Enhanced keyword patterns with multiple signals
        self.intent_patterns = {
            'transportation': {
                'verbs': ['go', 'travel', 'commute', 'drive', 'ride', 'walk', 'bike', 
                         'fly', 'reach', 'arrive', 'move', 'head', 'navigate', 'drop'],
                'nouns': ['bus', 'car', 'train', 'taxi', 'uber', 'ola', 'bike', 'plane', 
                         'metro', 'auto', 'transport', 'rickshaw', 'scooter', 'cab',
                         'airport', 'station', 'office', 'work', 'rapido', 'vehicle',
                         'cabs', 'commute'],
                'phrases': ['get to', 'how to reach', 'way to', 'going to', 'travel to',
                           'commute to', 'best route', 'fastest way', 'or uber', 'vs uber',
                           'or ola', 'vs ola', 'or cab', 'vs cab', 'vs metro', 'or metro',
                           'vs bus', 'or bus', 'take the', 'airport drop'],
                'locations': ['GPE', 'LOC', 'FAC']  # spaCy entity types for places
            },
            'purchase': {
                'verbs': ['buy', 'purchase', 'get', 'acquire', 'order', 'shop', 'invest',
                         'upgrade', 'replace', 'spend', 'repair'],
                'nouns': ['phone', 'laptop', 'product', 'item', 'gadget', 'device', 
                         'clothes', 'watch', 'tv', 'camera', 'headphones', 'shoes',
                         'iphone', 'samsung', 'macbook', 'airpods'],
                'phrases': ['should i buy', 'worth buying', 'repair or replace', 
                           'new vs old', 'buy or wait', 'worth getting', 'or repair',
                           'new phone', 'new laptop', 'buy new'],
                'modifiers': ['new', 'old', 'expensive', 'cheap', 'affordable']
            },
            'food': {
                'verbs': ['eat', 'cook', 'order', 'dine', 'prepare', 'make', 'bake'],
                'nouns': ['food', 'restaurant', 'meal', 'dinner', 'lunch', 'breakfast', 
                         'snack', 'swiggy', 'zomato', 'kitchen', 'recipe', 'delivery'],
                'phrases': ['cook or order', 'eat out', 'home cooked', 'order food',
                           'dine out', 'food delivery', 'make food', 'cook at home',
                           'or order', 'or cook', 'swiggy delivery', 'zomato delivery']
            },
            'career': {
                'verbs': ['work', 'join', 'switch', 'apply', 'resign', 'accept', 
                         'quit', 'leave', 'change', 'ask'],
                'nouns': ['job', 'career', 'company', 'offer', 'salary', 'position', 
                         'role', 'promotion', 'boss', 'workplace', 'office', 'raise',
                         'hike'],
                'phrases': ['job offer', 'change job', 'new job', 'career move',
                           'switch companies', 'leave job', 'job switch', 'ask for raise',
                           'look elsewhere', 'remote position']
            },
            'health': {
                'verbs': ['exercise', 'sleep', 'rest', 'workout', 'diet', 'run', 'jog',
                         'see', 'join'],
                'nouns': ['health', 'gym', 'doctor', 'medicine', 'fitness', 'sleep',
                         'hospital', 'clinic', 'workout', 'yoga', 'specialist', 
                         'physician', 'checkup'],
                'phrases': ['see a doctor', 'go to gym', 'health concern', 'feel sick',
                           'start exercising', 'workout routine', 'join gym', 'at home',
                           'or gym', 'yoga class', 'health checkup', 'see specialist']
            },
            'relationship': {
                'verbs': ['date', 'marry', 'propose', 'breakup', 'meet', 'talk',
                         'ask', 'apologize'],
                'nouns': ['relationship', 'girlfriend', 'boyfriend', 'partner', 'friend',
                         'family', 'marriage', 'date', 'her', 'him'],
                'phrases': ['ask out', 'break up', 'get married', 'in love', 'ask her',
                           'ask him', 'apologize first', 'should i ask']
            }
        }
    
    def classify_intent(self, text: str, parsed_data: Dict) -> Tuple[str, float]:
        """
        Classify intent with confidence score using multiple signals
        
        Args:
            text: Original question text
            parsed_data: Output from ScenarioParser.parse()
        
        Returns:
            Tuple of (intent_name, confidence_score)
        """
        text_lower = text.lower()
        scores = {}
        
        # Pre-process tokens once (they are already strings from scenario_parser)
        tokens_lower = [token.lower() for token in parsed_data.get('tokens', [])]
        
        for intent, patterns in self.intent_patterns.items():
            score = 0
            
            # Signal 1: Check verbs from parsed actions (weight: 4)
            for action in parsed_data.get('actions', []):
                if action.lower() in patterns['verbs']:
                    score += 4
            
            # Signal 2: Check nouns from parsed data (weight: 3)
            for noun in parsed_data.get('nouns', []):
                if noun.lower() in patterns['nouns']:
                    score += 3
            
            # Signal 3: Check key phrases (weight: 6 - highest)
            # Check longer phrases first for better matching
            sorted_phrases = sorted(patterns['phrases'], key=len, reverse=True)
            for phrase in sorted_phrases:
                if phrase in text_lower:
                    score += 6
                    break  # Only count the best phrase match
            
            # Signal 4: Check entities for context (weight: 3)
            for entity in parsed_data.get('entities', []):
                entity_text = entity['text'].lower()
                entity_label = entity['label']
                
                # Match entity text
                if entity_text in patterns['nouns']:
                    score += 3
                
                # Match entity types (like GPE for transportation)
                if 'locations' in patterns and entity_label in patterns['locations']:
                    score += 3
            
            # Signal 5: Check modifiers if present (weight: 2)
            if 'modifiers' in patterns:
                for modifier in patterns['modifiers']:
                    if modifier in text_lower:
                        score += 2
            
            # Bonus: Check for brand names and specific keywords in raw text
            for noun in patterns['nouns']:
                if noun in text_lower and noun not in tokens_lower:
                    score += 2  # Catch things spaCy might have missed
            
            scores[intent] = score
        
        # Find best match
        if not scores or max(scores.values()) == 0:
            return 'general', 0.3
        
        best_intent = max(scores, key=scores.get)
        max_score = scores[best_intent]
        
        # Get second best score for confidence calculation
        sorted_scores = sorted(scores.values(), reverse=True)
        second_score = sorted_scores[1] if len(sorted_scores) > 1 else 0
        
        # Calculate confidence based on score difference
        # More separation = higher confidence
        if second_score == 0:
            confidence = min(max_score / 12.0, 1.0)
        else:
            # Confidence increases with score gap
            score_gap = max_score - second_score
            confidence = min((max_score / 12.0) + (score_gap / 20.0), 1.0)
        
        # Boost confidence if score is very high
        if max_score >= 15:
            confidence = min(confidence * 1.2, 1.0)
        
        return best_intent, confidence


class ContextExtractor:
    """Extracts decision constraints and context from text"""
    
    def __init__(self):
        self.constraint_keywords = {
            'time_sensitive': ['urgent', 'quick', 'fast', 'asap', 'immediately', 
                              'hurry', 'rush', 'quickly', 'soon', 'right now'],
            'budget_conscious': ['cheap', 'affordable', 'budget', 'save money', 
                                'economical', 'inexpensive', 'low cost', 'under'],
            'quality_focused': ['best', 'quality', 'premium', 'reliable', 'durable',
                               'long-term', 'high quality', 'top rated', 'excellent'],
            'convenience': ['easy', 'convenient', 'simple', 'hassle free', 
                           'comfortable', 'effortless']
        }
    
    def extract_constraints(self, parsed_data: Dict, text: str) -> Dict:
        """
        Extract decision constraints and preferences from text
        
        Returns dict with constraint flags and extracted values
        """
        constraints = {
            'time_sensitive': False,
            'budget_conscious': False,
            'quality_focused': False,
            'convenience_focused': False,
            'urgency_level': 'normal',
            'budget_amount': None,
            'primary_concern': None
        }
        
        text_lower = text.lower()
        concern_scores = {}
        
        # Check each constraint type
        for constraint_type, keywords in self.constraint_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                concern_scores[constraint_type] = score
                
                # Set boolean flags
                if constraint_type == 'time_sensitive':
                    constraints['time_sensitive'] = True
                    constraints['urgency_level'] = 'high'
                elif constraint_type == 'budget_conscious':
                    constraints['budget_conscious'] = True
                elif constraint_type == 'quality_focused':
                    constraints['quality_focused'] = True
                elif constraint_type == 'convenience':
                    constraints['convenience_focused'] = True
        
        # Determine primary concern (highest scoring)
        if concern_scores:
            constraints['primary_concern'] = max(concern_scores, key=concern_scores.get)
        
        # Extract monetary values from entities
        money_entities = [e for e in parsed_data.get('entities', []) 
                         if e['label'] == 'MONEY']
        if money_entities:
            constraints['budget_amount'] = money_entities[0]['text']
        
        # Extract time entities
        time_entities = [e for e in parsed_data.get('entities', [])
                        if e['label'] in ['TIME', 'DATE']]
        if time_entities:
            constraints['time_constraint'] = time_entities[0]['text']
        
        return constraints
