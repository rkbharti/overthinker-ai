# 🧠 Overthinker AI - Scenario Analysis Engine

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

An AI system that analyzes scenarios from multiple perspectives, assessing risks, sentiment, and ethical implications.

```mermaid
graph TD
    A[User Input] --> B(Text Parsing)
    B --> C[Entity Recognition]
    B --> D[Action Extraction]
    C --> E[Risk Assessment]
    D --> F[Probability Modeling]
    E --> G[Output Visualization]
    F --> G

    📦 Installation
    git clone https://github.com/yourusername/overthinker-ai.git
    cd overthinker-ai
    #setup variable env
    python -m venv .venv
    # Windows:
    .\.venv\Scripts\activate
    # Mac/Linux:
    source .venv/bin/activate


    Install dependencies 
    pip install -r requirements.txt
    python -m spacy download en_core_web_lg
    python -m textblob.download_corpora

    graph LR
    A[overthinker-ai/] --> B[core/]
    A --> C[tests/]
    A --> D[data/]
    B --> E[scenario_parser.py]
    B --> F[probability_engine.py]
    C --> G[unit/]
    D --> H[knowledge_graphs/]