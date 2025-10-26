"""
FastAPI Proxy - Queries agents on Agentverse (or local)
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uagents import Model
from uagents.query import query
import asyncio
from typing import List, Optional, Dict, Any
import os
import ssl
import certifi

# Configure SSL to use certifi certificates
os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

app = FastAPI(title="Email Analysis Agent Proxy - Agentverse")

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

class AgentMessage(Model):
    timestamp: float
    agent: str
    type: str
    content: str
    recipient: str = ""

class MessagesResponse(Model):
    messages: List[Dict[str, Any]]
    last_index: int

class EmailInput(Model):
    email_text: str
    sender_info: str
    recipient_info: str
    original_chat_sender: str = ""

# ============================================
# CONFIGURE YOUR AGENT ADDRESSES HERE
# ============================================
# Get these from your Agentverse console!
AGENT_ADDRESSES = {
    "analyzer": os.getenv("ANALYZER_ADDRESS", "agent1qtfaxjdl7kp5h89te4966857zfrhpp5zmtty39gzcnvq4tm65nxtv9w0cjl"),
    "evaluator": os.getenv("EVALUATOR_ADDRESS", "agent1qgam0z5083wwtn8zztetyy9jjqlqvqj4a62nzecfw27gg2xg75revacc48n"),
    "output": os.getenv("OUTPUT_ADDRESS", "agent1qgwf37l6sq7xe7nvjgx2679rj7asw3lka5df5k5guqf2xm7ksruz536eeet")
}

@app.get("/")
async def root():
    return {
        "service": "Email Analysis Agent Proxy - Agentverse",
        "mode": "Agentverse",
        "agents": AGENT_ADDRESSES,
        "endpoints": {
            "/messages": "Get messages from all agents",
            "/messages/{agent_name}": "Get messages from specific agent",
            "/analyze": "Submit email for analysis"
        }
    }

@app.get("/messages")
async def get_all_messages(last_index: int = 0):
    """Get messages from all agents on Agentverse"""
    all_messages = []

    for agent_name, agent_address in AGENT_ADDRESSES.items():
        try:
            print(f"Querying {agent_name} at {agent_address}...")
            response = await query(
                destination=agent_address,
                message=GetMessagesRequest(last_index=0),
                timeout=10.0
            )

            if response:
                print(f"✓ Got response from {agent_name}, type: {type(response)}")

                # Check if it's a MsgStatus or actual response
                if hasattr(response, 'decode_payload'):
                    payload = response.decode_payload()
                    print(f"Decoded payload: {type(payload)}")

                    # Handle the messages - they come as dicts
                    if hasattr(payload, 'messages'):
                        for msg in payload.messages:
                            if isinstance(msg, dict):
                                all_messages.append(msg)
                            else:
                                all_messages.append({
                                    "timestamp": msg.timestamp,
                                    "agent": msg.agent,
                                    "type": msg.type,
                                    "content": msg.content,
                                    "recipient": msg.recipient if hasattr(msg, 'recipient') else ""
                                })
                else:
                    # It's a MsgStatus, agent responded but no query handler
                    print(f"Got MsgStatus from {agent_name}: {response}")
                    all_messages.append({
                        "timestamp": 0,
                        "agent": agent_name.title(),
                        "type": "info",
                        "content": f"Agent {agent_name} responded but query handler may not be deployed",
                        "recipient": ""
                    })
            else:
                print(f"✗ No response from {agent_name}")
                all_messages.append({
                    "timestamp": 0,
                    "agent": agent_name.title(),
                    "type": "info",
                    "content": f"No messages yet from {agent_name}",
                    "recipient": ""
                })
        except Exception as e:
            print(f"✗ Error querying {agent_name}: {e}")
            import traceback
            traceback.print_exc()
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
    """Get messages from a specific agent on Agentverse"""
    if agent_name not in AGENT_ADDRESSES:
        return {"error": f"Unknown agent: {agent_name}"}

    agent_address = AGENT_ADDRESSES[agent_name]

    try:
        print(f"Querying {agent_name} at {agent_address}...")
        response = await query(
            destination=agent_address,
            message=GetMessagesRequest(last_index=last_index),
            timeout=10.0
        )

        if response:
            print(f"✓ Got response from {agent_name}")
            payload = response.decode_payload()
            messages_list = []

            if hasattr(payload, 'messages'):
                for msg in payload.messages:
                    if isinstance(msg, dict):
                        messages_list.append(msg)
                    else:
                        messages_list.append({
                            "timestamp": msg.timestamp,
                            "agent": msg.agent,
                            "type": msg.type,
                            "content": msg.content,
                            "recipient": msg.recipient if hasattr(msg, 'recipient') else ""
                        })

            return {
                "messages": messages_list,
                "last_index": payload.last_index if hasattr(payload, 'last_index') else len(messages_list)
            }
        else:
            return {
                "error": "No response from agent",
                "messages": [],
                "last_index": 0
            }

    except Exception as e:
        print(f"✗ Error querying {agent_name}: {e}")
        return {"error": f"Failed to query agent: {str(e)}"}

@app.post("/analyze")
async def analyze_email(
    email_text: str,
    sender_info: str,
    recipient_info: str
):
    """
    Send an email to the Analyzer agent on Agentverse for analysis.

    NOTE: This sends a message to the agent. The agent will process it
    and you can poll /messages to get updates.
    """
    email_input = EmailInput(
        email_text=email_text,
        sender_info=sender_info,
        recipient_info=recipient_info,
        original_chat_sender="web_app"
    )

    try:
        analyzer_address = AGENT_ADDRESSES["analyzer"]
        print(f"Sending email to Analyzer at {analyzer_address}...")

        # For Agentverse, we need to use the send pattern
        # Query is for request-response, but EmailInput is fire-and-forget
        # We'll need to use the almanac contract to send messages

        # For now, return the address for manual sending via Agentverse console
        return {
            "status": "ready",
            "message": "To send via Agentverse console, use this data:",
            "analyzer_address": analyzer_address,
            "payload": email_input.dict(),
            "note": "For programmatic sending, you'll need to implement agent-to-agent messaging or use a local agent as a proxy"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to prepare email: {str(e)}"
        }

@app.get("/status")
async def check_agent_status():
    """Check if agents are responding on Agentverse"""
    status = {}

    for agent_name, agent_address in AGENT_ADDRESSES.items():
        try:
            print(f"Checking {agent_name}...")
            response = await query(
                destination=agent_address,
                message=GetMessagesRequest(last_index=0),
                timeout=5.0
            )

            if response:
                payload = response.decode_payload()
                msg_count = len(payload.messages) if hasattr(payload, 'messages') else 0
                status[agent_name] = {
                    "status": "online",
                    "address": agent_address,
                    "message_count": msg_count
                }
            else:
                status[agent_name] = {
                    "status": "no_response",
                    "address": agent_address
                }
        except Exception as e:
            status[agent_name] = {
                "status": "error",
                "address": agent_address,
                "error": str(e)
            }

    return status

if __name__ == "__main__":
    import uvicorn
    print("="*60)
    print("FastAPI Proxy for Agentverse Agents")
    print("="*60)
    print("\nConfigured Agents:")
    for name, address in AGENT_ADDRESSES.items():
        print(f"  {name}: {address}")
    print("\nStarting server on http://localhost:5000")
    print("\nTo update agent addresses:")
    print("  1. Edit AGENT_ADDRESSES in this file")
    print("  2. Or set environment variables:")
    print("     export ANALYZER_ADDRESS=agent1q...")
    print("     export EVALUATOR_ADDRESS=agent1q...")
    print("     export OUTPUT_ADDRESS=agent1q...")
    print("\nEndpoints:")
    print("  GET  / - Proxy status and agent info")
    print("  GET  /status - Check if agents are online")
    print("  GET  /messages - Get all messages from all agents")
    print("  GET  /messages/{agent_name} - Get messages from specific agent")
    print("  POST /analyze - Submit email for analysis")
    print("="*60 + "\n")

    uvicorn.run(app, host="0.0.0.0", port=6000)
