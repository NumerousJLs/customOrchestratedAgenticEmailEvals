"""
FastAPI Proxy - Queries all three agents for messages
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uagents import Model
from uagents.query import query
import asyncio
from typing import List
from pydantic import BaseModel

app = FastAPI(title="Email Analysis Agent Proxy")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models (matching agent definitions)
class GetMessagesRequest(Model):
    last_index: int = 0

class AgentMessage(BaseModel):
    timestamp: float
    agent: str
    type: str
    content: str
    recipient: str = ""

class MessagesResponse(Model):
    messages: List[AgentMessage]
    last_index: int

# Agent addresses and endpoints
AGENTS = {
    "analyzer": {
        "address": "agent1qw4m67px6nqk0zjmqgv23hux0phn5cukjj8ewt5qlmcvhwmaxxx8v2r3m85",
        "endpoint": "http://localhost:8001/submit"
    },
    "evaluator": {
        "address": "agent1qtdp0gp2v9zlz55q4j09lk8gy63uawz5ygxje4qzcgkvy04d0lwwcr9kcg9",
        "endpoint": "http://localhost:8002/submit"
    },
    "output": {
        "address": "agent1qfauvn87q8x7rthzmqnk8a4q2a5c7f39lklzphd05fpkgvjfv9scsxgupzv",
        "endpoint": "http://localhost:8003/submit"
    }
}

@app.get("/")
async def root():
    return {
        "service": "Email Analysis Agent Proxy",
        "agents": list(AGENTS.keys()),
        "endpoints": {
            "/messages": "Get messages from all agents",
            "/messages/{agent_name}": "Get messages from specific agent"
        }
    }

@app.get("/messages")
async def get_all_messages(last_index: int = 0):
    """Get messages from all agents"""
    all_messages = []

    for agent_name, agent_info in AGENTS.items():
        try:
            response = await query(
                destination=agent_info["address"],
                message=GetMessagesRequest(last_index=0),
                timeout=5.0
            )

            if response:
                messages = response.decode_payload()
                all_messages.extend([
                    {
                        "timestamp": msg.timestamp,
                        "agent": msg.agent,
                        "type": msg.type,
                        "content": msg.content,
                        "recipient": msg.recipient
                    }
                    for msg in messages.messages
                ])
        except Exception as e:
            print(f"Error querying {agent_name}: {e}")
            all_messages.append({
                "timestamp": 0,
                "agent": agent_name.title(),
                "type": "error",
                "content": f"Failed to query {agent_name}: {str(e)}",
                "recipient": ""
            })

    # Sort by timestamp
    all_messages.sort(key=lambda x: x["timestamp"])

    return {
        "messages": all_messages,
        "total": len(all_messages)
    }

@app.get("/messages/{agent_name}")
async def get_agent_messages(agent_name: str, last_index: int = 0):
    """Get messages from a specific agent"""
    if agent_name not in AGENTS:
        return {"error": f"Unknown agent: {agent_name}"}

    agent_info = AGENTS[agent_name]

    try:
        response = await query(
            destination=agent_info["address"],
            message=GetMessagesRequest(last_index=last_index),
            timeout=5.0
        )

        if response:
            messages = response.decode_payload()
            return {
                "messages": [
                    {
                        "timestamp": msg.timestamp,
                        "agent": msg.agent,
                        "type": msg.type,
                        "content": msg.content,
                        "recipient": msg.recipient
                    }
                    for msg in messages.messages
                ],
                "last_index": messages.last_index
            }
        else:
            return {"error": "No response from agent"}

    except Exception as e:
        return {"error": f"Failed to query agent: {str(e)}"}

@app.post("/analyze")
async def analyze_email(
    email_text: str,
    sender_info: str,
    recipient_info: str
):
    """
    Send an email to the Analyzer agent for analysis.
    NOTE: This is a direct send, not a query. The agents will process it.
    """
    from uagents.envelope import Envelope
    from uagents import Model
    import json
    import httpx

    class EmailInput(Model):
        email_text: str
        sender_info: str
        recipient_info: str
        original_chat_sender: str = ""

    email_input = EmailInput(
        email_text=email_text,
        sender_info=sender_info,
        recipient_info=recipient_info,
        original_chat_sender="proxy"
    )

    try:
        # Send directly to analyzer endpoint
        async with httpx.AsyncClient() as client:
            response = await client.post(
                AGENTS["analyzer"]["endpoint"],
                json=email_input.dict(),
                timeout=10.0
            )

            if response.status_code == 200:
                return {
                    "status": "submitted",
                    "message": "Email sent to Analyzer for processing"
                }
            else:
                return {
                    "status": "error",
                    "message": f"Failed to submit: {response.status_code}"
                }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to send email: {str(e)}"
        }

if __name__ == "__main__":
    import uvicorn
    print("Starting FastAPI proxy on http://localhost:5000")
    print("Agents:")
    for name, info in AGENTS.items():
        print(f"  - {name}: {info['address']}")
    print("\nEndpoints:")
    print("  GET  /messages - Get all messages from all agents")
    print("  GET  /messages/{agent_name} - Get messages from specific agent")
    print("  POST /analyze - Submit email for analysis")
    uvicorn.run(app, host="0.0.0.0", port=5000)
