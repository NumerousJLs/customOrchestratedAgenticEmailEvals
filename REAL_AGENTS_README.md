# Email Analysis System - Real uAgents Implementation

This version uses **actual uAgents** that communicate with each other via the uAgents framework, with a Flask frontend that polls their REST endpoints for live updates.

## 🏗️ Architecture

```
User (Browser)
    ↓
Flask App (port 5001)
    ↓ [HTTP POST EmailInput]
Analyzer Agent (port 8201)
    ↓ [uAgent message: AnalysisResult]
Evaluator Agent (port 8202)
    ↓ [uAgent message: EvaluationResult]
Output Agent (port 8203)
    ↓
Flask polls REST endpoints → User sees results
```

## ✨ Key Features

- **Real uAgent Communication**: Agents actually send messages to each other
- **Message Storage**: Each agent stores its messages in `ctx.storage`
- **REST API Polling**: Flask polls agents for new messages every 500ms
- **Independent Processes**: Each agent runs in its own process
- **Live Updates**: Frontend receives updates in real-time via WebSocket

## 📦 Components

### 1. **Three uAgents**
- `analyzer_with_rest.py` - Analyzes email context, relationships, culture (port 8201)
- `evaluator_with_rest.py` - Evaluates tone, goals, risks (port 8202)
- `output_with_rest.py` - Generates feedback and rewrites (port 8203)

### 2. **Launcher Script**
- `start_agents.py` - Starts all three agents in separate processes

### 3. **Flask Coordinator**
- `app_real_agents.py` - Polls agents and displays updates to frontend

## 🚀 Quick Start

### Step 1: Start the Agents

```bash
# Terminal 1: Start all agents
python start_agents.py
```

You should see:
```
✅ Started Analyzer Agent (port 8201)
✅ Started Evaluator Agent (port 8202)
✅ Started Output Agent (port 8203)
✅ ALL AGENTS RUNNING!
```

### Step 2: Start Flask App

```bash
# Terminal 2: Start Flask
python app_real_agents.py
```

### Step 3: Open Browser

Navigate to: **http://localhost:5001**

## 🔍 How It Works

### Agent Communication Flow

1. **User submits email** via Flask web interface
2. **Flask sends HTTP POST** to Analyzer agent's `/submit` endpoint
3. **Analyzer processes** the email and stores messages in `ctx.storage`
4. **Analyzer sends uAgent message** to Evaluator (real agent-to-agent communication!)
5. **Evaluator receives message**, processes, stores its messages
6. **Evaluator sends uAgent message** to Output agent
7. **Output generates** feedback and rewrites, stores in `ctx.storage`
8. **Flask polls** all agents' REST endpoints every 500ms
9. **Flask forwards** new messages to browser via WebSocket
10. **User sees** live updates as agents communicate

### REST Endpoints

Each agent exposes:
- `GET /messages` - Returns new messages since last poll
- `GET /results` - (Output agent only) Returns final results

### Message Storage

Agents use `ctx.storage` to store:
```python
messages = [
    {
        "timestamp": 1234567890.123,
        "agent": "Analyzer",
        "type": "processing",
        "content": "Analyzing email context...",
        "recipient": "Evaluator"
    },
    ...
]
```

## 🛠️ Development

### Agent Addresses

Each agent has a unique address generated from its seed:
- **Analyzer**: `agent1qfz6h76gu27qcxjc69suw2n7v6nkuxvzj3vdv0z4jx0t7kgfhmwv7njaqgz`
- **Evaluator**: `agent1qw4m67px6nqk0zjmqgv23hux0phn5cukjj8ewt5qlmcvhwmaxxx8v2r3m85`
- **Output**: `agent1q2ajv39re0r3ttvjg6j4pq8nfu56kh6aqkquzlgplv25xzaf9g8xc5rrvaj`

### Testing Agents Individually

You can test each agent's REST API:

```bash
# Get messages from Analyzer
curl http://localhost:8201/messages

# Get messages from Evaluator
curl http://localhost:8202/messages

# Get results from Output
curl http://localhost:8203/results
```

### Sending Test Messages

Send a test email to the Analyzer:

```bash
curl -X POST http://localhost:8201/submit \
  -H "Content-Type: application/json" \
  -d '{
    "type": "EmailInput",
    "data": {
      "email_text": "Hi, can we meet tomorrow?",
      "sender_info": "John",
      "recipient_info": "Jane"
    }
  }'
```

## 🐛 Troubleshooting

### Port Already in Use

If you get "Address already in use":
```bash
# Kill processes on ports 8201-8203
lsof -ti:8201,8202,8203 | xargs kill
```

### Agents Not Communicating

1. Check all agents are running:
```bash
lsof -i :8201,8202,8203
```

2. Check agent logs in Terminal 1

3. Verify agent addresses match in each agent's code

### Flask Not Receiving Updates

1. Ensure agents are started BEFORE Flask
2. Check Flask is polling (should see GET requests in agent logs)
3. Verify WebSocket connection in browser console

## 📊 Monitoring

### Agent Logs
- Each agent logs to stdout in Terminal 1
- Look for message sends: `Sent analysis to evaluator`
- Look for message receives: `Received analysis from...`

### Flask Logs
- Flask logs polling activity
- Watch for `agent_message` WebSocket emits

### Browser Console
- Open browser DevTools → Console
- Watch for WebSocket messages
- Look for `agent_message` events

## 🎯 Advantages Over Simulated Version

1. **Truly Multi-Agent**: Real independent processes
2. **Real Communication**: Actual uAgent messages, not simulated
3. **Scalable**: Could deploy agents to different machines
4. **Testable**: Can test agents independently
5. **Educational**: Learn real uAgents framework

## 🔄 Stopping Everything

### Stop Agents
In Terminal 1, press `Ctrl+C`

### Stop Flask
In Terminal 2, press `Ctrl+C`

## 📝 Next Steps

- Add more dialogue between agents
- Implement agent discovery
- Add authentication
- Deploy agents to different servers
- Add monitoring/metrics
- Implement retry logic
- Add rate limiting

## 🆚 Comparison with Simulated Version

| Feature | Simulated (`app.py`) | Real Agents (`app_real_agents.py`) |
|---------|---------------------|-----------------------------------|
| Agent Communication | Simulated (function calls) | Real (uAgents messages) |
| Processes | Single process | Multiple processes |
| Setup Complexity | Low | Medium |
| Scalability | Limited | High |
| Testing | Easier | More complex |
| Learning Value | Basic | Advanced |

## 📚 Learn More

- [uAgents Documentation](https://docs.fetch.ai/uagents/)
- [uAgents GitHub](https://github.com/fetchai/uAgents)
- [Flask-SocketIO Documentation](https://flask-socketio.readthedocs.io/)
