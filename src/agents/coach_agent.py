"""
Coach Agent - Analyzes emails and provides expert feedback.
"""
from uagents import Agent, Context
from openai import OpenAI
import json
import sys
import os

# Add parent directory to path so we can import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.models.messages import CoachFeedbackRequest, CoachFeedback
from src.utils.config import (
    OPENAI_API_KEY,
    AGENT_HOST,
    COACH_AGENT_PORT,
    COACH_SYSTEM_PROMPT
)


class CoachAgent:
    """
    Expert coach that analyzes email drafts and provides feedback.
    """

    def __init__(self, seed: str = "coach_agent_seed"):
        """Initialize the coach agent."""
        self.agent = Agent(
            name="coach_agent",
            seed=seed,
            port=COACH_AGENT_PORT,
            endpoint=[f"http://{AGENT_HOST}:{COACH_AGENT_PORT}/submit"]
        )

        # OpenAI client
        self.client = OpenAI(api_key=OPENAI_API_KEY)

        # Set up message handlers
        self._setup_handlers()

    def _setup_handlers(self):
        """Set up message handlers for the agent."""

        @self.agent.on_message(model=CoachFeedbackRequest)
        async def handle_feedback_request(ctx: Context, sender: str, msg: CoachFeedbackRequest):
            """Handle incoming feedback requests."""
            ctx.logger.info(f"Received feedback request for {msg.personality_type} personality")

            # Generate feedback using OpenAI
            feedback_data = await self._generate_feedback(
                draft_email=msg.draft_email,
                personality_type=msg.personality_type,
                persona_response=msg.persona_response,
                emotional_tone=msg.emotional_tone,
                key_concerns=msg.key_concerns
            )

            # Create feedback message
            feedback = CoachFeedback(
                overall_assessment=feedback_data["overall_assessment"],
                draft_strengths=feedback_data["draft_strengths"],
                draft_weaknesses=feedback_data["draft_weaknesses"],
                persona_alignment=feedback_data["persona_alignment"],
                improvement_suggestions=feedback_data["improvement_suggestions"],
                revised_draft_suggestion=feedback_data.get("revised_draft_suggestion")
            )

            # Send feedback back
            await ctx.send(sender, feedback)
            ctx.logger.info(f"Sent coaching feedback")

    async def _generate_feedback(
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

    def run(self):
        """Run the coach agent."""
        print(f"Starting Coach Agent on port {COACH_AGENT_PORT}...")
        self.agent.run()


if __name__ == "__main__":
    coach_agent = CoachAgent()
    coach_agent.run()
