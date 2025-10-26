"""
Demo Orchestrator - Works without OpenAI API for testing.
"""
import asyncio
import sys
import os
from typing import Optional, Dict

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class EmailEvaluationOrchestrator:
    """
    Demo orchestrator that provides sample responses without calling OpenAI.
    Perfect for testing the UI and system without API costs.
    """

    def __init__(self):
        """Initialize the demo orchestrator."""
        print("🎭 Running in DEMO MODE - Using sample responses (no API calls)")

    async def evaluate_email(
        self,
        draft_email: str,
        personality_type: str,
        personality_description: Optional[str] = None,
        sender_name: str = "User"
    ) -> dict:
        """
        Generate demo evaluation responses.
        """
        print(f"\n{'='*60}")
        print(f"[DEMO] Evaluating email for personality: {personality_type}")
        print(f"{'='*60}\n")

        # Simulate processing time
        await asyncio.sleep(1)

        # Generate personality-specific demo responses
        persona_data = self._get_demo_persona_response(personality_type, draft_email)

        print(f"\nPersona Response ({persona_data['emotional_tone']}):")
        print(f"{persona_data['response']}\n")

        # Simulate processing time
        await asyncio.sleep(1)

        feedback_data = self._get_demo_coach_feedback(personality_type, draft_email)

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

    def _get_demo_persona_response(self, personality_type: str, email: str) -> Dict:
        """Generate demo persona responses based on personality type."""

        responses = {
            "angry_ceo": {
                "response": "I don't have time for vague updates. What's the timeline? What's the budget impact? Give me specifics, not fluff. Schedule a meeting with concrete numbers or don't bother.",
                "emotional_tone": "frustrated",
                "key_concerns": [
                    "Lack of specific details",
                    "No clear action items",
                    "Missing timeline information",
                    "Too casual for executive communication"
                ]
            },
            "chill_coworker": {
                "response": "Hey! Thanks for reaching out. Yeah, totally understand things can get hectic. Just keep me posted on how it's going - no rush on my end. Let me know if you need any help!",
                "emotional_tone": "supportive",
                "key_concerns": [
                    "Would appreciate more details eventually",
                    "Wants to stay in the loop",
                    "Prefers collaborative approach"
                ]
            },
            "stern_professor": {
                "response": "Your correspondence lacks proper structure and substantiation. Where is your supporting evidence? What methodology are you employing? Please revise this with proper citations and a clear analytical framework.",
                "emotional_tone": "critical",
                "key_concerns": [
                    "Insufficient academic rigor",
                    "Missing evidence and citations",
                    "Poor structural organization",
                    "Lacks proper formality"
                ]
            },
            "supportive_mentor": {
                "response": "Thanks for reaching out! I appreciate you keeping me informed. For next time, it would be helpful to include what specific challenges you're facing and what support you need from me. How can I help you work through this?",
                "emotional_tone": "encouraging",
                "key_concerns": [
                    "Could benefit from more specific details",
                    "Wants to understand how to help",
                    "Encourages proactive communication"
                ]
            },
            "anxious_client": {
                "response": "Wait, what does this mean for our timeline? I'm worried about our launch date. Can you give me exact dates? What happens if this takes longer? I need more information to feel comfortable with this.",
                "emotional_tone": "anxious",
                "key_concerns": [
                    "Timeline uncertainty",
                    "Potential delays",
                    "Lack of contingency plans",
                    "Insufficient reassurance"
                ]
            },
            "skeptical_investor": {
                "response": "I need data, not narratives. What's the quantifiable impact? Show me the metrics. What's your risk mitigation strategy? Where are the numbers that support this claim?",
                "emotional_tone": "skeptical",
                "key_concerns": [
                    "No financial data provided",
                    "Missing risk analysis",
                    "Lack of concrete metrics",
                    "Insufficient business justification"
                ]
            }
        }

        # Get response for personality type or use default
        return responses.get(
            personality_type.lower().replace(' ', '_'),
            {
                "response": "Thank you for your email. I've reviewed the contents and have some thoughts. Could we discuss this further?",
                "emotional_tone": "neutral",
                "key_concerns": [
                    "Would like more context",
                    "Prefers detailed communication",
                    "Wants clear next steps"
                ]
            }
        )

    def _get_demo_coach_feedback(self, personality_type: str, email: str) -> Dict:
        """Generate demo coach feedback."""

        # Check email length for some basic feedback
        word_count = len(email.split())
        has_specific_details = any(char.isdigit() for char in email)

        return {
            "overall_assessment": f"This email shows room for improvement when communicating with a {personality_type.replace('_', ' ')}. The tone is present but could be more aligned with the recipient's expectations.",
            "draft_strengths": [
                "Polite and professional tone",
                "Reaches out proactively" if word_count > 20 else "Concise communication",
                "Shows awareness of the situation"
            ],
            "draft_weaknesses": [
                "Lacks specific details and data points" if not has_specific_details else "Could provide more context",
                "Missing clear action items or next steps",
                "No proposed timeline or deadline",
                "Could be more direct in communication style"
            ],
            "persona_alignment": f"For a {personality_type.replace('_', ' ')}, this email misses key expectations. This personality type values specificity, actionable information, and clear structure. The current approach may come across as too vague or informal for their preferences.",
            "improvement_suggestions": [
                "Lead with the specific issue and proposed solution",
                "Include concrete data, timelines, and metrics",
                "Add clear action items with assigned owners",
                "Use a more direct, structured format",
                "Anticipate and address potential concerns upfront"
            ],
            "revised_draft_suggestion": f"""Subject: [Specific Topic] - Action Required by [Date]

Dear [Recipient],

I'm writing to inform you that [specific issue] has impacted [specific area]. Here's the situation:

Current Status: [Concrete details with numbers/dates]
Impact: [Quantified impact]
Proposed Solution: [Specific action plan]
New Timeline: [Exact dates]

Next Steps:
1. [Action item with owner and deadline]
2. [Action item with owner and deadline]

I'll follow up with a detailed report by [date]. Please let me know if you need any additional information.

Best regards,
[Your Name]"""
        }

    async def update_personality(
        self,
        personality_type: str,
        mood: Optional[str] = None,
        context: Optional[str] = None,
        additional_traits: Optional[str] = None
    ):
        """Demo personality update."""
        print(f"[DEMO] Personality update noted (demo mode - not persisted)")

    def print_detailed_feedback(self, result: dict):
        """Print detailed, formatted feedback."""
        if result.get("error"):
            print(f"\n❌ Error: {result['error']}")
            return

        print(f"\n{'='*60}")
        print("EVALUATION RESULTS (DEMO MODE)")
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

        print(f"\n{'='*60}")
        print("NOTE: This is demo mode with sample responses.")
        print("Add OpenAI API credits to use real AI analysis.")
        print(f"{'='*60}\n")
