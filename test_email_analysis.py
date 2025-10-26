"""
Simple Email Analysis Test Script
Uses LLMs directly to simulate analyzer-evaluator conversation
"""
from openai import OpenAI
import time

# Initialize OpenAI
client = OpenAI(
    base_url='https://api.asi1.ai/v1',
    api_key='sk_a77e3af6ceb240939b2c03ce2d30a9f750fb81f4266d44d192d3a4af763f7b8c',
)

def print_message(agent: str, msg_type: str, content: str):
    """Pretty print a message"""
    icons = {
        "Analyzer": "🔍",
        "Evaluator": "⚖️",
        "Output": "📤"
    }
    icon = icons.get(agent, "🤖")
    print(f"\n{icon} [{agent}] [{msg_type.upper()}]")
    print(f"{'─' * 70}")
    print(content)
    print(f"{'─' * 70}\n")

def analyze_email(email_text: str, sender_info: str, recipient_info: str):
    """Run full email analysis with LLM conversation"""

    print("\n" + "="*70)
    print("📧 EMAIL ANALYSIS STARTING")
    print("="*70)

    # STEP 1: Analyzer - Context Analysis
    print_message("Analyzer", "processing", "Analyzing email context and intent...")
    context_response = client.chat.completions.create(
        model="asi1-mini",
        messages=[
            {"role": "system", "content": "You are an expert at analyzing email context, intent, tone, urgency. Be concise (2-3 sentences)."},
            {"role": "user", "content": f"Analyze this email:\n\nFrom: {sender_info}\nTo: {recipient_info}\n\nEmail:\n{email_text}"}
        ],
        max_tokens=250,
    )
    context_analysis = str(context_response.choices[0].message.content)
    print_message("Analyzer", "result", f"Context Analysis:\n{context_analysis}")

    time.sleep(0.5)

    # STEP 2: Analyzer - Relationship Analysis
    print_message("Analyzer", "processing", "Analyzing relationship dynamics...")
    relationship_response = client.chat.completions.create(
        model="asi1-mini",
        messages=[
            {"role": "system", "content": "Analyze relationship dynamics and power structures. Be concise (2-3 sentences)."},
            {"role": "user", "content": f"Analyze relationship:\n\nFrom: {sender_info}\nTo: {recipient_info}\n\nEmail:\n{email_text}"}
        ],
        max_tokens=250,
    )
    relationship_analysis = str(relationship_response.choices[0].message.content)
    print_message("Analyzer", "result", f"Relationship Analysis:\n{relationship_analysis}")

    time.sleep(0.5)

    # STEP 3: Analyzer - Risk Assessment
    print_message("Analyzer", "processing", "Identifying potential risks...")
    risk_response = client.chat.completions.create(
        model="asi1-mini",
        messages=[
            {"role": "system", "content": "Identify risks and problems. Be brief (2-3 sentences)."},
            {"role": "user", "content": f"What could go wrong with this email:\n{email_text}"}
        ],
        max_tokens=200,
    )
    risk_assessment = str(risk_response.choices[0].message.content)
    print_message("Analyzer", "result", f"Risk Assessment:\n{risk_assessment}")

    print_message("Analyzer", "complete", "Analysis complete. Sending to Evaluator...")

    time.sleep(1)

    # STEP 4: Evaluator - Review
    print_message("Evaluator", "status", "Received analysis from Analyzer")
    print_message("Evaluator", "processing", "Reviewing analysis...")

    analysis_summary = f"""
Context: {context_analysis}
Relationship: {relationship_analysis}
Risks: {risk_assessment}
"""

    time.sleep(0.5)

    # STEP 5: Evaluator asks Analyzer a question
    question = "Can you elaborate on the most significant risk you identified? How likely is it to occur?"
    print_message("Evaluator", "dialogue", f"Question to Analyzer:\n{question}")

    time.sleep(1)

    # STEP 6: Analyzer responds
    print_message("Analyzer", "processing", "Formulating response to Evaluator...")
    response = client.chat.completions.create(
        model="asi1-mini",
        messages=[
            {"role": "system", "content": "You are the Analyzer defending your analysis. Be concise (2-3 sentences)."},
            {"role": "user", "content": f"Based on your analysis of risks: {risk_assessment}\n\nEvaluator asks: {question}"}
        ],
        max_tokens=250,
    )
    analyzer_response = str(response.choices[0].message.content)
    print_message("Analyzer", "dialogue", f"Response to Evaluator:\n{analyzer_response}")

    time.sleep(1)

    # STEP 7: Evaluator - Final Evaluation
    print_message("Evaluator", "processing", "Making final evaluation...")
    evaluation_response = client.chat.completions.create(
        model="asi1-mini",
        messages=[
            {"role": "system", "content": "You are an evaluator making final judgment. Be concise but decisive (3-4 sentences)."},
            {"role": "user", "content": f"Email Analysis:\n{analysis_summary}\n\nAnalyzer's response: {analyzer_response}\n\nProvide your final evaluation and recommendation."}
        ],
        max_tokens=300,
    )
    final_eval = str(evaluation_response.choices[0].message.content)
    print_message("Evaluator", "result", f"Final Evaluation:\n{final_eval}")

    time.sleep(0.5)

    # STEP 8: Evaluator - Recommendation
    recommendation_response = client.chat.completions.create(
        model="asi1-mini",
        messages=[
            {"role": "system", "content": "Provide a clear send/don't send recommendation. Be decisive (1-2 sentences)."},
            {"role": "user", "content": f"Based on this evaluation: {final_eval}\n\nShould this email be sent? Provide clear recommendation."}
        ],
        max_tokens=150,
    )
    recommendation = str(recommendation_response.choices[0].message.content)
    print_message("Evaluator", "complete", f"Recommendation:\n{recommendation}")

    time.sleep(0.5)

    # STEP 9: Output - Generate Feedback
    print_message("Output", "status", "Generating final feedback...")
    feedback_prompt = f"""
Email Analysis Summary:
- Context: {context_analysis}
- Relationship: {relationship_analysis}
- Risks: {risk_assessment}

Evaluation: {final_eval}
Recommendation: {recommendation}

Provide 3-5 specific, actionable improvements for the email.
"""

    feedback_response = client.chat.completions.create(
        model="asi1-mini",
        messages=[
            {"role": "system", "content": "Provide specific, actionable feedback in bullet points."},
            {"role": "user", "content": feedback_prompt}
        ],
        max_tokens=300,
    )
    feedback = str(feedback_response.choices[0].message.content)
    print_message("Output", "result", f"Actionable Feedback:\n{feedback}")

    print_message("Output", "complete", "✅ Analysis complete!")

    print("\n" + "="*70)
    print("📊 ANALYSIS COMPLETE")
    print("="*70 + "\n")


if __name__ == "__main__":
    # Example email
    email_text = """Hi team,

I need the report by EOD today. This is urgent and can't wait.

Thanks,
Manager"""

    sender_info = "Manager"
    recipient_info = "Engineering Team"

    print("\n📧 Testing Email:")
    print(f"From: {sender_info}")
    print(f"To: {recipient_info}")
    print(f"Content:\n{email_text}\n")

    # Run analysis
    analyze_email(email_text, sender_info, recipient_info)
