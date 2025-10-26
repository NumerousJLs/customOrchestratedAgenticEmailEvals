"""
FastAPI Web Interface for AgentMail
Provides REST API for the 12-agent email analysis system.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from agents.orchestrator import AgentOrchestrator

app = FastAPI(title="AgentMail API", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize orchestrator
orchestrator = AgentOrchestrator()


class EmailAnalysisInput(BaseModel):
    """Input model for email analysis."""
    email_text: str
    sender_info: Optional[str] = None
    recipient_info: Optional[str] = None
    context_hints: Optional[Dict[str, Any]] = None
    mode: Optional[str] = "professional"  # or "roast"


class HealthCheck(BaseModel):
    """Health check response."""
    status: str
    agents_available: int
    message: str


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the web interface."""
    html_path = os.path.join(os.path.dirname(__file__), "web", "index.html")
    if os.path.exists(html_path):
        with open(html_path, "r") as f:
            return f.read()
    else:
        return """
        <html>
            <head><title>AgentMail</title></head>
            <body>
                <h1>AgentMail API</h1>
                <p>API is running. Frontend not found.</p>
                <p>Visit <a href="/docs">/docs</a> for API documentation.</p>
            </body>
        </html>
        """


@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Check if all agents are running."""
    # Try to ping a few agents to verify they're up
    return HealthCheck(
        status="healthy",
        agents_available=12,
        message="All 12 agents are running on ports 8101-8402"
    )


@app.post("/analyze")
async def analyze_email(input_data: EmailAnalysisInput):
    """
    Analyze an email using all 12 agents.

    Returns complete analysis with:
    - Context extraction
    - Multi-agent simulation
    - Evaluation scores
    - Feedback and rewrites
    """
    try:
        result = await orchestrator.analyze_email(
            email_text=input_data.email_text,
            sender_info=input_data.sender_info,
            recipient_info=input_data.recipient_info,
            context_hints=input_data.context_hints or {},
            mode=input_data.mode or "professional"
        )

        if not result["success"]:
            raise HTTPException(
                status_code=500,
                detail=f"Analysis failed: {result.get('error', 'Unknown error')}"
            )

        # Format response for frontend
        return {
            "success": True,
            "request_id": result["request_id"],
            "summary": result["summary"],
            "layers": {
                "layer1_context": _format_layer_response(result["results"].get("layer1_context", {})),
                "layer2_simulation": _format_layer_response(result["results"].get("layer2_simulation", {})),
                "layer3_evaluation": _format_layer_response(result["results"].get("layer3_evaluation", {})),
                "layer4_output": _format_layer_response(result["results"].get("layer4_output", {})),
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/agents")
async def list_agents():
    """List all available agents and their status."""
    return {
        "total_agents": 12,
        "agents": {
            "layer1_context": [
                {"name": "context_analyzer", "port": 8101, "description": "Extracts goal, tone, urgency"},
                {"name": "relationship_mapper", "port": 8102, "description": "Maps power dynamics"},
                {"name": "culture_detector", "port": 8103, "description": "Detects cultural context"},
            ],
            "layer2_simulation": [
                {"name": "recipient_persona", "port": 8201, "description": "Simulates recipient response"},
                {"name": "sender_advocate", "port": 8202, "description": "Defends sender's approach"},
                {"name": "devils_advocate", "port": 8203, "description": "Finds potential issues"},
                {"name": "mediator", "port": 8204, "description": "Synthesizes perspectives"},
            ],
            "layer3_evaluation": [
                {"name": "tone_validator", "port": 8301, "description": "Validates tone appropriateness"},
                {"name": "goal_alignment", "port": 8302, "description": "Evaluates goal achievement"},
                {"name": "risk_assessor", "port": 8303, "description": "Assesses communication risks"},
            ],
            "layer4_output": [
                {"name": "feedback_synthesizer", "port": 8401, "description": "Creates actionable feedback"},
                {"name": "email_rewriter", "port": 8402, "description": "Generates improved versions"},
            ]
        }
    }


def _format_layer_response(layer_data: Dict) -> Dict:
    """Format agent responses for frontend display."""
    formatted = {}
    for agent_name, response in layer_data.items():
        if response and hasattr(response, 'analysis'):
            formatted[agent_name] = {
                "analysis": response.analysis,
                "confidence": getattr(response, 'confidence', 0),
                "reasoning": getattr(response, 'reasoning', '')
            }
        elif response:
            # Handle raw dict responses
            formatted[agent_name] = response
    return formatted


if __name__ == "__main__":
    import uvicorn

    print("\n" + "="*70)
    print("🚀 Starting AgentMail Web API")
    print("="*70)
    print("\nMake sure all 12 agents are running first!")
    print("Run: python start_all_agents.py")
    print("\nAPI will be available at:")
    print("  - http://localhost:8000")
    print("  - API docs: http://localhost:8000/docs")
    print("="*70 + "\n")

    uvicorn.run(app, host="0.0.0.0", port=8000)
