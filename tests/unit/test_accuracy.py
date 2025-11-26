"""
Accuracy Testing Suite for Overthinker AI
Tests intent classification and overall decision quality
"""
import pytest
from overthinker.core.decision_analyzer import DecisionAnalyzer
from overthinker.core.intent_classifier import IntentClassifier, ContextExtractor


class TestIntentClassification:
    """Test intent classification accuracy"""
    
    @pytest.fixture
    def analyzer(self):
        return DecisionAnalyzer()
    
    @pytest.fixture
    def intent_classifier(self):
        return IntentClassifier()
    
    @pytest.fixture
    def comprehensive_dataset(self):
        """Comprehensive test dataset with expected intents"""
        return [
            # Transportation (15 cases)
            ("Should I take the bus or Uber to work?", "transportation"),
            ("What's the fastest way to reach the airport?", "transportation"),
            ("I need to commute daily, bike or metro?", "transportation"),
            ("How do I get to Connaught Place from Noida?", "transportation"),
            ("Should I drive or take public transport today?", "transportation"),
            ("Best way to travel to Bangalore from Delhi?", "transportation"),
            ("Metro vs auto rickshaw for office?", "transportation"),
            ("Should I walk to the market or take a cab?", "transportation"),
            ("Going to Mumbai next week, train or flight?", "transportation"),
            ("How to reach the hospital quickly?", "transportation"),
            ("Should I bike to gym or drive?", "transportation"),
            ("Ola vs Uber for airport drop?", "transportation"),
            ("Is metro better than bus for daily commute?", "transportation"),
            ("Should I buy a car or keep using cabs?", "transportation"),
            ("Walking vs cycling for nearby places?", "transportation"),
            
            # Purchase (15 cases)
            ("Should I buy iPhone 15 or wait for 16?", "purchase"),
            ("Is it worth repairing my old laptop?", "purchase"),
            ("Need a new phone under 30000 rupees", "purchase"),
            ("Buy new shoes or repair old ones?", "purchase"),
            ("Should I get a PS5 or Xbox?", "purchase"),
            ("Worth buying noise canceling headphones?", "purchase"),
            ("New laptop or upgrade current one?", "purchase"),
            ("Should I purchase this expensive watch?", "purchase"),
            ("Buy smart TV now or wait for sale?", "purchase"),
            ("Invest in good mattress or save money?", "purchase"),
            ("Should I get AirPods or cheaper alternative?", "purchase"),
            ("Buy camera or use phone camera?", "purchase"),
            ("Worth getting premium gym membership?", "purchase"),
            ("Should I upgrade my bike or buy new?", "purchase"),
            ("Buy ergonomic chair for WFH?", "purchase"),
            
            # Food (10 cases)
            ("Should I cook dinner or order from Swiggy?", "food"),
            ("Eating out vs meal prep for the week?", "food"),
            ("Order food or cook at home tonight?", "food"),
            ("Restaurant dinner or home cooked meal?", "food"),
            ("Should I get Zomato delivery or cook?", "food"),
            ("Meal prep Sunday or order daily?", "food"),
            ("Cook breakfast or buy from cafe?", "food"),
            ("Eat out with friends or host at home?", "food"),
            ("Order pizza or make pasta at home?", "food"),
            ("Food delivery or cook simple meal?", "food"),
            
            # Career (12 cases)
            ("Got a job offer with 30% hike, should I switch?", "career"),
            ("Should I accept this remote position?", "career"),
            ("Leave current job for startup opportunity?", "career"),
            ("Switch to new company or stay for promotion?", "career"),
            ("Accept job offer with lower salary but better role?", "career"),
            ("Should I resign without another offer?", "career"),
            ("Join new company or wait for better offer?", "career"),
            ("Take promotion or switch company?", "career"),
            ("Accept transfer to different city?", "career"),
            ("Should I ask for raise or look elsewhere?", "career"),
            ("Stay in stable job or take risky opportunity?", "career"),
            ("Change career field or stick to current?", "career"),
            
            # Health (10 cases)
            ("Should I join gym or workout at home?", "health"),
            ("See a doctor for this headache?", "health"),
            ("Start exercising now or wait?", "health"),
            ("Go to gym or morning walk?", "health"),
            ("Should I consult doctor for back pain?", "health"),
            ("Join yoga class or do at home?", "health"),
            ("See specialist or general physician?", "health"),
            ("Start diet plan or exercise first?", "health"),
            ("Get health checkup or wait?", "health"),
            ("Home workout or gym membership?", "health"),
            
            # Relationship (8 cases)
            ("Should I ask her out?", "relationship"),
            ("Talk to friend about problem or let it go?", "relationship"),
            ("Break up or give another chance?", "relationship"),
            ("Should I propose or wait?", "relationship"),
            ("Tell parents about relationship?", "relationship"),
            ("Continue long distance or break up?", "relationship"),
            ("Should I apologize first?", "relationship"),
            ("Meet ex for closure or move on?", "relationship"),
            
            # General (10 cases)
            ("Should I watch a movie tonight?", "general"),
            ("Need advice on weekend plans", "general"),
            ("Should I learn guitar or piano?", "general"),
            ("Vacation in mountains or beach?", "general"),
            ("Should I adopt a pet?", "general"),
            ("Read book or watch series tonight?", "general"),
            ("Should I start a blog?", "general"),
            ("Learn coding or design?", "general"),
            ("Should I move to a new apartment?", "general"),
            ("Join evening class or online course?", "general"),
        ]
    
    def test_intent_classification_accuracy(self, analyzer, intent_classifier, 
                                           comprehensive_dataset):
        """Test overall intent classification accuracy"""
        correct = 0
        total = len(comprehensive_dataset)
        misclassifications = []
        
        for question, expected_intent in comprehensive_dataset:
            parsed = analyzer.parser.parse(question)
            detected_intent, confidence = intent_classifier.classify_intent(
                question, parsed
            )
            
            if detected_intent == expected_intent:
                correct += 1
            else:
                misclassifications.append({
                    'question': question,
                    'expected': expected_intent,
                    'detected': detected_intent,
                    'confidence': confidence
                })
        
        accuracy = (correct / total) * 100
        
        print(f"\n{'='*60}")
        print(f"INTENT CLASSIFICATION TEST RESULTS")
        print(f"{'='*60}")
        print(f"Total test cases: {total}")
        print(f"Correct classifications: {correct}")
        print(f"Accuracy: {accuracy:.2f}%")
        print(f"{'='*60}")
        
        if misclassifications:
            print(f"\nMisclassifications ({len(misclassifications)}):")
            for miss in misclassifications[:10]:  # Show first 10
                print(f"\n  Question: {miss['question']}")
                print(f"  Expected: {miss['expected']}")
                print(f"  Detected: {miss['detected']} (confidence: {miss['confidence']:.2f})")
        
        # Assert accuracy is at least 85%
        assert accuracy >= 85, f"Accuracy {accuracy:.2f}% is below 85% threshold"
    
    def test_context_extraction(self, analyzer):
        """Test constraint extraction accuracy"""
        extractor = ContextExtractor()
        
        test_cases = [
            ("Need urgent transport to hospital", 
             {'time_sensitive': True, 'urgency_level': 'high'}),
            
            ("Looking for cheap phone under 10k", 
             {'budget_conscious': True}),
            
            ("Want the best quality laptop", 
             {'quality_focused': True}),
            
            ("Need convenient option for daily commute",
             {'convenience_focused': True}),
            
            ("Should I buy this expensive watch worth 50000 rupees?",
             {'budget_amount': '50000 rupees'}),
        ]
        
        passed = 0
        for question, expected_constraints in test_cases:
            parsed = analyzer.parser.parse(question)
            constraints = extractor.extract_constraints(parsed, question)
            
            all_match = True
            for key, value in expected_constraints.items():
                if constraints.get(key) != value:
                    print(f"\nFailed: {question}")
                    print(f"  Expected {key}={value}")
                    print(f"  Got {key}={constraints.get(key)}")
                    all_match = False
            
            if all_match:
                passed += 1
        
        accuracy = (passed / len(test_cases)) * 100
        print(f"\nContext Extraction Accuracy: {accuracy:.0f}%")
        
        assert accuracy >= 80, "Context extraction accuracy too low"
    
    def test_confidence_scores(self, intent_classifier):
        """Test that confidence scores are reasonable"""
        test_cases = [
            ("Should I take bus or uber?", 0.5),  # Clear transportation
            ("What should I do today?", 0.3),     # Vague, low confidence
            ("Buy iPhone or Samsung?", 0.5),      # Clear purchase
        ]
        
        for question, min_confidence in test_cases:
            from overthinker.core.scenario_parser import ScenarioParser
            parser = ScenarioParser()
            parsed = parser.parse(question)
            intent, confidence = intent_classifier.classify_intent(question, parsed)
            
            print(f"\nQuestion: {question}")
            print(f"Intent: {intent}, Confidence: {confidence:.2f}")
            
            assert confidence >= min_confidence, \
                f"Confidence too low for: {question}"


class TestDecisionQuality:
    """Test the quality of decision analysis output"""
    
    @pytest.fixture
    def analyzer(self):
        return DecisionAnalyzer()
    
    def test_transportation_analysis_completeness(self, analyzer):
        """Test transportation analysis provides comprehensive info"""
        question = "Should I take metro or cab to office?"
        result = analyzer.analyze_decision(question)
        
        # Check for key elements
        assert "TRANSPORTATION" in result
        assert len(result) > 200, "Analysis too short"
        assert "💰" in result or "⏰" in result or "⚖️" in result
    
    def test_purchase_analysis_completeness(self, analyzer):
        """Test purchase analysis provides financial wisdom"""
        question = "Should I buy new iPhone?"
        result = analyzer.analyze_decision(question)
        
        assert "PURCHASE" in result
        assert len(result) > 200
        # Should contain financial considerations
        assert any(word in result.lower() for word in 
                  ['budget', 'cost', 'financial', 'money', 'price'])
    
    def test_consistency(self, analyzer):
        """Test that same question gives consistent answer"""
        question = "Should I take bus to work?"
        
        result1 = analyzer.analyze_decision(question)
        result2 = analyzer.analyze_decision(question)
        
        # Results should be identical (no randomness)
        assert result1 == result2, "Analysis not consistent"


def test_overall_system():
    """Integration test of the entire system"""
    analyzer = DecisionAnalyzer()
    
    test_questions = [
        "Should I buy new laptop or repair old one?",
        "Metro or Uber for airport?",
        "Cook at home or order food?",
        "Accept job offer with 40% hike?",
        "Join gym or workout at home?"
    ]
    
    print(f"\n{'='*60}")
    print("INTEGRATION TEST - Sample Analyses")
    print(f"{'='*60}")
    
    for question in test_questions:
        result = analyzer.analyze_decision(question)
        parsed = analyzer.parser.parse(question)
        intent, confidence = analyzer.intent_classifier.classify_intent(
            question, parsed
        )
        
        print(f"\nQ: {question}")
        print(f"Intent: {intent} (confidence: {confidence:.2f})")
        print(f"Analysis length: {len(result)} chars")
        
        assert len(result) > 100, "Analysis too short"
        assert confidence > 0, "Zero confidence"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
