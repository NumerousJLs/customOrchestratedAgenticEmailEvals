"""
Persona Agent - Simulates different personality types responding to emails.
"""
from uagents import Agent, Context, Model
from openai import OpenAI
import json
import sys
import os
from typing import Dict, Optional

# Add parent directory to path so we can import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.models.messages import EmailDraftRequest, PersonaResponse, PersonalityUpdate
from src.utils.config import (
    OPENAI_API_KEY,
    AGENT_HOST,
    PERSONA_AGENT_PORT,
    get_personality_prompt
)


class PersonaAgent:
    """
    Manages persona agents with different personalities.
    Each personality is stored in memory for the session.
    """

    def __init__(self, seed: str = "persona_agent_seed"):
        """Initialize the persona agent."""
        self.agent = Agent(
            name="persona_agent",
            seed=seed,
            port=PERSONA_AGENT_PORT,
            endpoint=[f"http://{AGENT_HOST}:{PERSONA_AGENT_PORT}/submit"]
        )

        # Store personality states (not persisted between sessions)
        self.personalities: Dict[str, Dict] = {}

        # OpenAI client
        self.client = OpenAI(api_key=OPENAI_API_KEY)

        # Set up message handlers
        self._setup_handlers()

    def _setup_handlers(self):
        """Set up message handlers for the agent."""

        @self.agent.on_message(model=EmailDraftRequest)
        async def handle_email_draft(ctx: Context, sender: str, msg: EmailDraftRequest):
            """Handle incoming email draft requests."""
            ctx.logger.info(f"Received email draft for personality: {msg.personality_type}")

            # Get or create personality
            personality_key = msg.personality_type.lower().replace(" ", "_")

            if personality_key not in self.personalities:
                ctx.logger.info(f"Creating new personality: {msg.personality_type}")
                self.personalities[personality_key] = {
                    "type": msg.personality_type,
                    "description": msg.personality_description,
                    "mood": None,
                    "context": None
                }
            else:
                ctx.logger.info(f"Using existing personality: {msg.personality_type}")

            # Get personality data
            personality_data = self.personalities[personality_key]

            # Generate response using OpenAI
            response_data = await self._generate_persona_response(
                draft_email=msg.draft_email,
                personality_type=msg.personality_type,
                personality_data=personality_data,
                sender_name=msg.sender_name
            )

            # Create response message
            response = PersonaResponse(
                personality_type=msg.personality_type,
                simulated_response=response_data["response"],
                emotional_tone=response_data["emotional_tone"],
                key_concerns=response_data["key_concerns"]
            )

            # Send response back
            await ctx.send(sender, response)
            ctx.logger.info(f"Sent persona response for {msg.personality_type}")

        @self.agent.on_message(model=PersonalityUpdate)
        async def handle_personality_update(ctx: Context, sender: str, msg: PersonalityUpdate):
            """Handle personality updates."""
            personality_key = msg.personality_type.lower().replace(" ", "_")

            if personality_key in self.personalities:
                ctx.logger.info(f"Updating personality: {msg.personality_type}")
                if msg.mood:
                    self.personalities[personality_key]["mood"] = msg.mood
                if msg.context:
                    self.personalities[personality_key]["context"] = msg.context
                if msg.additional_traits:
                    self.personalities[personality_key]["additional_traits"] = msg.additional_traits
            else:
                ctx.logger.warning(f"Personality {msg.personality_type} not found for update")

    async def _generate_persona_response(
        self,
        draft_email: str,
        personality_type: str,
        personality_data: Dict,
        sender_name: str
    ) -> Dict:
        """Generate a persona response using OpenAI."""

        # Build personality prompt
        personality_prompt = get_personality_prompt(
            personality_type=personality_type,
            custom_description=personality_data.get("description"),
            mood=personality_data.get("mood"),
            context=personality_data.get("context")
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

    def run(self):
        """Run the persona agent."""
        print(f"Starting Persona Agent on port {PERSONA_AGENT_PORT}...")
        self.agent.run()


if __name__ == "__main__":
    persona_agent = PersonaAgent()
    persona_agent.run()
