"""
Orchestrator - Main application that coordinates persona and coach agents.
"""
from uagents import Agent, Context, Bureau
from uagents.query import query
import asyncio
import sys
import os
from typing import Optional

# Add parent directory to path so we can import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.messages import (
    EmailDraftRequest,
    PersonaResponse,
    CoachFeedbackRequest,
    CoachFeedback,
    PersonalityUpdate
)
from src.utils.config import AGENT_HOST, PERSONA_AGENT_PORT, COACH_AGENT_PORT


class EmailEvaluationOrchestrator:
    """
    Orchestrates the email evaluation workflow between persona and coach agents.
    """

    def __init__(self):
        """Initialize the orchestrator."""
        self.persona_agent_address = f"agent1qfpqn9jhvp9kcrygva7xvqq7xaq2c2h4y5vxqwq6h4q8tn9x7w2h7q9ycvp"
        self.coach_agent_address = f"agent1qv2cqk3d8yq89rnpyqm9qcgjfq0qvr3r4pjnvqp9xaq9ngwf0y6hs7kv8kd"

        # We'll update these with actual addresses when agents start
        self.persona_endpoint = f"http://{AGENT_HOST}:{PERSONA_AGENT_PORT}/submit"
        self.coach_endpoint = f"http://{AGENT_HOST}:{COACH_AGENT_PORT}/submit"

    async def evaluate_email(
        self,
        draft_email: str,
        personality_type: str,
        personality_description: Optional[str] = None,
        sender_name: str = "User"
    ) -> dict:
        """
        Evaluate an email draft with a specific personality and get coach feedback.

        Args:
            draft_email: The email draft to evaluate
            personality_type: The personality type to simulate (e.g., "angry_ceo")
            personality_description: Optional custom personality description
            sender_name: Name of the email sender

        Returns:
            Dictionary containing persona response and coach feedback
        """
        print(f"\n{'='*60}")
        print(f"Evaluating email for personality: {personality_type}")
        print(f"{'='*60}\n")

        # Step 1: Send email to persona agent
        print("Step 1: Sending email to persona agent...")
        email_request = EmailDraftRequest(
            draft_email=draft_email,
            personality_type=personality_type,
            personality_description=personality_description,
            sender_name=sender_name
        )

        try:
            # Query persona agent
            persona_response = await query(
                destination=self.persona_endpoint,
                message=email_request,
                timeout=30.0
            )

            if not persona_response:
                return {
                    "error": "No response from persona agent",
                    "persona_response": None,
                    "coach_feedback": None
                }

            # Parse persona response
            if isinstance(persona_response, PersonaResponse):
                persona_data = persona_response
            else:
                # Handle response data
                persona_data = PersonaResponse.parse_obj(persona_response)

            print(f"\nPersona Response ({persona_data.emotional_tone}):")
            print(f"{persona_data.simulated_response}\n")

            # Step 2: Send to coach for feedback
            print("Step 2: Sending to coach agent for feedback...")
            feedback_request = CoachFeedbackRequest(
                draft_email=draft_email,
                personality_type=personality_type,
                persona_response=persona_data.simulated_response,
                emotional_tone=persona_data.emotional_tone,
                key_concerns=persona_data.key_concerns
            )

            # Query coach agent
            coach_response = await query(
                destination=self.coach_endpoint,
                message=feedback_request,
                timeout=30.0
            )

            if not coach_response:
                return {
                    "persona_response": persona_data.dict(),
                    "coach_feedback": None,
                    "error": "No response from coach agent"
                }

            # Parse coach response
            if isinstance(coach_response, CoachFeedback):
                coach_data = coach_response
            else:
                coach_data = CoachFeedback.parse_obj(coach_response)

            print(f"\nCoach Feedback:")
            print(f"Overall: {coach_data.overall_assessment}\n")

            return {
                "persona_response": persona_data.dict(),
                "coach_feedback": coach_data.dict(),
                "error": None
            }

        except Exception as e:
            print(f"Error during evaluation: {str(e)}")
            return {
                "error": str(e),
                "persona_response": None,
                "coach_feedback": None
            }

    async def update_personality(
        self,
        personality_type: str,
        mood: Optional[str] = None,
        context: Optional[str] = None,
        additional_traits: Optional[str] = None
    ):
        """
        Update an existing personality's characteristics.

        Args:
            personality_type: The personality type to update
            mood: Current mood modifier
            context: Additional context
            additional_traits: Additional personality traits
        """
        update_msg = PersonalityUpdate(
            personality_type=personality_type,
            mood=mood,
            context=context,
            additional_traits=additional_traits
        )

        try:
            await query(
                destination=self.persona_endpoint,
                message=update_msg,
                timeout=10.0
            )
            print(f"Updated personality: {personality_type}")
        except Exception as e:
            print(f"Error updating personality: {str(e)}")

    def print_detailed_feedback(self, result: dict):
        """
        Print detailed, formatted feedback from the evaluation.

        Args:
            result: The result dictionary from evaluate_email
        """
        if result.get("error"):
            print(f"\n❌ Error: {result['error']}")
            return

        print(f"\n{'='*60}")
        print("EVALUATION RESULTS")
        print(f"{'='*60}\n")

        # Persona Response
        if result.get("persona_response"):
            persona = result["persona_response"]
            print(f"📧 PERSONA RESPONSE ({persona['personality_type']})")
            print(f"{'─'*60}")
            print(f"Emotional Tone: {persona['emotional_tone']}")
            print(f"\nResponse:")
            print(persona['simulated_response'])
            print(f"\nKey Concerns:")
            for concern in persona['key_concerns']:
                print(f"  • {concern}")
            print()

        # Coach Feedback
        if result.get("coach_feedback"):
            feedback = result["coach_feedback"]
            print(f"\n🎓 COACH FEEDBACK")
            print(f"{'─'*60}")
            print(f"\nOverall Assessment:")
            print(feedback['overall_assessment'])

            print(f"\n✅ Strengths:")
            for strength in feedback['draft_strengths']:
                print(f"  • {strength}")

            print(f"\n⚠️  Areas for Improvement:")
            for weakness in feedback['draft_weaknesses']:
                print(f"  • {weakness}")

            print(f"\n🎯 Persona Alignment:")
            print(feedback['persona_alignment'])

            print(f"\n💡 Improvement Suggestions:")
            for i, suggestion in enumerate(feedback['improvement_suggestions'], 1):
                print(f"  {i}. {suggestion}")

            if feedback.get('revised_draft_suggestion'):
                print(f"\n📝 Suggested Revision:")
                print(feedback['revised_draft_suggestion'])

        print(f"\n{'='*60}\n")


async def main_example():
    """Example usage of the orchestrator."""
    orchestrator = EmailEvaluationOrchestrator()

    # Example email draft
    draft_email = """
    Hi,

    I wanted to reach out about the project. I think we might need to push back
    the deadline a bit because there have been some unexpected challenges.
    Let me know what you think when you get a chance.

    Thanks,
    John
    """

    # Evaluate with angry CEO personality
    result = await orchestrator.evaluate_email(
        draft_email=draft_email,
        personality_type="angry_ceo",
        sender_name="John"
    )

    # Print formatted results
    orchestrator.print_detailed_feedback(result)


if __name__ == "__main__":
    asyncio.run(main_example())
