"""
Chat Protocol Agent - Official uagents_core Pattern
Simple agent using FastAPI + uagents_core
"""
import os
from typing import cast
from dotenv import load_dotenv

# Load environment
load_dotenv()

from fastapi import FastAPI
from uagents_core.contrib.protocols.chat import (
    ChatMessage,
    TextContent,
)
from uagents_core.envelope import Envelope
from uagents_core.identity import Identity
from uagents_core.utils.messages import parse_envelope, send_message_to_agent
from anthropic import Anthropic
import json

# Agent configuration
name = "Email Context Analyzer"
identity = Identity.from_seed(os.environ["AGENT_SEED_PHRASE"], 0)
readme = """# Email Context Analyzer
AI-powered email analysis agent using Claude.

Analyzes emails to extract:
- Primary goal and intent
- Tone and emotional undercurrent
- Urgency level
- Key action items
"""

# Claude client
claude = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

app = FastAPI(title=name)

print("\n" + "="*70)
print(f"🚀 Starting {name}")
print("="*70)
print(f"Agent Address: {identity.address}")
print(f"Port: 8101")
print("="*70 + "\n")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": name,
        "address": identity.address,
        "status": "running",
        "endpoints": ["/status", "/chat"],
        "readme": readme
    }


@app.get("/status")
async def healthcheck():
    """Health check endpoint required by Agentverse"""
    return {
        "status": "OK - Agent is running",
        "agent": name,
        "address": identity.address,
        "ready": True
    }


@app.post("/chat")
async def handle_message(env: Envelope):
    """Handle incoming chat messages"""
    try:
        msg = cast(ChatMessage, parse_envelope(env, ChatMessage))
        message_text = msg.text()

        print(f"📩 Received message from {env.sender}")
        print(f"   Message: {message_text[:100]}...")

        # Parse as JSON if possible (for structured requests)
        try:
            request_data = json.loads(message_text)
            email_text = request_data.get("email_text", message_text)
        except json.JSONDecodeError:
            email_text = message_text

        # Analyze with Claude
        print(f"🤖 Analyzing with Claude...")

        system_prompt = """You are an expert email analyst. Analyze emails and extract:
1. Primary Goal: What does the sender want?
2. Tone: Formal, casual, urgent, friendly, etc.
3. Urgency Level: 1-5
4. Subject Matter: Brief topic
5. Action Items: What's requested
6. Emotional Undercurrent: Hidden emotions

Respond in JSON format:
{
    "primary_goal": "string",
    "tone": "string",
    "urgency_level": 1-5,
    "subject_matter": "string",
    "action_items": ["item1", "item2"],
    "emotional_undercurrent": "string",
    "confidence": 0.0-1.0
}"""

        response = claude.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            temperature=0.7,
            system=system_prompt,
            messages=[{
                "role": "user",
                "content": f"Analyze this email:\n\n{email_text}"
            }]
        )

        analysis_text = response.content[0].text

        print(f"✅ Analysis complete")
        print(f"   Response: {analysis_text[:100]}...")

        # Send response back
        send_message_to_agent(
            destination=env.sender,
            msg=ChatMessage([TextContent(analysis_text)]),
            sender=identity,
        )

        return {"status": "processed", "sender": env.sender}

    except Exception as e:
        print(f"❌ Error: {str(e)}")

        # Send error response
        send_message_to_agent(
            destination=env.sender,
            msg=ChatMessage([TextContent(f"Error processing message: {str(e)}")]),
            sender=identity,
        )

        return {"status": "error", "error": str(e)}


if __name__ == "__main__":
    import uvicorn

    print("🔥 Starting FastAPI server...")
    print("   Visit http://localhost:8101/status to check health")
    print("   Agent ready to receive messages at /chat\n")

    uvicorn.run(app, host="0.0.0.0", port=8101)
