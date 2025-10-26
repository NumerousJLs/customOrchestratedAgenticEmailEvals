"""
Message models for agent communication.
"""
from uagents import Model
from typing import Optional


class EmailDraftRequest(Model):
    """Request to analyze an email draft with a specific personality."""
    draft_email: str
    personality_type: str
    personality_description: Optional[str] = None
    sender_name: str = "User"


class PersonaResponse(Model):
    """Response from a persona agent simulating how they would react."""
    personality_type: str
    simulated_response: str
    emotional_tone: str
    key_concerns: list[str]


class CoachFeedbackRequest(Model):
    """Request for coach to analyze email and persona response."""
    draft_email: str
    personality_type: str
    persona_response: str
    emotional_tone: str
    key_concerns: list[str]


class CoachFeedback(Model):
    """Feedback from the coach agent."""
    overall_assessment: str
    draft_strengths: list[str]
    draft_weaknesses: list[str]
    persona_alignment: str
    improvement_suggestions: list[str]
    revised_draft_suggestion: Optional[str] = None


class PersonalityUpdate(Model):
    """Update personality characteristics for an existing persona agent."""
    personality_type: str
    mood: Optional[str] = None
    context: Optional[str] = None
    additional_traits: Optional[str] = None
