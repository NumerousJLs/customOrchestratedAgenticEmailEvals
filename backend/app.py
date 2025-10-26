"""
12-Agent Email Analysis System
4 Layers with 2 rounds of dialogue between each agent
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from anthropic import Anthropic
import time
import threading
from typing import List, Dict
import os

# Initialize Anthropic
client = Anthropic(
    api_key='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',
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

def agent_response(agent_name: str, system_prompt: str, user_prompt: str, context: str = "") -> str:
    """Get a single response from an agent"""
    full_prompt = f"{context}\n\n{user_prompt}" if context else user_prompt

    response = client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=300,
        system=system_prompt,
        messages=[
            {"role": "user", "content": full_prompt}
        ]
    )
    content = str(response.content[0].text)
    add_message(agent_name, "message", content)
    time.sleep(0.3)
    return content

def two_agent_dialogue(agent1_name: str, agent1_prompt: str, agent2_name: str, agent2_prompt: str, topic: str, context: str = "") -> tuple:
    """Have 2 rounds of dialogue between two agents about the email"""

    # Round 1: Agent 1 speaks about the email
    response1 = agent_response(agent1_name, agent1_prompt, topic, context)
    time.sleep(0.3)

    # Round 1: Agent 2 responds - keeping email in context
    response2 = agent_response(
        agent2_name,
        agent2_prompt,
        f"{topic}\n\n{agent1_name} said: {response1}\n\nRespond to their point while analyzing the email:",
        context
    )
    time.sleep(0.3)

    # Round 2: Agent 1 responds back - keeping email in context
    response3 = agent_response(
        agent1_name,
        agent1_prompt,
        f"{topic}\n\n{agent2_name} said: {response2}\n\nRespond to their point while continuing to analyze the email:",
        context
    )
    time.sleep(0.3)

    # Round 2: Agent 2 final response - keeping email in context
    response4 = agent_response(
        agent2_name,
        agent2_prompt,
        f"{topic}\n\n{agent1_name} said: {response3}\n\nProvide your final analysis of the email, building on this dialogue:",
        context
    )
    time.sleep(0.3)

    return response1, response2, response3, response4

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

        # Dialogue 1: Context Analyzer <-> Relationship Mapper
        add_message("System", "status", "Context Analyzer discussing with Relationship Mapper...")
        ctx1, ctx2, ctx3, ctx4 = two_agent_dialogue(
            "Context Analyzer",
            "You are a context extraction expert. Analyze the goal, tone, and urgency of emails. Engage in dialogue with the Relationship Mapper.",
            "Relationship Mapper",
            "You are a relationship dynamics expert. Infer power structures, rapport, and communication history. Engage in dialogue with the Context Analyzer.",
            f"Discuss this email:\n\nFrom: {sender_info}\nTo: {recipient_info}\n\nEmail:\n{email_text}"
        )
        context_analysis = ctx4
        relationship_analysis = ctx2
        time.sleep(0.5)

        # Dialogue 2: Relationship Mapper <-> Culture Detector
        add_message("System", "status", "Relationship Mapper discussing with Culture Detector...")
        rel1, cul1, rel2, cul2 = two_agent_dialogue(
            "Relationship Mapper",
            "You are a relationship dynamics expert. Discuss how relationship dynamics affect communication.",
            "Culture Detector",
            "You are a cultural communication expert. Identify cultural, regional, or professional norms that matter.",
            f"Building on previous context, discuss cultural aspects:\n\nEmail:\n{email_text}\n\nFrom: {sender_info}\nTo: {recipient_info}",
            f"Previous context: {context_analysis}"
        )
        culture_analysis = cul2
        time.sleep(0.5)

        # ========================================
        # LAYER 2: SIMULATION LAYER (4 agents)
        # ========================================
        add_message("System", "status", "🎭 SIMULATION LAYER")

        layer1_context = f"Context: {context_analysis}\nRelationship: {relationship_analysis}\nCulture: {culture_analysis}"

        # Dialogue 3: Recipient Persona <-> Sender Advocate
        add_message("System", "status", "Recipient Persona discussing with Sender Advocate...")
        rec1, sen1, rec2, sen2 = two_agent_dialogue(
            "Recipient Persona",
            "You are role-playing as the email recipient. React authentically and discuss your perspective.",
            "Sender Advocate",
            "You represent the sender's goals and interests. Advocate for what they're trying to achieve.",
            f"Discuss this email:\n{email_text}",
            layer1_context
        )
        recipient_response = rec2
        sender_advocacy = sen2
        time.sleep(0.5)

        # Dialogue 4: Devil's Advocate <-> Mediator
        add_message("System", "status", "Devil's Advocate discussing with Mediator...")
        dev1, med1, dev2, med2 = two_agent_dialogue(
            "Devil's Advocate",
            "You challenge assumptions and identify potential blind spots. Be skeptical and probe weaknesses.",
            "Mediator",
            "You facilitate productive dialogue between perspectives. Find common ground and identify actionable insights.",
            f"Discuss what could go wrong:\n\nEmail: {email_text}\nRecipient says: {recipient_response}\nSender position: {sender_advocacy}",
            layer1_context
        )
        devils_advocacy = dev2
        mediation = med2
        time.sleep(0.5)

        # ========================================
        # LAYER 3: EVALUATION LAYER (3 agents)
        # ========================================
        add_message("System", "status", "⚖️ EVALUATION LAYER")

        layer2_context = f"{layer1_context}\n\nRecipient: {recipient_response}\nAdvocacy: {sender_advocacy}\nChallenges: {devils_advocacy}\nMediation: {mediation}"

        # Dialogue 5: Tone Validator <-> Goal Alignment
        add_message("System", "status", "Tone Validator discussing with Goal Alignment...")
        tone1, goal1, tone2, goal2 = two_agent_dialogue(
            "Tone Validator",
            "You validate emotional tone and appropriateness. Check if the tone matches intent and context.",
            "Goal Alignment",
            "You verify if the email achieves its stated or implied objectives. Check for goal-message alignment.",
            f"Evaluate this email:\n{email_text}",
            layer2_context
        )
        tone_validation = tone2
        goal_check = goal2
        time.sleep(0.5)

        # Dialogue 6: Goal Alignment <-> Risk Assessment
        add_message("System", "status", "Goal Alignment discussing with Risk Assessment...")
        goal3, risk1, goal4, risk2 = two_agent_dialogue(
            "Goal Alignment",
            "You verify if objectives are met. Discuss potential alignment issues.",
            "Risk Assessment",
            "You identify risks, misunderstandings, or negative consequences. Be specific about what could go wrong.",
            f"Discuss risks and goal achievement:\n\nEmail: {email_text}\nTone assessment: {tone_validation}",
            layer2_context
        )
        risk_analysis = risk2
        time.sleep(0.5)

        # ========================================
        # LAYER 4: OUTPUT LAYER (2 agents)
        # ========================================
        add_message("System", "status", "📝 OUTPUT LAYER")

        layer3_context = f"{layer2_context}\n\nTone: {tone_validation}\nGoal Check: {goal_check}\nRisks: {risk_analysis}"

        # Dialogue 7: Feedback Synthesizer <-> Email Rewriter
        add_message("System", "status", "Feedback Synthesizer discussing with Email Rewriter...")
        feed1, rew1, feed2, rew2 = two_agent_dialogue(
            "Feedback Synthesizer",
            "You synthesize all analysis into clear, actionable feedback. Provide specific improvements.",
            "Email Rewriter",
            "You rewrite emails to be more effective. Create an improved version incorporating all feedback.",
            f"Collaborate on improving this email:\n\nOriginal:\n{email_text}",
            layer3_context
        )
        feedback_synthesis = feed2
        rewritten_email = rew2
        time.sleep(0.5)

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
