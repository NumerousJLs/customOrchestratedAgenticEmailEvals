"""
Auto-detecting orchestrator that switches between real and demo mode.
"""
import os
import sys
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

load_dotenv()

# Check if we have a valid API key
api_key = os.getenv("OPENAI_API_KEY")
use_demo_mode = not api_key or api_key.startswith("sk-") == False or len(api_key) < 20

if use_demo_mode or os.getenv("DEMO_MODE", "").lower() == "true":
    print("🎭 Using DEMO MODE (no API calls)")
    print("   To use real OpenAI: Set OPENAI_API_KEY in .env file\n")
    from src.orchestrator_demo import EmailEvaluationOrchestrator
else:
    print("🤖 Using REAL MODE (OpenAI API)")
    print("   To use demo mode: Set DEMO_MODE=true in .env\n")
    from src.orchestrator_simple import EmailEvaluationOrchestrator

# Export the selected orchestrator
__all__ = ['EmailEvaluationOrchestrator']
