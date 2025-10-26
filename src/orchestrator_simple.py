"""
Simplified Orchestrator - Directly uses OpenAI without agent queries.
"""
from openai import OpenAI
import json
import sys
import os
from typing import Optional, Dict

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.config import (
    OPENAI_API_KEY,
    get_personality_prompt,
    COACH_SYSTEM_PROMPT
)


class EmailEvaluationOrchestrator:
    """
    Simplified orchestrator that directly uses OpenAI API.
    """

    def __init__(self):
        """Initialize the orchestrator."""
        self.client = OpenAI(api_key=OPENAI_API_KEY)

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

        try:
            # Step 1: Generate persona response
            print("Step 1: Getting persona response...")
            persona_data = await self._generate_persona_response(
                draft_email=draft_email,
                personality_type=personality_type,
                personality_description=personality_description,
                sender_name=sender_name
            )

            print(f"\nPersona Response ({persona_data['emotional_tone']}):")
            print(f"{persona_data['response']}\n")

            # Step 2: Get coach feedback
            print("Step 2: Getting coach feedback...")
            feedback_data = await self._generate_coach_feedback(
                draft_email=draft_email,
                personality_type=personality_type,
                persona_response=persona_data['response'],
                emotional_tone=persona_data['emotional_tone'],
                key_concerns=persona_data['key_concerns']
            )

            print(f"\nCoach Feedback:")
            print(f"Overall: {feedback_data['overall_assessment']}\n")

            return {
                "persona_response": {
                    "personality_type": personality_type,
                    "simulated_response": persona_data['response'],
                    "emotional_tone": persona_data['emotional_tone'],
                    "key_concerns": persona_data['key_concerns']
                },
                "coach_feedback": feedback_data,
                "error": None
            }

        except Exception as e:
            print(f"Error during evaluation: {str(e)}")
            return {
                "error": str(e),
                "persona_response": None,
                "coach_feedback": None
            }

    async def _generate_persona_response(
        self,
        draft_email: str,
        personality_type: str,
        personality_description: Optional[str],
        sender_name: str
    ) -> Dict:
        """Generate a persona response using OpenAI."""

        # Build personality prompt
        personality_prompt = get_personality_prompt(
            personality_type=personality_type,
            custom_description=personality_description
        )

        # System prompt
        system_prompt = f"""{personality_prompt}

You will receive a draft email. Your task is to:
1. Read the email as if you are the recipient with this personality
2. Generate a realistic response showing how you would react
3. Identify your emotional tone (e.g., frustrated, pleased, confused, supportive)
4. List your key concerns or thoughts about the email

Respond in JSON format:
{{
    "response": "Your email response here",
    "emotional_tone": "Your emotional state",
    "key_concerns": ["concern 1", "concern 2", ...]
}}
"""

        try:
            # Call OpenAI API
            completion = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Using gpt-4o-mini - widely available and cost-effective
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Draft email from {sender_name}:\n\n{draft_email}"}
                ],
                temperature=0.8,
                response_format={"type": "json_object"}
            )

            # Parse response
            response_text = completion.choices[0].message.content
            response_data = json.loads(response_text)

            return response_data

        except Exception as e:
            # Fallback response
            return {
                "response": f"[Error generating response: {str(e)}]",
                "emotional_tone": "confused",
                "key_concerns": ["Unable to process email"]
            }

    async def _generate_coach_feedback(
        self,
        draft_email: str,
        personality_type: str,
        persona_response: str,
        emotional_tone: str,
        key_concerns: list
    ) -> dict:
        """Generate comprehensive feedback using OpenAI."""

        # Build analysis prompt
        user_prompt = f"""Analyze this email communication:

DRAFT EMAIL:
{draft_email}

RECIPIENT PERSONALITY TYPE: {personality_type}

RECIPIENT'S RESPONSE:
{persona_response}

RECIPIENT'S EMOTIONAL TONE: {emotional_tone}

RECIPIENT'S KEY CONCERNS:
{', '.join(key_concerns)}

---

Provide comprehensive coaching feedback in JSON format:
{{
    "overall_assessment": "Brief overall assessment of the email's effectiveness",
    "draft_strengths": ["strength 1", "strength 2", ...],
    "draft_weaknesses": ["weakness 1", "weakness 2", ...],
    "persona_alignment": "Analysis of how well the email lands with this personality type",
    "improvement_suggestions": ["suggestion 1", "suggestion 2", ...],
    "revised_draft_suggestion": "Optional: A revised version of the email incorporating your suggestions"
}}
"""

        try:
            # Call OpenAI API
            completion = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Using gpt-4o-mini - widely available and cost-effective
                messages=[
                    {"role": "system", "content": COACH_SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )

            # Parse response
            response_text = completion.choices[0].message.content
            feedback_data = json.loads(response_text)

            return feedback_data

        except Exception as e:
            # Fallback response
            return {
                "overall_assessment": f"Error generating feedback: {str(e)}",
                "draft_strengths": ["Unable to analyze"],
                "draft_weaknesses": ["Unable to analyze"],
                "persona_alignment": "Unable to analyze",
                "improvement_suggestions": ["Please check API configuration"],
                "revised_draft_suggestion": None
            }

    async def update_personality(
        self,
        personality_type: str,
        mood: Optional[str] = None,
        context: Optional[str] = None,
        additional_traits: Optional[str] = None
    ):
        """
        Note: In this simplified version, personality updates aren't persisted.
        This is here for API compatibility.
        """
        print(f"Note: Personality updates in simplified mode aren't persisted.")

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
