# Email Evaluation Agent System

An intelligent email evaluation system built with Fetch.ai's uAgents framework. Test how your emails will be received by different personality types and get expert coaching feedback to improve your communication.

## Overview

This project uses AI agents to simulate email recipients with different personalities and provides professional coaching feedback on how to improve your emails. The system helps you:

- **Test emails** against different personality types (angry CEO, chill coworker, stern professor, etc.)
- **Get realistic responses** showing how each personality would react
- **Receive expert coaching** on improving your email's effectiveness
- **Customize personalities** with moods, contexts, and traits
- **Deploy to Fetch.ai's agent network** for decentralized operation

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Orchestrator (Local)                      │
│          Coordinates workflow and user interaction           │
└──────────────┬──────────────────────────────┬───────────────┘
               │                              │
               ▼                              ▼
     ┌─────────────────┐            ┌─────────────────┐
     │  Persona Agent  │            │   Coach Agent   │
     │   (Port 8001)   │            │   (Port 8002)   │
     │                 │            │                 │
     │ • Simulates     │            │ • Analyzes      │
     │   personalities │            │   emails        │
     │ • Generates     │            │ • Provides      │
     │   responses     │            │   feedback      │
     │ • Uses OpenAI   │            │ • Uses OpenAI   │
     └─────────────────┘            └─────────────────┘
```

## Features

### Built-in Personality Types

1. **Angry CEO** - Busy executive with no patience for poorly written emails
2. **Chill Coworker** - Laid-back colleague who values work-life balance
3. **Stern Professor** - Academic who expects precision and rigor
4. **Supportive Mentor** - Helpful guide focused on growth
5. **Anxious Client** - Worried about deadlines and outcomes
6. **Skeptical Investor** - Data-driven and scrutinizing

### Key Capabilities

- **Beautiful Web UI**: Modern Streamlit interface with real-time feedback
- **Batch Comparison**: Test emails against multiple personalities simultaneously
- **Dynamic Personality Management**: Create custom personalities on the fly
- **Mood & Context Updates**: Modify personality states without creating new agents
- **Comprehensive Feedback**: Get both persona reactions and expert coaching
- **Interactive CLI**: User-friendly command-line interface
- **Programmatic API**: Use as a library in your own applications
- **Fetch.ai Network Ready**: Deploy agents to the decentralized network

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- OpenAI API key (optional - can run in demo mode without it)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd customOrchestratedAgenticEmailEvals
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

   **Don't have an API key?** No problem! The system automatically runs in demo mode with sample responses.

## Demo Mode vs Real Mode

The system automatically detects if you have a valid OpenAI API key:

### 🎭 Demo Mode (No API Key Needed)
- Uses pre-generated sample responses
- Perfect for testing the UI and workflow
- No API costs
- No signup required
- Great for understanding how the system works

**To use demo mode:**
- Don't set `OPENAI_API_KEY` in `.env`, OR
- Set `DEMO_MODE=true` in `.env`

### 🤖 Real Mode (Requires OpenAI API Key)
- Uses actual AI analysis via OpenAI
- Personalized responses for your emails
- Requires OpenAI account with credits
- More accurate and contextual feedback

**To use real mode:**
1. Sign up at [OpenAI Platform](https://platform.openai.com/)
2. Add payment method and credits ($5-10 is plenty to start)
3. Create an API key
4. Add to `.env`: `OPENAI_API_KEY=sk-...`

**Note:** If you see a quota error, visit [OpenAI Billing](https://platform.openai.com/account/billing) to add credits.

## Usage

### Running the System

The system works directly with OpenAI - no need to start separate agents!

You have three options to use the system:

**Option A: Web UI (Recommended)**

Start the web interface:

```bash
# macOS/Linux
./start_web.sh

# Windows
start_web.bat

# Or directly with streamlit
streamlit run web/app.py
```

Open your browser to `http://localhost:8501` and enjoy the beautiful interface!

No need to start agents separately - the web UI handles everything!

**Option B: Interactive CLI**

In a separate terminal:

```bash
python src/cli.py
```

Follow the interactive prompts to evaluate emails.

**Option C: Run Examples**

```bash
# Basic usage examples
python examples/basic_usage.py

# Custom personality examples
python examples/custom_personality.py
```

**Option D: Programmatic Usage**

Create your own Python script:

```python
import asyncio
from src.orchestrator import EmailEvaluationOrchestrator

async def main():
    orchestrator = EmailEvaluationOrchestrator()

    result = await orchestrator.evaluate_email(
        draft_email="Your email text here",
        personality_type="angry_ceo",
        sender_name="Your Name"
    )

    orchestrator.print_detailed_feedback(result)

asyncio.run(main())
```

## Example Output

```
==============================================================
EVALUATION RESULTS
==============================================================

📧 PERSONA RESPONSE (angry_ceo)
────────────────────────────────────────────────────────────
Emotional Tone: frustrated

Response:
John - I don't have time to "touch base." What challenges?
What's the new deadline? Give me specifics, not vague updates.

Key Concerns:
  • Lack of specific details
  • No clear action items
  • Vague language about challenges
  • Missing concrete timeline


🎓 COACH FEEDBACK
────────────────────────────────────────────────────────────

Overall Assessment:
The email is too vague and informal for an executive audience...

✅ Strengths:
  • Polite tone
  • Acknowledges there's an issue

⚠️  Areas for Improvement:
  • Lacks specific details about challenges
  • No proposed new deadline
  • No action items or next steps
  • Too casual for executive communication

🎯 Persona Alignment:
This email would frustrate an executive who values efficiency...

💡 Improvement Suggestions:
  1. Lead with the specific issue and proposed solution
  2. Provide concrete data and a new deadline
  3. Include clear action items
  4. Use more direct, professional language

📝 Suggested Revision:
Subject: Project Timeline Adjustment Required

[Improved email text...]
```

## Project Structure

```
customOrchestratedAgenticEmailEvals/
├── src/
│   ├── agents/
│   │   ├── persona_agent.py    # Personality simulation agent
│   │   └── coach_agent.py      # Coaching feedback agent
│   ├── models/
│   │   └── messages.py         # Message models for agent communication
│   ├── utils/
│   │   └── config.py           # Configuration and personality templates
│   ├── orchestrator.py         # Main orchestration logic
│   ├── main.py                 # Agent startup script
│   └── cli.py                  # Interactive command-line interface
├── web/
│   ├── app.py                  # Main Streamlit application
│   └── pages/
│       ├── evaluation.py       # Single email evaluation page
│       └── comparison.py       # Batch comparison page
├── examples/
│   ├── basic_usage.py          # Basic usage examples
│   └── custom_personality.py   # Custom personality examples
├── start_web.sh               # Web UI launcher (macOS/Linux)
├── start_web.bat              # Web UI launcher (Windows)
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
└── README.md                  # This file
```

## Advanced Usage

### Creating Custom Personalities

```python
result = await orchestrator.evaluate_email(
    draft_email=your_email,
    personality_type="picky_designer",
    personality_description="""
    You are a meticulous designer who cares deeply about aesthetics,
    user experience, and attention to detail. You get frustrated by
    vague feedback and appreciate specificity.
    """,
    sender_name="Project Manager"
)
```

### Updating Personality States

```python
await orchestrator.update_personality(
    personality_type="angry_ceo",
    mood="extremely stressed after board meeting",
    context="Company is behind on quarterly goals"
)
```

### Batch Testing

```python
personalities = ["angry_ceo", "chill_coworker", "stern_professor"]
results = []

for personality in personalities:
    result = await orchestrator.evaluate_email(
        draft_email=email_draft,
        personality_type=personality
    )
    results.append(result)
```

## Deployment to Fetch.ai Network

The agents are designed to run locally but can be deployed to Fetch.ai's agent network for decentralized operation.

### Prerequisites for Network Deployment

1. **Fetch.ai wallet** with FET tokens
2. **Agent seeds** (secure random phrases)
3. **Public endpoints** (for production deployment)

### Deployment Steps

1. **Update agent initialization** with unique seeds:
   ```python
   persona_agent = PersonaAgent(seed="your_secure_seed_phrase_1")
   coach_agent = CoachAgent(seed="your_secure_seed_phrase_2")
   ```

2. **Configure public endpoints** in `.env`:
   ```
   PERSONA_ENDPOINT=https://your-domain.com:8001/submit
   COACH_ENDPOINT=https://your-domain.com:8002/submit
   ```

3. **Run agents** - they will automatically register on the Fetch.ai Almanac

4. **Update orchestrator** to use network addresses instead of localhost

For detailed deployment instructions, see [Fetch.ai Documentation](https://docs.fetch.ai/uAgents/).

## Configuration

### Environment Variables

- `OPENAI_API_KEY` - Your OpenAI API key (required)
- `AGENT_HOST` - Host for local agents (default: localhost)
- `PERSONA_AGENT_PORT` - Port for persona agent (default: 8001)
- `COACH_AGENT_PORT` - Port for coach agent (default: 8002)

### Customizing OpenAI Model

The system uses `gpt-4o-mini` by default (fast and cost-effective). To change the model, edit `src/orchestrator_simple.py`:

```python
completion = self.client.chat.completions.create(
    model="gpt-4o-mini",  # Options: gpt-4o-mini, gpt-4o, gpt-3.5-turbo
    messages=[...],
    temperature=0.8
)
```

**Available Models:**
- `gpt-4o-mini` - Fast, cost-effective, widely available (default)
- `gpt-4o` - More capable, higher quality, more expensive
- `gpt-3.5-turbo` - Fastest, cheapest, good for testing

Change in two places in `orchestrator_simple.py`:
- Line ~132: Persona response generation
- Line ~197: Coach feedback generation

## Troubleshooting

### Common Issues

**"You exceeded your current quota" (Error 429)**
- Your OpenAI account is out of credits
- **Quick fix:** System automatically switches to demo mode when this happens
- **To use real AI:** Add credits at [OpenAI Billing](https://platform.openai.com/account/billing)
- Demo mode works perfectly for testing - no credits needed!

**"Model gpt-4 does not exist or you do not have access to it"**
- The system now uses `gpt-4o-mini` by default (already fixed!)
- If you still see this error, check that you have access to GPT-4o-mini
- Alternative: Change model to `gpt-3.5-turbo` in `src/orchestrator_simple.py`

**"OpenAI API error"**
- Verify your API key is set in `.env`
- Check your OpenAI account has credits
- Ensure you have access to the model being used
- Try using `gpt-3.5-turbo` if other models fail
- Or just use demo mode - works great!

**"Import errors"**
- Run `pip install -r requirements.txt`
- Ensure you're in the project root directory
- Check Python version (3.8+ required)
- Activate your virtual environment: `source venv/bin/activate`

**"Streamlit command not found"**
- Install streamlit: `pip install streamlit`
- Make sure your virtual environment is activated
- Try running directly: `python -m streamlit run web/app.py`

## Contributing

Contributions are welcome! Areas for improvement:

- Additional personality types
- Support for other LLM providers
- Web interface
- Email template library
- Multi-language support
- Performance optimizations

## License

[Your license here]

## Acknowledgments

Built with:
- [Fetch.ai uAgents Framework](https://github.com/fetchai/uAgents)
- [OpenAI API](https://openai.com/)
- Python ecosystem

## Support

For issues and questions:
- Open an issue on GitHub
- Check [Fetch.ai Documentation](https://docs.fetch.ai/)
- Review example scripts in `examples/`
