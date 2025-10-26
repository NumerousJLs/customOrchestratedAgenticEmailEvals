# Email Analysis Multi-Agent System

Clean, production-ready agents for email analysis with multi-round dialogue. Ready for Agentverse deployment.

## 🎯 Agents

### 1. Analyzer Agent (`agents/analyzer.py`)
**Purpose**: Analyzes emails from multiple perspectives

**Features**:
- Context & intent analysis
- Relationship dynamics detection
- Cultural context awareness
- Recipient reaction simulation
- Sender intent advocacy
- Risk identification (Devil's Advocate)
- Multi-round dialogue support
- **Chat Protocol** - Interactive chat support using `uagents_core.contrib.protocols.chat`
  - Handles ChatMessage with StartSessionContent, TextContent, EndSessionContent
  - Sends ChatAcknowledgement for each message
  - LLM-powered chat responses for email analysis questions
  - All chat interactions logged to message storage
- **Query API** for message retrieval (local testing with proxy)
- Message storage in `ctx.storage` for query access

**Seed**: `analyzer_email_seed_2024`
**Port**: 8001 (for local query testing)
**Query Endpoint**: `@on_query(model=GetMessagesRequest, replies={MessagesResponse})`
**Chat Protocol**: `@chat_proto.on_message(ChatMessage)` with session support

### 2. Evaluator Agent (`agents/evaluator.py`)
**Purpose**: Evaluates analysis quality through dialogue, then scores the email

**Features**:
- **3-round dialogue** with Analyzer
- Asks critical questions about the analysis
- Tone appropriateness evaluation
- Goal alignment assessment
- Risk scoring
- Overall quality score (0-10)
- **Query API** for message retrieval
- Message storage in `ctx.storage` for query access

**Seed**: `evaluator_email_seed_2024`
**Port**: 8002 (for local query testing)
**Query Endpoint**: `@on_query(model=GetMessagesRequest, replies={MessagesResponse})`

### 3. Output Agent (`agents/output.py`)
**Purpose**: Generates actionable feedback and email rewrites

**Features**:
- Synthesizes all evaluations into feedback
- Creates 3 rewrite versions:
  - Conservative (minimal changes)
  - Recommended (balanced)
  - Bold (major revisions)
- **Query API** for message retrieval
- Message storage in `ctx.storage` for query access

**Seed**: `output_email_seed_2024`
**Port**: 8003 (for local query testing)
**Query Endpoint**: `@on_query(model=GetMessagesRequest, replies={MessagesResponse})`

## 🔄 Message Flow

```
EmailInput
    ↓
Analyzer (analyzes email)
    ↓
    AnalysisResult
    ↓
Evaluator (starts dialogue)
    ↓
DialogueQuestion (Round 1)
    ↓
Analyzer (responds)
    ↓
DialogueResponse (Round 1)
    ↓
DialogueQuestion (Round 2)
    ↓
... (3 rounds total)
    ↓
Evaluator (evaluates after dialogue)
    ↓
EvaluationResult
    ↓
Output (generates feedback & rewrites)
    ↓
FinalOutput
```

## 📦 Models

### EmailInput
```python
email_text: str
sender_info: str
recipient_info: str
original_chat_sender: str
```

### AnalysisResult
```python
context_analysis: str
relationship_analysis: str
culture_analysis: str
recipient_simulation: str
sender_advocacy: str
devils_advocate: str
mediation_synthesis: str
email_text: str
sender_info: str
recipient_info: str
original_chat_sender: str
```

### DialogueQuestion
```python
round_number: int
question: str
context: str
original_chat_sender: str
```

### DialogueResponse
```python
round_number: int
response: str
original_chat_sender: str
```

### EvaluationResult
```python
analysis_summary: str
tone_evaluation: str
goal_alignment: str
risk_assessment: str
overall_score: float
send_recommendation: str
email_text: str
sender_info: str
recipient_info: str
original_chat_sender: str
```

### FinalOutput
```python
feedback: str
rewritten_email: str
overall_score: float
original_chat_sender: str
```

## 🚀 Deployment to Agentverse

### Step 1: Get Agent Addresses

Run each agent locally to get their addresses:

```bash
# Terminal 1
python agents/analyzer.py

# Terminal 2
python agents/evaluator.py

# Terminal 3
python agents/output.py
```

Copy the addresses shown in the startup messages.

### Step 2: Update Agent Addresses

Edit each agent file to set the correct addresses:

**`agents/analyzer.py`** (line ~57):
```python
ctx.storage.set("evaluator_address", "YOUR_EVALUATOR_ADDRESS_HERE")
```

**`agents/evaluator.py`** (line ~70):
```python
ctx.storage.set("output_address", "YOUR_OUTPUT_ADDRESS_HERE")
```

### Step 3: Deploy to Agentverse

1. Go to [https://agentverse.ai](https://agentverse.ai)
2. Create three new agents
3. Copy the code from each agent file
4. Paste into the respective Agentverse agent editor
5. Save and deploy

### Step 4: Test the System

Send an `EmailInput` message to the Analyzer agent:

```python
{
  "email_text": "Hi team, I need this done by EOD.",
  "sender_info": "Manager",
  "recipient_info": "Team"
}
```

Watch the agents communicate through 3 dialogue rounds, then produce a final evaluation!

## 🔑 Key Features

✅ **No REST API Dependencies** - Pure uAgents messaging
✅ **Multi-Round Dialogue** - 3 rounds of Q&A between Analyzer & Evaluator
✅ **State Management** - Uses `ctx.storage` to persist dialogue state
✅ **Clean Code** - No unnecessary dependencies or complexity
✅ **Production Ready** - Works on Agentverse without modification (after setting addresses)
✅ **ASI-1 LLM** - Powered by api.asi1.ai for all analysis

## 📝 API Key

The agents use ASI-1 API. The key is already included in the code:
```python
base_url='https://api.asi1.ai/v1'
api_key='sk_a77e3af6ceb240939b2c03ce2d30a9f750fb81f4266d44d192d3a4af763f7b8c'
```

## 🧪 Local Testing with Query Proxy

For local development and testing, use the **query proxy pattern**:

### Start Agents Locally

```bash
# Option 1: Start all agents with one script
python start_all_agents.py

# Option 2: Start agents individually in separate terminals
# Terminal 1
python agents/analyzer.py

# Terminal 2
python agents/evaluator.py

# Terminal 3
python agents/output.py
```

### Start the FastAPI Proxy

In a separate terminal:

```bash
python proxy.py
```

This starts a FastAPI server on `http://localhost:5000` that can:
- Query all agents for their messages
- Submit emails for analysis
- Track the entire processing flow

### Test the System

```bash
python test_query_proxy.py
```

### Proxy API Endpoints

- `GET /` - Proxy status and agent info
- `GET /messages` - Get all messages from all agents
- `GET /messages/{agent_name}` - Get messages from specific agent (analyzer, evaluator, output)
- `POST /analyze` - Submit an email for analysis

### Example: Submit an Email

```bash
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "email_text": "Hi team, I need this done by EOD.",
    "sender_info": "Manager",
    "recipient_info": "Team"
  }'
```

### Example: Get All Messages

```bash
curl http://localhost:5000/messages
```

## 💬 Using the Chat Protocol

The Analyzer agent now supports interactive chat using the standard uAgents chat protocol!

### Chat Message Types

1. **StartSessionContent** - Start a new chat session
2. **TextContent** - Send text messages
3. **EndSessionContent** - End the current session

### Example: Sending a Chat Message

```python
from datetime import datetime
from uuid import uuid4
from uagents_core.contrib.protocols.chat import (
    ChatMessage,
    StartSessionContent,
    TextContent,
    EndSessionContent,
)

# Helper function
def create_text_chat(text: str, end_session: bool = False) -> ChatMessage:
    content = [TextContent(type="text", text=text)]
    if end_session:
        content.append(EndSessionContent(type="end-session"))
    return ChatMessage(timestamp=datetime.utcnow(), msg_id=uuid4(), content=content)

# Start a session
start_msg = ChatMessage(
    timestamp=datetime.utcnow(),
    msg_id=uuid4(),
    content=[
        StartSessionContent(type="start-session"),
        TextContent(type="text", text="Hello! Can you help me analyze an email?")
    ]
)

# Send a text message
text_msg = create_text_chat("How should I handle urgent email requests?", end_session=False)

# End a session
end_msg = create_text_chat("Thanks for your help!", end_session=True)
```

### Chat Integration with Message Storage

All chat interactions are automatically logged to the message storage system:
- `chat_received` - When a chat message is received
- `chat_session` - When a session starts or ends
- `chat_processing` - When processing a chat message
- `chat_sent` - When a response is sent
- `chat_error` - If an error occurs

You can retrieve all chat history via the query API!

## 🎓 Learning Resources

- [uAgents Documentation](https://docs.fetch.ai/uagents/)
- [uAgents Query Pattern](https://docs.fetch.ai/guides/agents/query-requests/)
- [uAgents Chat Protocol](https://docs.fetch.ai/guides/agents/protocols/)
- [Agentverse Guide](https://docs.fetch.ai/guides/agentverse/)
- [ASI-1 API](https://api.asi1.ai/docs)

## 🤝 Contributing

Feel free to extend these agents with:
- Additional analysis perspectives
- More dialogue rounds
- Different LLM models
- Custom evaluation criteria
- Enhanced query endpoints
- Additional chat protocol features

Happy agent building! 🚀
