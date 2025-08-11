# 🧠 Overthinker AI - Scenario Analysis System

![Python](https://img.shields.io/badge/python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)

An AI system that analyzes text scenarios for risks, sentiment, and multiple outcome probabilities.

## 📦 Installation

```bash
# Clone repository
git clone https://github.com/yourusername/overthinker-ai.git
cd overthinker-ai

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.\.venv\Scripts\activate

# Activate (Mac/Linux)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_lg


 🚀 Quick Start
from overthinker.core.scenario_parser import ScenarioParser

parser = ScenarioParser()
analysis = parser.parse("Eating wild mushrooms could be dangerous")

print(f"Risk Score: {analysis['risk_score']:.0%}")
print(f"Main Entities: {analysis['entities']}")
print(f"Sentiment: {analysis['sentiment']:.2f} (-1 to 1 scale)")


🌟 Features
Multi-perspective analysis of scenarios

Risk probability scoring (0-100%)

Sentiment & emotion detection

Action/entity extraction

Knowledge-backed reasoning



📜 License
MIT © 2025 [Ravi Kumar]

CONTRIBUTION
Come Back Soon


