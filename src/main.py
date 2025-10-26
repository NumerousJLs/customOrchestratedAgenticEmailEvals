"""
Main entry point - Starts all agents using Bureau.
"""
from uagents import Bureau
import asyncio
import sys
import os

# Add parent directory to path so we can import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents.persona_agent import PersonaAgent
from src.agents.coach_agent import CoachAgent


def main():
    """Start all agents in a Bureau."""
    # Create agents
    persona_agent_instance = PersonaAgent(seed="persona_agent_seed_123")
    coach_agent_instance = CoachAgent(seed="coach_agent_seed_456")

    # Create bureau to run agents together
    bureau = Bureau(
        port=8000,
        endpoint=["http://localhost:8000/submit"]
    )

    # Add agents to bureau
    bureau.add(persona_agent_instance.agent)
    bureau.add(coach_agent_instance.agent)

    print("="*60)
    print("Starting Email Evaluation Agent System")
    print("="*60)
    print(f"\nPersona Agent: http://localhost:{persona_agent_instance.agent._port}")
    print(f"Coach Agent: http://localhost:{coach_agent_instance.agent._port}")
    print(f"\nAgents are ready to receive requests...")
    print("="*60 + "\n")

    # Run the bureau
    bureau.run()


if __name__ == "__main__":
    main()
