"""
Simple test of the Agentverse orchestrator with one agent.
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from agents.orchestrator_agentverse import AgentverseOrchestrator


async def main():
    """Test orchestrator with locally running agent."""

    print("\n" + "="*70)
    print("🧪 TESTING AGENTVERSE ORCHESTRATOR")
    print("="*70)

    # Create orchestrator with only context_analyzer
    orchestrator = AgentverseOrchestrator({
        "context_analyzer": "http://localhost:8101",
    })

    # Test email
    test_email = """
    Hi team,

    Just wanted to touch base about the project deadline.
    Can we push it back a week?

    Thanks!
    """

    print("\n📧 Test Email:")
    print(test_email)

    try:
        print("\n🚀 Sending to agent...")

        # Make a simple request to context_analyzer
        result = await orchestrator._query_agent(
            "context_analyzer",
            {
                "email_text": test_email,
                "sender_info": "Project Manager",
                "recipient_info": "Development Team",
                "request_id": "test-orchestrator-001",
                "mode": "professional"
            }
        )

        print("\n✅ AGENT RESPONSE:")
        print("="*70)

        if result:
            print(f"Agent: {result.get('agent_name')}")
            print(f"Type: {result.get('agent_type')}")
            print(f"Confidence: {result.get('confidence')}")
            print(f"\n📊 Analysis:")

            analysis = result.get('analysis', {})
            for key, value in analysis.items():
                print(f"  • {key}: {value}")

            print(f"\n💡 Reasoning:")
            print(f"  {result.get('reasoning')}")
        else:
            print("❌ No response from agent")

    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

    finally:
        await orchestrator.close()

    print("\n" + "="*70)
    print("✅ TEST COMPLETE")
    print("="*70 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
