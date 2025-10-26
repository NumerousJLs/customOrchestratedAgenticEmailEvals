"""
Register Chat Protocol Agent on Agentverse
Uses the uagents_core registration API
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import registration utilities
try:
    from uagents_core.utils.registration import (
        register_chat_agent,
        RegistrationRequestCredentials,
    )
    print("✅ uagents_core registration module imported")
except ImportError as e:
    print(f"❌ Failed to import uagents_core: {e}")
    print("   Try: pip install uagents")
    exit(1)

# Configuration
AGENT_NAME = "Email_Context_Analyzer"
AGENT_URL = "https://midi-routines-andrews-region.trycloudflare.com"

# Get credentials from environment
AGENTVERSE_KEY = os.getenv("AGENTVERSE_API_KEY")
AGENT_SEED = os.getenv("AGENT_SEED_PHRASE")

print("\n" + "="*70)
print("🚀 REGISTERING AGENT ON AGENTVERSE")
print("="*70)

# Validate credentials
if not AGENTVERSE_KEY:
    print("\n❌ ERROR: AGENTVERSE_API_KEY not found in .env")
    print("   Get your API key from: https://agentverse.ai/ → Settings → API Keys")
    exit(1)

if not AGENT_SEED:
    print("\n❌ ERROR: AGENT_SEED_PHRASE not found in .env")
    print("   Generate one: openssl rand -base64 32")
    exit(1)

print(f"\n📝 Agent Details:")
print(f"   Name: {AGENT_NAME}")
print(f"   URL: {AGENT_URL}")
print(f"   API Key: {AGENTVERSE_KEY[:20]}...")
print(f"   Seed: {AGENT_SEED[:20]}...")

print("\n🔄 Registering agent...")

try:
    result = register_chat_agent(
        AGENT_NAME,
        AGENT_URL,
        active=True,
        credentials=RegistrationRequestCredentials(
            agentverse_api_key=AGENTVERSE_KEY,
            agent_seed_phrase=AGENT_SEED,
        ),
    )

    print("\n✅ REGISTRATION SUCCESSFUL!")
    print("="*70)
    print(f"\n🎉 Your agent is now registered on Agentverse!")
    print(f"\nAgent Details:")
    print(f"   Name: {AGENT_NAME}")
    print(f"   URL: {AGENT_URL}")

    if hasattr(result, 'address'):
        print(f"   Address: {result.address}")

    if hasattr(result, 'agent_url'):
        print(f"   Dashboard: {result.agent_url}")

    print("\n📋 Next Steps:")
    print("   1. Visit https://agentverse.ai/ to see your agent")
    print("   2. Test it in the Agentverse chat interface")
    print("   3. Copy the agent address for your orchestrator")
    print("\n" + "="*70 + "\n")

except Exception as e:
    print(f"\n❌ REGISTRATION FAILED!")
    print(f"   Error: {str(e)}")
    print("\n🔍 Troubleshooting:")
    print("   - Check your AGENTVERSE_API_KEY is valid")
    print("   - Verify the tunnel URL is accessible")
    print("   - Make sure agent is responding at /status")
    print("   - Check Agentverse API documentation")
    exit(1)
