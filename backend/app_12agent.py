"""
12-Agent Email Analysis System
4 Layers with 2 rounds of dialogue between each agent
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from openai import OpenAI
import time
import threading
from typing import List, Dict
import os

# Initialize OpenAI
client = OpenAI(
    base_url='https://api.asi1.ai/v1',
    api_key='sk_a77e3af6ceb240939b2c03ce2d30a9f750fb81f4266d44d192d3a4af763f7b8c',
)

# Initialize Flask
app = Flask(__name__, static_folder='.')
CORS(app)

# In-memory storage for messages
messages_store: List[Dict] = []
analysis_in_progress = False

def add_message(agent: str, msg_type: str, content: str):
    """Add a message to the store"""
    message = {
        "timestamp": time.time(),
        "agent": agent,
        "type": msg_type,
        "content": content
    }
    messages_store.append(message)
    print(f"[{agent}] [{msg_type}] {content[:100]}")
    return message

def agent_dialogue(agent_name: str, system_prompt: str, user_prompt: str, context: str = "") -> str:
    """Have two rounds of internal dialogue for an agent"""
    # First pass
    response1 = client.chat.completions.create(
        model="asi1-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{context}\n\n{user_prompt}"}
        ],
        max_tokens=250,
    )
    first_thought = str(response1.choices[0].message.content)
    add_message(agent_name, "thinking", first_thought)
    time.sleep(0.3)

    # Second pass - refine
    response2 = client.chat.completions.create(
        model="asi1-mini",
        messages=[
            {"role": "system", "content": f"{system_prompt}\n\nNow refine your initial analysis and provide deeper insight."},
            {"role": "user", "content": f"Initial thought: {first_thought}\n\nProvide a refined, more nuanced perspective."}
        ],
        max_tokens=250,
    )
    refined_thought = str(response2.choices[0].message.content)
    add_message(agent_name, "result", refined_thought)
    time.sleep(0.3)

    return refined_thought

def run_analysis(email_text: str, sender_info: str, recipient_info: str):
    """Run the 12-agent analysis pipeline"""
    global analysis_in_progress
    analysis_in_progress = True

    try:
        messages_store.clear()

        # ========================================
        # LAYER 1: CONTEXT EXTRACTION (3 agents)
        # ========================================
        add_message("System", "status", "🔍 CONTEXT EXTRACTION LAYER")

        # Agent 1: Context Analyzer
        add_message("Context Analyzer", "processing", "Extracting goal, tone, urgency...")
        context_analysis = agent_dialogue(
            "Context Analyzer",
            "You are a context extraction expert. Analyze the goal, tone, and urgency of emails. Be concise.",
            f"Analyze this email:\n\nFrom: {sender_info}\nTo: {recipient_info}\n\nEmail:\n{email_text}",
        )
        time.sleep(0.5)

        # Agent 2: Relationship Mapper
        add_message("Relationship Mapper", "processing", "Inferring sender-recipient dynamics...")
        relationship_analysis = agent_dialogue(
            "Relationship Mapper",
            "You are a relationship dynamics expert. Infer power structures, rapport, and communication history.",
            f"Analyze the relationship:\n\nFrom: {sender_info}\nTo: {recipient_info}\n\nEmail:\n{email_text}",
        )
        time.sleep(0.5)

        # Agent 3: Culture Detector
        add_message("Culture Detector", "processing", "Identifying cultural considerations...")
        culture_analysis = agent_dialogue(
            "Culture Detector",
            "You are a cultural communication expert. Identify cultural, regional, or professional norms that matter.",
            f"Detect cultural considerations:\n\nFrom: {sender_info}\nTo: {recipient_info}\n\nEmail:\n{email_text}",
        )
        time.sleep(0.5)

        # ========================================
        # LAYER 2: SIMULATION LAYER (4 agents)
        # ========================================
        add_message("System", "status", "🎭 SIMULATION LAYER")

        layer1_context = f"Context: {context_analysis}\nRelationship: {relationship_analysis}\nCulture: {culture_analysis}"

        # Agent 4: Recipient Persona
        add_message("Recipient Persona", "processing", "Simulating recipient's perspective...")
        recipient_response = agent_dialogue(
            "Recipient Persona",
            "You are role-playing as the email recipient. React authentically based on the analysis provided.",
            f"How would you react to this email:\n{email_text}",
            layer1_context
        )
        time.sleep(0.5)

        # Agent 5: Sender Advocate
        add_message("Sender Advocate", "processing", "Representing sender's goals...")
        sender_advocacy = agent_dialogue(
            "Sender Advocate",
            "You represent the sender's goals and interests. Explain what they're trying to achieve and why it matters.",
            f"Advocate for the sender's position in this email:\n{email_text}",
            layer1_context
        )
        time.sleep(0.5)

        # Agent 6: Devil's Advocate
        add_message("Devil's Advocate", "processing", "Challenging assumptions...")
        devils_advocacy = agent_dialogue(
            "Devil's Advocate",
            "You challenge assumptions and identify potential blind spots. Be skeptical and probe weaknesses.",
            f"What could go wrong? What's being overlooked?\n\nEmail: {email_text}\nRecipient reaction: {recipient_response}\nSender position: {sender_advocacy}",
            layer1_context
        )
        time.sleep(0.5)

        # Agent 7: Mediator
        add_message("Mediator", "processing", "Facilitating productive discussion...")
        mediation = agent_dialogue(
            "Mediator",
            "You facilitate productive dialogue between perspectives. Find common ground and identify actionable insights.",
            f"Mediate between:\n\nRecipient: {recipient_response}\nSender Advocate: {sender_advocacy}\nDevil's Advocate: {devils_advocacy}",
            layer1_context
        )
        time.sleep(0.5)

        # ========================================
        # LAYER 3: EVALUATION LAYER (3 agents)
        # ========================================
        add_message("System", "status", "⚖️ EVALUATION LAYER")

        layer2_context = f"{layer1_context}\n\nRecipient: {recipient_response}\nAdvocacy: {sender_advocacy}\nChallenges: {devils_advocacy}\nMediation: {mediation}"

        # Agent 8: Tone Validator
        add_message("Tone Validator", "processing", "Checking emotional appropriateness...")
        tone_validation = agent_dialogue(
            "Tone Validator",
            "You validate emotional tone and appropriateness. Check if the tone matches intent and context.",
            f"Validate the tone of this email:\n{email_text}",
            layer2_context
        )
        time.sleep(0.5)

        # Agent 9: Goal Alignment
        add_message("Goal Alignment", "processing", "Verifying objectives are met...")
        goal_check = agent_dialogue(
            "Goal Alignment",
            "You verify if the email achieves its stated or implied objectives. Check for goal-message alignment.",
            f"Does this email achieve its goals?\n{email_text}",
            layer2_context
        )
        time.sleep(0.5)

        # Agent 10: Risk Assessment
        add_message("Risk Assessment", "processing", "Flagging potential issues...")
        risk_analysis = agent_dialogue(
            "Risk Assessment",
            "You identify risks, misunderstandings, or negative consequences. Be specific about what could go wrong.",
            f"What are the risks of sending this email:\n{email_text}",
            layer2_context
        )
        time.sleep(0.5)

        # ========================================
        # LAYER 4: OUTPUT LAYER (2 agents)
        # ========================================
        add_message("System", "status", "📝 OUTPUT LAYER")

        layer3_context = f"{layer2_context}\n\nTone: {tone_validation}\nGoal Check: {goal_check}\nRisks: {risk_analysis}"

        # Agent 11: Feedback Synthesizer
        add_message("Feedback Synthesizer", "processing", "Creating actionable advice...")
        feedback_synthesis = agent_dialogue(
            "Feedback Synthesizer",
            "You synthesize all analysis into clear, actionable feedback. Provide specific improvements.",
            f"Synthesize actionable feedback for this email:\n{email_text}",
            layer3_context
        )
        time.sleep(0.5)

        # Agent 12: Email Rewriter
        add_message("Email Rewriter", "processing", "Generating improved versions...")
        rewritten_email = agent_dialogue(
            "Email Rewriter",
            "You rewrite emails to be more effective. Create an improved version incorporating all feedback.",
            f"Rewrite this email to address all concerns:\n\nOriginal:\n{email_text}\n\nFeedback: {feedback_synthesis}",
            layer3_context
        )

        add_message("System", "complete", "✅ 12-Agent Analysis Complete!")

    finally:
        analysis_in_progress = False

@app.route('/')
def home():
    """Serve the main HTML page"""
    return send_from_directory('.', 'index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_email():
    """Submit email for analysis"""
    try:
        data = request.get_json()
        email_text = data.get('email_text', '')
        sender_info = data.get('sender_info', 'Unknown')
        recipient_info = data.get('recipient_info', 'Unknown')

        thread = threading.Thread(
            target=run_analysis,
            args=(email_text, sender_info, recipient_info)
        )
        thread.start()

        return jsonify({"status": "submitted"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/messages', methods=['GET'])
def get_messages():
    """Get all messages"""
    return jsonify({
        "messages": messages_store,
        "analysis_in_progress": analysis_in_progress
    })

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🚀 Starting 12-Agent Email Analysis System")
    print("="*70)
    print("\n4 Layers:")
    print("  1. Context Extraction (3 agents)")
    print("  2. Simulation (4 agents)")
    print("  3. Evaluation (3 agents)")
    print("  4. Output (2 agents)")
    print("\nEach agent has 2 rounds of internal dialogue")
    print("\nOpen http://localhost:5001 in your browser")
    print("="*70 + "\n")

    app.run(host='0.0.0.0', port=5001, debug=True)
