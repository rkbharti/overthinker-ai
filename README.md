# Overthinker AI

A thoughtful AI assistant that helps with decision-making by providing multiple perspectives on everyday questions.

## Features

- Natural language processing using spaCy
- Entity recognition for people, organizations, locations, etc.
- Decision analysis for transportation, purchases, and general life choices
- Multi-perspective analysis (financial, practical, emotional, etc.)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/overthinker-ai.git
cd overthinker-ai

2. Create a virtual environment:
python -m venv .venv

3. Activate the virtual environment:
Windows: .venv\Scripts\activate
macOS/Linux: source .venv/bin/activate

4. Install dependencies:
pip install -r requirements.txt

5. Run the demo script:
python demo.py


Example questions to ask:

"Should I buy a new phone or repair my old one?"

"What's the best way to get to work today?"

"I'm not sure whether to cook at home or order food."


overthinker-ai/
├── overthinker/
│   ├── core/
│   │   ├── scenario_parser.py    # NLP parsing with spaCy
│   │   ├── decision_analyzer.py  # Decision analysis logic
│   │   └── __init__.py          # Package initialization
│   └── __init__.py
├── tests/
│   └── unit/
│       └── test_parser.py       # Unit tests
├── demo.py                      # Demo script
└── README.md                    # This file

Technologies Used
--Python 3.x
--spaCy for NLP
--pytest for testing


Future Enhancements
-- Web interface
--More decision categories
--Memory of previous decisions
--Integration with external APIs for real-time data
```
