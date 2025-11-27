import spacy
from spacy.tokens import Doc
from typing import Dict, List, Tuple, Optional  # Added Optional for type hints
from textblob import TextBlob

class ScenarioParser:
    def __init__(self):
        """Initialize with English language model"""
        self.nlp = spacy.load("en_core_web_sm")
        
        # === ENHANCEMENT 1: Cache for repeated texts ===
        self._cache = {}  # Dictionary to store parsed results for faster repeated access
        
    def analyze_sentiment(self, text: str) -> float:
        """
        Enhanced sentiment analysis using TextBlob
        Returns: float from -1 (negative) to 1 (positive)
        """
        analysis = TextBlob(text)
        return analysis.sentiment.polarity
        
    def parse(self, text: str) -> Dict[str, any]:
        """Main parsing method that returns structured analysis"""
        
        # === ENHANCEMENT 2: Check cache first ===
        if text in self._cache:
            return self._cache[text]  # Return cached result if available
        
        doc = self.nlp(text)  # Process text with spaCy
        
        # === ENHANCEMENT 3: Detailed entity processing ===
        entities = []
        for ent in doc.ents:
            entities.append({
                'text': ent.text,         # The actual entity text
                'label': ent.label_,      # Entity type (PERSON, ORG, etc.)
                'start': ent.start_char,  # Character start position
                'end': ent.end_char       # Character end position
            })
            
        # === ENHANCEMENT 4: Risk assessment integration ===
        risk_score = self._assess_risk(text, doc)  # Calculate risk score
        
        # Build complete analysis result
        result = {
            'raw_text': text,
            'tokens': [token.text for token in doc],
            'entities': entities,  # Using enhanced entity format
            'actions': [token.lemma_ for token in doc if token.pos_ == "VERB"],
            'nouns': [token.text for token in doc if token.pos_ == "NOUN"],
            'sentiment': self.analyze_sentiment(text),
            'risk_score': risk_score  # New risk assessment field
        }
        
        # Cache the result before returning
        self._cache[text] = result
        return result
    
    def _assess_risk(self, text: str, doc: Optional[Doc] = None) -> float:
        """
        Assesses potential risk level (0-1)
        Args:
            text: Input text to analyze
            doc: Optional pre-processed spaCy Doc object
        Returns:
            float: Risk score between 0 (safe) and 1 (dangerous)
        """
        if doc is None:
            doc = self.nlp(text)  # Process text if Doc not provided
            
        # Dictionary of risk indicators and their weights
        risk_indicators = {
            'danger': 0.8,
            'risk': 0.7,
            'harm': 0.6, 
            'poison': 0.9,
            'toxic': 0.85,
            'kill': 0.95,
            'death': 0.9
        }
        
        # Calculate maximum risk score found in text
        max_risk = 0.0
        for token in doc:
            lemma = token.lemma_.lower()
            if lemma in risk_indicators:
                max_risk = max(max_risk, risk_indicators[lemma])
        
        # Adjust risk based on number of entities and cap at 1.0
        return min(max_risk * (1 + 0.1 * len(doc.ents)), 1.0)