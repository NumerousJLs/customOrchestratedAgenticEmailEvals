"""
Example of using custom personality types.

Make sure you have configured your .env file with OPENAI_API_KEY.

Run this script:
    python examples/custom_personality.py
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.orchestrator_auto import EmailEvaluationOrchestrator


async def main():
    """Demonstrate custom personality usage."""

    orchestrator = EmailEvaluationOrchestrator()

    # Custom Personality: Overworked Junior Developer
    print("\n" + "="*70)
    print("EXAMPLE: Custom Personality - Overworked Junior Developer")
    print("="*70)

    custom_personality_description = """
    You are a junior developer who is overwhelmed with work and struggling to keep up.
    You are:
    - Eager to please but stressed about deadlines
    - Sometimes confused by technical jargon
    - Worried about making mistakes
    - Appreciative of clear instructions and guidance
    - Anxious about asking for help but know you need it
    You respond with a mix of enthusiasm and anxiety, and you need clear,
    actionable guidance.
    """

    draft_email = """
    Hey,

    I need you to refactor the authentication module and optimize the database
    queries. Also, can you look into that bug in production? It's pretty urgent.
    Should be straightforward.

    Let me know when it's done.

    Thanks
    """

    result = await orchestrator.evaluate_email(
        draft_email=draft_email,
        personality_type="overworked_junior_dev",
        personality_description=custom_personality_description,
        sender_name="Senior Developer"
    )

    orchestrator.print_detailed_feedback(result)

    # Example of updating personality with mood
    print("\n" + "="*70)
    print("EXAMPLE: Updating Personality Mood")
    print("="*70)

    print("\nUpdating 'angry_ceo' personality with current mood and context...")

    await orchestrator.update_personality(
        personality_type="angry_ceo",
        mood="extremely frustrated after a bad quarterly meeting",
        context="Just found out the project is over budget"
    )

    print("Now testing the same email with updated personality mood:\n")

    draft_email_2 = """
    Hi,

    Quick update on the project status. We're making good progress but hit
    a small roadblock with the vendor integration. Should be resolved soon.

    Best,
    Team Lead
    """

    result_2 = await orchestrator.evaluate_email(
        draft_email=draft_email_2,
        personality_type="angry_ceo",
        sender_name="Team Lead"
    )

    orchestrator.print_detailed_feedback(result_2)


if __name__ == "__main__":
    print("\n🚀 Starting Custom Personality Examples...\n")

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Examples interrupted.\n")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure:")
        print("1. Your .env file is configured with OPENAI_API_KEY")
        print("2. All dependencies are installed (pip install -r requirements.txt)")
        print("3. You have an active internet connection\n")
