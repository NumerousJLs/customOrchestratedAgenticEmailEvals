"""
Basic usage example of the Email Evaluation System.

Make sure you have configured your .env file with OPENAI_API_KEY.

Run this script:
    python examples/basic_usage.py
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.orchestrator_auto import EmailEvaluationOrchestrator


async def main():
    """Run basic email evaluation example."""

    orchestrator = EmailEvaluationOrchestrator()

    # Example 1: Angry CEO
    print("\n" + "="*70)
    print("EXAMPLE 1: Testing with Angry CEO")
    print("="*70)

    draft_email_1 = """
    Hi,

    I wanted to touch base about the project timeline. Things have been a bit
    hectic on our end, and we're thinking we might need to adjust the deadline.
    There have been some unexpected challenges that popped up.

    Let me know your thoughts when you get a chance.

    Best,
    John
    """

    result_1 = await orchestrator.evaluate_email(
        draft_email=draft_email_1,
        personality_type="angry_ceo",
        sender_name="John"
    )

    orchestrator.print_detailed_feedback(result_1)

    # Example 2: Chill Coworker
    print("\n" + "="*70)
    print("EXAMPLE 2: Testing with Chill Coworker")
    print("="*70)

    draft_email_2 = """
    Hey!

    Quick heads up - I'm running a bit behind on the report. Should have it
    to you by end of week though. Let me know if that works!

    Thanks,
    Sarah
    """

    result_2 = await orchestrator.evaluate_email(
        draft_email=draft_email_2,
        personality_type="chill_coworker",
        sender_name="Sarah"
    )

    orchestrator.print_detailed_feedback(result_2)

    # Example 3: Stern Professor
    print("\n" + "="*70)
    print("EXAMPLE 3: Testing with Stern Professor")
    print("="*70)

    draft_email_3 = """
    Professor Smith,

    I wanted to ask about the assignment that's due next week. I'm having some
    trouble understanding the requirements. Could you maybe explain it again?

    Thanks,
    Mike
    """

    result_3 = await orchestrator.evaluate_email(
        draft_email=draft_email_3,
        personality_type="stern_professor",
        sender_name="Mike"
    )

    orchestrator.print_detailed_feedback(result_3)


if __name__ == "__main__":
    print("\n🚀 Starting Email Evaluation Examples...\n")

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
