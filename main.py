"""
FastAPI Web Interface for Overthinker AI
Deployment-ready REST API with web UI
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Optional
from overthinker.core.decision_analyzer import DecisionAnalyzer
import time
import os

# Initialize FastAPI app
app = FastAPI(
    title="Overthinker AI",
    description="Thoughtful AI assistant for decision-making",
    version="2.0.0"
)

# Add CORS middleware for web access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize analyzer (singleton)
analyzer = DecisionAnalyzer()


# Request/Response models
class DecisionRequest(BaseModel):
    question: str = Field(..., min_length=5, max_length=500)
    

class DecisionResponse(BaseModel):
    question: str
    analysis: str
    intent: str
    confidence: float
    processing_time: float
    

class HealthResponse(BaseModel):
    status: str
    version: str
    message: str


@app.get("/")
async def root():
    """Serve the main HTML page"""
    return FileResponse('static/index.html')


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for deployment platforms"""
    return HealthResponse(
        status="healthy",
        version="2.0.0",
        message="All systems operational"
    )


@app.post("/analyze", response_model=DecisionResponse)
async def analyze_decision(request: DecisionRequest):
    """
    Main endpoint to analyze a decision
    
    Example request:
    ```
    {
        "question": "Should I take the bus or Uber to work?"
    }
    ```
    """
    try:
        start_time = time.time()
        
        # Parse and classify
        parsed = analyzer.parser.parse(request.question)
        intent, confidence = analyzer.intent_classifier.classify_intent(
            request.question, parsed
        )
        
        # Generate analysis
        analysis = analyzer.analyze_decision(request.question)
        
        processing_time = time.time() - start_time
        
        return DecisionResponse(
            question=request.question,
            analysis=analysis,
            intent=intent,
            confidence=round(confidence, 2),
            processing_time=round(processing_time, 3)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Analysis failed: {str(e)}"
        )


@app.get("/intents")
async def get_supported_intents():
    """Get list of supported decision categories"""
    return {
        "intents": [
            "transportation",
            "purchase",
            "food",
            "career",
            "health",
            "relationship",
            "general"
        ],
        "total": 7
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
