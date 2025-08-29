import pytest
from overthinker.core.scenario_parser import ScenarioParser

@pytest.fixture
def parser():
    """Fixture providing a pre-configured ScenarioParser"""
    return ScenarioParser()

class TestBasicFunctionality:
    def test_parser_initialization(self, parser):
        """Verify the parser loads its NLP model"""
        assert hasattr(parser, 'nlp'), "NLP model not loaded"

    def test_parse_output_structure(self, parser):
        """Test the basic output structure"""
        result = parser.parse("John eats an apple")
        assert isinstance(result, dict)
        assert 'tokens' in result
        assert 'entities' in result
        assert 'actions' in result

class TestEntityRecognition:
    def test_parser_with_entities(self, parser):
        """Verify entity recognition works"""
        result = parser.parse("Apple is looking at buying U.K. startup for $1 billion")
        assert len(result['entities']) > 0, "No entities detected"
        
        # Check if any entity has text 'U.K.' and label 'GPE'
        uk_entity = next((entity for entity in result['entities'] 
                         if entity['text'] == 'U.K.' and entity['label'] == 'GPE'), None)
        assert uk_entity is not None, "GPE entity not found"
        
        # Check for MONEY entity
        money_entity = next((entity for entity in result['entities'] 
                            if entity['label'] == 'MONEY'), None)
        assert money_entity is not None, "Money entity missing"

class TestSentimentAnalysis:
    def test_positive_sentiment(self, parser):
        """Test positive sentiment detection"""
        result = parser.parse("This is absolutely wonderful!")
        assert result.get('sentiment', 0) > 0.7, "Positive sentiment not detected"

    def test_negative_sentiment(self, parser):
        """Test negative sentiment detection"""
        result = parser.parse("This is terrible and awful")
        assert result.get('sentiment', 1) < 0.3, "Negative sentiment not detected"