"""
Get the agent address from the seed phrase
"""
import os
from dotenv import load_dotenv

load_dotenv()

try:
    from uagents import Identity

    seed = os.getenv("AGENT_SEED_PHRASE")

    if seed:
        identity = Identity.from_seed(seed, 0)
        print("\n" + "="*70)
        print("🎯 YOUR AGENT ADDRESS")
        print("="*70)
        print(f"\nAgent Address: {identity.address}")
        print(f"\nThis is your agent's unique identifier on the Fetch.ai network!")
        print("\n📋 Use this address in your orchestrator:")
        print(f'   "context_analyzer": "{identity.address}"')
        print("\n" + "="*70 + "\n")
    else:
        print("❌ AGENT_SEED_PHRASE not found in .env")

except ImportError:
    print("❌ uagents not installed")
    print("   Try: pip install uagents")
