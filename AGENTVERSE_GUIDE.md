# Agentverse Integration Guide

**Updated:** Based on official Agentverse Chat Protocol documentation

This guide explains how to properly deploy your AgentMail agents to Fetch.ai's Agentverse using the **Chat Protocol**.

---

## 🔧 What Was Fixed

### Critical Issues Resolved

1. **❌ OLD: Incorrect Mailbox Implementation**
   ```python
   # WRONG - This doesn't work
   self.agent._mailbox_client = mailbox_key
   ```

   **✅ NEW: Proper Mailbox API**
   ```python
   # CORRECT - Use the mailbox parameter
   self.agent = Agent(
       name=name,
       seed=seed,
       port=port,
       mailbox=f"{mailbox_key}@https://agentverse.ai"
   )
   ```

2. **❌ OLD: Local-only Communication**
   - Agents used `localhost` endpoints
   - No public URL exposure
   - Could not be reached by Agentverse

   **✅ NEW: Chat Protocol with FastAPI**
   - Public HTTP endpoints (`/status`, `/chat`)
   - Works with cloudflared tunnels
   - Agentverse-ready architecture

3. **❌ OLD: Missing Agentverse Requirements**
   - No `AGENT_SEED_PHRASE` for stable identity
   - No health check endpoints
   - No proper message envelope handling

   **✅ NEW: Full Chat Protocol Support**
   - Seed phrase for consistent agent addresses
   - Health check `/status` endpoint
   - Message handler `/chat` endpoint
   - Envelope-wrapped message handling

---

## 📚 Architecture Overview

### Two Agent Implementations

Your project now has **two types** of agent implementations:

#### 1. **Original uAgents Implementation** (`agents/shared/base_agent.py`)
- Uses `uagents.Agent` with message handlers
- Good for local agent-to-agent communication
- Requires all agents running in same network
- **Fixed:** Now uses proper mailbox API

#### 2. **Chat Protocol Implementation** (`agents/shared/chat_protocol_agent.py`) ⭐ RECOMMENDED
- Uses FastAPI for HTTP endpoints
- Compatible with Agentverse Chat Protocol
- Can be deployed to Agentverse
- Works with public URLs and tunnels
- **New file created based on official docs**

---

## 🚀 Deployment Methods

### Method 1: Local Development + Tunnels (Testing)

**Best for:** Testing before production deployment

#### Requirements
- `cloudflared` installed ([Installation Guide](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/))
- Anthropic API key
- Agent seed phrase

#### Steps

1. **Set up environment**
   ```bash
   cp .env.example .env
   ```

   Edit `.env`:
   ```bash
   ANTHROPIC_API_KEY=your_anthropic_key
   AGENT_SEED_PHRASE=$(openssl rand -base64 32)
   AGENTVERSE_API_KEY=your_agentverse_key  # Optional
   ```

2. **Run deployment helper**
   ```bash
   python deploy_to_agentverse.py
   ```

   Choose option 1 for local + tunnels.

3. **The script will:**
   - Start agents locally
   - Create cloudflared tunnels for each agent
   - Provide registration instructions
   - Give you public URLs

4. **Register on Agentverse**
   - Go to https://agentverse.ai/
   - Navigate to: Agents → "+ Launch an Agent"
   - Select "Chat Protocol"
   - Enter your agent's public URL
   - Follow registration prompts
   - Copy the agent address (starts with `agent1q...`)

5. **Update orchestrator**
   ```bash
   # Edit .env and add:
   AGENT_ENDPOINTS={"context_analyzer":"agent1q...","relationship_mapper":"agent1q..."}
   ```

---

### Method 2: Hosted Agents (Production)

**Best for:** Production deployment, always-on agents

#### Steps

1. **Go to Agentverse**
   - Visit https://agentverse.ai/
   - Log in / Sign up

2. **Create Hosted Agent**
   - Click "Agents" → "+ Launch an Agent"
   - Select "Create an Agentverse hosted Agent"

3. **Prepare your code**

   You need to merge your agent into a single file for Agentverse:

   ```python
   # Example: context_analyzer_hosted.py
   # Include ALL dependencies in one file

   from fastapi import FastAPI, Request
   from anthropic import Anthropic
   import os
   import json

   # Copy ChatProtocolAgent class here
   # Copy ContextAnalyzerChatAgent class here

   # Run the agent
   if __name__ == "__main__":
       agent = ContextAnalyzerChatAgent()
       agent.run()
   ```

4. **Upload to Agentverse**
   - Paste your merged code in the Agentverse editor
   - Set environment variables:
     - `ANTHROPIC_API_KEY`
   - Click "Deploy Agent"

5. **Get agent address**
   - Copy the agent address (e.g., `agent1q...`)
   - Save for orchestrator configuration

6. **Repeat for all 12 agents**

---

### Method 3: uAgents with Mailbox (Advanced)

**Best for:** Complex agent interactions, local control

#### Steps

1. **Create mailbox on Agentverse**
   - Go to https://agentverse.ai/
   - Create a mailbox agent
   - Copy the mailbox key

2. **Update agent initialization**
   ```python
   from agents.shared.base_agent import AgentMailBaseAgent

   agent = ContextAnalyzerAgent(
       port=8101,
       seed="your_seed",
       mailbox_key="your_mailbox_key"  # Now uses correct API!
   )
   ```

3. **Run agents locally**
   ```bash
   python agents/layer1_context/context_analyzer.py
   ```

4. **Agents will register with Agentverse**
   - They maintain local execution
   - But are accessible via Agentverse
   - Can communicate through mailbox

---

## 🧪 Testing Your Deployment

### Test Individual Agent

```bash
# If running locally
curl -X POST http://localhost:8101/status

# Test chat endpoint
curl -X POST http://localhost:8101/chat \
  -H "Content-Type: application/json" \
  -d '{
    "email_text": "Hello, this is a test email.",
    "request_id": "test-123"
  }'
```

### Test with Orchestrator

```python
import asyncio
from agents.orchestrator_agentverse import AgentverseOrchestrator

async def test():
    orchestrator = AgentverseOrchestrator({
        "context_analyzer": "http://localhost:8101",
        # or: "agent1q..." for deployed agents
    })

    result = await orchestrator.analyze_email(
        email_text="Test email",
        mode="professional"
    )

    print(result)
    await orchestrator.close()

asyncio.run(test())
```

---

## 📋 Checklist for Deployment

### Before Deployment
- [ ] Anthropic API key obtained
- [ ] Agentverse account created
- [ ] Agent seed phrase generated
- [ ] `.env` file configured
- [ ] Dependencies installed (`pip install -r requirements.txt`)

### For Local + Tunnel Deployment
- [ ] `cloudflared` installed
- [ ] Agents tested locally
- [ ] Public URLs obtained from tunnels
- [ ] Agents registered on Agentverse
- [ ] Agent addresses copied
- [ ] Orchestrator configured with addresses

### For Hosted Agent Deployment
- [ ] Code merged into single files
- [ ] Code uploaded to Agentverse
- [ ] Environment variables set in Agentverse
- [ ] Agents deployed successfully
- [ ] Agent addresses collected
- [ ] Orchestrator configured

---

## 🔑 Environment Variables Reference

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-...              # Claude API key

# For Agentverse deployment
AGENTVERSE_API_KEY=...                    # Agentverse API key
AGENT_SEED_PHRASE=...                     # Stable agent identity

# Agent endpoints (JSON format)
AGENT_ENDPOINTS={"context_analyzer":"http://localhost:8101"}

# Legacy (optional)
OPENAI_API_KEY=...                        # Old OpenAI support
DEMO_MODE=true                            # Demo mode
```

---

## 🐛 Troubleshooting

### Issue: Agent not responding

**Solution:**
1. Check agent is running: `curl http://localhost:8101/status`
2. Check logs for errors
3. Verify `ANTHROPIC_API_KEY` is set
4. Test Claude API separately

### Issue: Tunnel URL not working

**Solution:**
1. Ensure `cloudflared` is running
2. Check firewall settings
3. Verify agent is listening on correct port
4. Try alternative tunneling service (ngrok)

### Issue: Agentverse registration fails

**Solution:**
1. Verify public URL is accessible from internet
2. Check `/status` endpoint returns OK
3. Ensure `AGENT_SEED_PHRASE` is set
4. Try registration script provided by Agentverse

### Issue: Mailbox not working

**Solution:**
1. Verify mailbox format: `{key}@https://agentverse.ai`
2. Check mailbox key is valid
3. Ensure using new mailbox API (not `._mailbox_client`)
4. Check uagents library version: `pip install --upgrade uagents`

---

## 📖 Additional Resources

- [Agentverse Documentation](https://docs.agentverse.ai/)
- [Chat Protocol Guide](https://docs.agentverse.ai/documentation/launch-agents/connect-your-agents-chat-protocol-integration)
- [uAgents GitHub](https://github.com/fetchai/uAgents)
- [Cloudflared Installation](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/)

---

## 🎯 Quick Start Commands

```bash
# 1. Setup
cp .env.example .env
# Edit .env with your keys

# 2. Install dependencies
pip install -r requirements.txt

# 3. Test single agent locally
python agents/layer1_context/context_analyzer_chat.py

# 4. Deploy with tunnels
python deploy_to_agentverse.py

# 5. Test orchestrator
python agents/orchestrator_agentverse.py
```

---

## ✅ What's Working Now

- ✅ Proper mailbox API usage
- ✅ Chat Protocol implementation with FastAPI
- ✅ Health check endpoints (`/status`)
- ✅ Message handling endpoints (`/chat`)
- ✅ Seed phrase for stable identity
- ✅ Tunnel deployment support
- ✅ Agentverse-compatible orchestrator
- ✅ Environment variable configuration
- ✅ Deployment helper script

---

## 🎓 Understanding the Architecture

### Message Flow

```
User → Orchestrator → Agentverse → Agent /chat endpoint
                                      ↓
                                  Claude API
                                      ↓
                                  Analysis
                                      ↓
User ← Orchestrator ← Agentverse ← Response
```

### Agent Types

1. **Context Extraction** (Layer 1)
   - Analyzes email properties
   - Runs independently in parallel

2. **Simulation** (Layer 2)
   - Debates email effectiveness
   - Sequential with agent interaction

3. **Evaluation** (Layer 3)
   - Scores and validates
   - Parallel execution

4. **Output** (Layer 4)
   - Synthesizes feedback
   - Generates rewrites
   - Sequential processing

---

**Need help?** Check the troubleshooting section or file an issue on GitHub.
