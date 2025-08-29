#!/usr/bin/env python3
"""
Overthinker AI Demo
A simple command-line interface to demonstrate the decision analysis capabilities
"""
import sys
import os

# Add the current directory to the path so we can import overthinker
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from overthinker.core.decision_analyzer import DecisionAnalyzer

def main():
    analyzer = DecisionAnalyzer()
    
    print("=" * 60)
    print("OVERthinker AI Decision Assistant")
    print("=" * 60)
    print("I'll help you think through decisions with multiple perspectives.")
    print("Type 'quit' to exit the demo.")
    print("=" * 60)
    
    while True:
        question = input("\nWhat decision would you like help with?\n> ")
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("Thank you for using Overthinker AI. Happy decision-making!")
            break
        
        if not question.strip():
            continue
            
        print("\n" + "=" * 60)
        print("ANALYSIS:")
        print("=" * 60)
        
        try:
            analysis = analyzer.analyze_decision(question)
            print(analysis)
        except Exception as e:
            print(f"Sorry, I encountered an error: {e}")
        
        print("=" * 60)

if __name__ == "__main__":
    main()