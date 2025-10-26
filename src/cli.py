"""
Interactive CLI for email evaluation system.
"""
import asyncio
import sys
import os
from typing import Optional

# Add parent directory to path so we can import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.orchestrator_auto import EmailEvaluationOrchestrator
from src.utils.config import PERSONALITY_TEMPLATES


class EmailEvaluationCLI:
    """Interactive command-line interface for email evaluation."""

    def __init__(self):
        """Initialize the CLI."""
        self.orchestrator = EmailEvaluationOrchestrator()

    def print_header(self):
        """Print welcome header."""
        print("\n" + "="*60)
        print("📧 EMAIL EVALUATION SYSTEM")
        print("="*60)
        print("\nThis system helps you test how your emails will land")
        print("with different personality types and get coaching feedback.\n")

    def list_personalities(self):
        """List available personality types."""
        print("\n📋 Available Personality Types:")
        print("─"*60)
        for i, (key, description) in enumerate(PERSONALITY_TEMPLATES.items(), 1):
            # Get first line of description
            first_line = description.split('\n')[0]
            print(f"{i}. {key.replace('_', ' ').title()}")
            print(f"   {first_line[:70]}...")
        print()

    def get_multiline_input(self, prompt: str) -> str:
        """Get multiline input from user."""
        print(prompt)
        print("(Enter your email below. Type 'END' on a new line when done)")
        print("─"*60)

        lines = []
        while True:
            try:
                line = input()
                if line.strip().upper() == 'END':
                    break
                lines.append(line)
            except EOFError:
                break

        return '\n'.join(lines)

    async def evaluate_email_interactive(self):
        """Interactive email evaluation flow."""
        print("\n" + "─"*60)

        # Get email draft
        draft_email = self.get_multiline_input("\n📝 Enter your email draft:")

        if not draft_email.strip():
            print("\n❌ No email entered. Returning to menu.")
            return

        # Show personality options
        self.list_personalities()

        # Get personality choice
        personality_input = input("Enter personality type (name or number) or 'custom': ").strip()

        personality_type = None
        custom_description = None

        # Handle custom personality
        if personality_input.lower() == 'custom':
            personality_type = input("Enter personality name: ").strip()
            custom_description = self.get_multiline_input(
                "\n📝 Describe the personality:"
            )
        else:
            # Try to match by number or name
            try:
                idx = int(personality_input) - 1
                personality_type = list(PERSONALITY_TEMPLATES.keys())[idx]
            except (ValueError, IndexError):
                # Try to match by name
                normalized_input = personality_input.lower().replace(' ', '_')
                if normalized_input in PERSONALITY_TEMPLATES:
                    personality_type = normalized_input
                else:
                    print(f"\n❌ Unknown personality type: {personality_input}")
                    return

        # Get sender name
        sender_name = input("\nYour name (optional, press Enter to skip): ").strip() or "User"

        # Perform evaluation
        print("\n⏳ Evaluating your email...")
        print("This may take a moment as we consult with the agents...\n")

        result = await self.orchestrator.evaluate_email(
            draft_email=draft_email,
            personality_type=personality_type,
            personality_description=custom_description,
            sender_name=sender_name
        )

        # Display results
        self.orchestrator.print_detailed_feedback(result)

    async def update_personality_interactive(self):
        """Interactive personality update flow."""
        print("\n" + "─"*60)

        self.list_personalities()

        personality_type = input("Enter personality type to update: ").strip()
        mood = input("Current mood (optional): ").strip() or None
        context = input("Additional context (optional): ").strip() or None
        traits = input("Additional traits (optional): ").strip() or None

        await self.orchestrator.update_personality(
            personality_type=personality_type,
            mood=mood,
            context=context,
            additional_traits=traits
        )

        print("\n✅ Personality updated!")

    async def run(self):
        """Run the interactive CLI."""
        self.print_header()

        while True:
            print("\n" + "─"*60)
            print("MENU:")
            print("1. Evaluate an email")
            print("2. List personality types")
            print("3. Update personality mood/context")
            print("4. Exit")
            print("─"*60)

            choice = input("\nEnter your choice (1-4): ").strip()

            if choice == '1':
                await self.evaluate_email_interactive()
            elif choice == '2':
                self.list_personalities()
            elif choice == '3':
                await self.update_personality_interactive()
            elif choice == '4':
                print("\n👋 Goodbye!\n")
                break
            else:
                print("\n❌ Invalid choice. Please enter 1-4.")


async def main():
    """Main entry point for CLI."""
    cli = EmailEvaluationCLI()
    try:
        await cli.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!\n")
        sys.exit(0)


if __name__ == "__main__":
    asyncio.run(main())
