# Email Analysis Web Application

A React + Flask application with multi-agent email analysis system. Watch as the Analyzer and Evaluator agents converse in real-time to evaluate your emails!

## Project Structure

```
.
├── backend/
│   ├── app.py                  # Flask API server
│   └── requirements.txt        # Python dependencies
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── EmailInput.jsx          # Email submission form
│   │   │   ├── EmailInput.css
│   │   │   ├── ConversationDisplay.jsx # Agent conversation viewer
│   │   │   └── ConversationDisplay.css
│   │   ├── App.js              # Main app component
│   │   ├── App.css
│   │   ├── index.js
│   │   └── index.css
│   └── package.json            # Node dependencies
└── agents/
    ├── analyzer.py             # Analyzer agent
    ├── evaluator.py            # Evaluator agent
    └── output.py               # Output agent
```

## Features

- 🔍 **Real-time Agent Conversation** - Watch Analyzer and Evaluator discuss your email
- 📊 **Multi-Agent Analysis** - Context, relationships, tone, risks all analyzed
- 🎨 **Beautiful UI** - Modern React interface with live updates
- 🚀 **Local Agents** - No cloud deployment needed, runs 100% locally
- 💬 **Dialogue System** - Agents ask each other questions for deeper analysis

## Setup Instructions

### Prerequisites

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 16+** - [Download Node.js](https://nodejs.org/)

### Backend Setup (Flask + Agents)

1. **Create and activate virtual environment:**

```bash
# Navigate to project root
cd /Users/addisonchen/Documents/workspace/customOrchestratedAgenticEmailEvals

# Create virtual environment (if not already created)
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

2. **Install backend dependencies:**

```bash
cd backend
pip install -r requirements.txt
```

3. **Start the Flask API:**

```bash
python app.py
```

The Flask API will start on `http://localhost:5000`

4. **In separate terminals, start each agent:**

Terminal 2:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
python agents/analyzer.py
```

Terminal 3:
```bash
source venv/bin/activate
python agents/evaluator.py
```

Terminal 4:
```bash
source venv/bin/activate
python agents/output.py
```

### Frontend Setup (React)

1. **Navigate to frontend directory:**

```bash
cd frontend
```

2. **Install dependencies:**

```bash
npm install
```

3. **Start the React development server:**

```bash
npm start
```

The React app will open automatically at `http://localhost:3000`

## Usage

1. **Start all services** (see setup instructions above):
   - 3 Agent processes (analyzer, evaluator, output)
   - 1 Flask backend
   - 1 React frontend

2. **Open the web app** at `http://localhost:3000`

3. **Check agent status** - The status bar shows if all agents are online (green = online, red = offline)

4. **Submit an email for analysis:**
   - Fill in sender info (e.g., "Manager", "Senior Developer")
   - Fill in recipient info (e.g., "Team", "Junior Developer")
   - Enter the email content
   - Click "Analyze Email"

5. **Watch the conversation** - The right panel will show the real-time dialogue between agents:
   - 🔍 **Analyzer** performs initial analysis
   - ⚖️ **Evaluator** asks questions and evaluates
   - 📤 **Output** generates final recommendations

## API Endpoints

The Flask backend provides these endpoints:

- `GET /` - API info
- `GET /api/health` - Health check
- `GET /api/test/<agent_name>` - Test agent connectivity
- `POST /api/analyze` - Submit email for analysis
- `GET /api/messages` - Get all agent messages
- `GET /api/messages/<agent_name>` - Get messages from specific agent

## Agent Communication Flow

1. **User submits email** → Flask API → **Analyzer Agent**
2. **Analyzer** performs 7-step analysis and sends to **Evaluator**
3. **Evaluator** reviews and may ask **Analyzer** questions (dialogue rounds)
4. **Evaluator** sends evaluation to **Output Agent**
5. **Output** generates final recommendations and feedback
6. **React UI** polls for messages and displays the conversation

## Troubleshooting

### Agents show as offline

- Make sure all 3 agents are running in separate terminals
- Check that ports 8001, 8002, 8003 are not in use
- Restart the agents if needed

### "No messages yet"

- Ensure Flask backend is running on port 5000
- Check browser console for errors
- Verify agents are responding: `curl http://localhost:5000/api/test/analyzer`

### CORS errors

- Make sure Flask is running with CORS enabled
- The frontend `package.json` includes proxy configuration

### Port conflicts

If ports are in use, you can change them:
- Agents: Edit `port=` in each agent file
- Flask: Change `port=5000` in `backend/app.py`
- React: Set `PORT=3001 npm start`

## Development

### Adding new agent types

1. Create agent in `agents/` directory
2. Add query handlers with `@agent.on_query()`
3. Add agent address to `backend/app.py` AGENT_MAP
4. Update UI to display new agent messages

### Customizing the UI

- Edit `frontend/src/App.css` for global styles
- Edit component CSS files for specific components
- Modify colors in `ConversationDisplay.css` `getAgentColor()`

## Technologies Used

- **Backend**: Flask, uAgents, httpx
- **Frontend**: React 18, CSS3
- **AI**: ASI-1 API (OpenAI compatible)
- **Agents**: Fetch.ai uAgents framework

## Next Steps

- Add more agents (tone validator, risk assessor, etc.)
- Implement email rewriting suggestions
- Add export/save functionality
- Create user authentication
- Deploy to production

---

**Enjoy analyzing your emails with AI agents! 🚀**
