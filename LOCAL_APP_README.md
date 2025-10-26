# Email Analysis System - Local Web Application

A real-time, multi-agent email analysis system with live agent communication visualization.

## Features

✨ **3-Agent Pipeline Architecture**
- **Analyzer Agent**: Performs 7 comprehensive analyses (context, relationships, culture, recipient simulation, sender advocacy, devil's advocate, mediation)
- **Evaluator Agent**: Evaluates tone, goal alignment, and risk assessment
- **Output Agent**: Generates actionable feedback and 3-tier email rewrites (Conservative, Recommended, Bold)

🔴 **Real-Time Communication**
- WebSocket-based live updates
- Watch agents communicate with each other in real-time
- See status updates, processing steps, and results as they happen

🎨 **Beautiful UI**
- Modern, responsive web interface
- Agent status visualization
- Live message log showing inter-agent communication
- Example emails to get started quickly

## Installation

1. **Install Dependencies**
```bash
pip install flask flask-socketio openai python-socketio
```

Or install from requirements.txt:
```bash
pip install -r requirements.txt
```

2. **Verify API Key**
The app uses ASI-1 API. The API key is already configured in `app.py`, but you can update it if needed:
```python
api_key='YOUR_API_KEY_HERE'
```

## Running the Application

### Option 1: Direct Python
```bash
python app.py
```

### Option 2: Using the start script
```bash
python start_local_app.py
```

The application will start on:
```
http://localhost:5000
```

## Usage

1. **Open your browser** to `http://localhost:5000`

2. **Enter email details**:
   - From (Sender): e.g., "John Smith (Manager)"
   - To (Recipient): e.g., "Jane Doe (Team Member)"
   - Email Content: The actual email text

3. **Click "Analyze Email"** or use one of the example emails

4. **Watch the magic happen**:
   - The **Analyzer** agent lights up and performs 7 analyses
   - Results are sent to the **Evaluator** agent
   - The **Evaluator** performs 3 evaluations and calculates a risk score
   - Results are sent to the **Output** agent
   - The **Output** agent generates feedback and rewrites
   - Final results appear with score, feedback, and 3 rewritten versions

5. **View Results**:
   - Overall score (0-10)
   - Detailed feedback with strengths, issues, and action items
   - Three rewritten versions: Conservative, Recommended, and Bold

## Agent Communication Pipeline

```
User Input
    ↓
┌─────────────┐
│  Analyzer   │  → Performs 7 analyses
└─────────────┘
    ↓ AnalysisResult
┌─────────────┐
│  Evaluator  │  → Evaluates tone, goals, risks
└─────────────┘
    ↓ EvaluationResult
┌─────────────┐
│   Output    │  → Generates feedback & rewrites
└─────────────┘
    ↓ FinalOutput
User sees results
```

## Features in Detail

### Analyzer Agent
- **Context Analysis**: Intent, tone, urgency, action items
- **Relationship Mapping**: Power dynamics, formality, trust
- **Culture Detection**: Communication styles, cultural sensitivities
- **Recipient Simulation**: How recipient would interpret/react
- **Sender Advocacy**: Defending sender's intentions
- **Devil's Advocate**: Identifying risks and problems
- **Mediation**: Synthesizing all perspectives

### Evaluator Agent
- **Tone Validation**: Appropriateness, professionalism
- **Goal Alignment**: Success probability, clarity
- **Risk Assessment**: Disaster scenarios, send/don't-send recommendation
- **Overall Scoring**: 0-10 scale with detailed explanation

### Output Agent
- **Feedback Synthesis**: Executive summary, strengths, issues, action items
- **Email Rewrites**:
  - Conservative: Minimal changes
  - Recommended: Balanced improvements
  - Bold: Major revisions

## Real-Time Features

The application uses WebSockets to show:
- Which agent is currently active (highlighted with animation)
- Status messages from each agent
- Processing steps in real-time
- Inter-agent communication ("Analyzer → Evaluator", etc.)
- Error handling and recovery

## Example Emails

The app includes 3 pre-loaded examples:
1. **Urgent Request**: Manager demanding immediate report
2. **Feedback Email**: Team lead providing code review feedback
3. **Meeting Request**: Marketing director requesting CEO meeting

## Troubleshooting

**Port already in use?**
Change the port in `app.py`:
```python
socketio.run(app, debug=True, host='0.0.0.0', port=5001)
```

**WebSocket not connecting?**
- Check firewall settings
- Try accessing via `http://localhost:5000` instead of `http://127.0.0.1:5000`

**API errors?**
- Verify your ASI-1 API key is valid
- Check internet connection
- Look at console logs for detailed error messages

## Architecture

- **Backend**: Flask + Flask-SocketIO
- **Frontend**: HTML/CSS/JavaScript with Socket.IO client
- **AI Model**: ASI-1 Mini (via OpenAI-compatible API)
- **Communication**: WebSocket for real-time bidirectional updates

## Development

To modify the agents:
- Edit the `run_analyzer()`, `run_evaluator()`, or `run_output()` functions in `app.py`
- Use `emit_agent_message()` to send updates to the frontend
- The pipeline runs in a background thread to keep the UI responsive

## Credits

Built with:
- Flask
- Flask-SocketIO
- OpenAI API (ASI-1)
- Socket.IO
- Lots of ☕ and 🎵
