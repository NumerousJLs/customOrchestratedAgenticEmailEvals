"""
Evaluator Agent - Email Evaluation with Multi-Round Dialogue
"""
from uagents import Agent, Context, Model
from openai import OpenAI
from typing import List
import re
import time

# Initialize OpenAI
client = OpenAI(
    base_url='https://api.asi1.ai/v1',
    api_key='sk_a77e3af6ceb240939b2c03ce2d30a9f750fb81f4266d44d192d3a4af763f7b8c',
)

# Models
class TestRequest(Model):
    message: str

class Response(Model):
    text: str

class GetMessagesRequest(Model):
    last_index: int = 0

class AgentMessage(Model):
    timestamp: float
    agent: str
    type: str
    content: str
    recipient: str = ""

class MessagesResponse(Model):
    messages: List[AgentMessage]
    last_index: int

class AnalysisResult(Model):
    context_analysis: str
    relationship_analysis: str
    culture_analysis: str
    recipient_simulation: str
    sender_advocacy: str
    devils_advocate: str
    mediation_synthesis: str
    original_chat_sender: str = ""
    email_text: str = ""
    sender_info: str = ""
    recipient_info: str = ""

class EvaluationResult(Model):
    analysis_summary: str
    tone_evaluation: str
    goal_alignment: str
    risk_assessment: str
    overall_score: float
    send_recommendation: str
    original_chat_sender: str = ""
    email_text: str = ""
    sender_info: str = ""
    recipient_info: str = ""

class DialogueQuestion(Model):
    """Evaluator asks Analyzer a question"""
    round_number: int
    question: str
    context: str
    original_chat_sender: str = ""

class DialogueResponse(Model):
    """Analyzer responds to Evaluator's question"""
    round_number: int
    response: str
    original_chat_sender: str = ""

# Create evaluator agent
evaluator = Agent(
    name="evaluator",
    seed="evaluator_email_seed_2024",
    port=8002,
    endpoint=["http://localhost:8002/submit"]
)

def add_message(ctx: Context, msg_type: str, content: str, recipient: str = ""):
    """Add a message to storage"""
    messages = ctx.storage.get("messages") or []
    messages.append({
        "timestamp": time.time(),
        "agent": "Evaluator",
        "type": msg_type,
        "content": content,
        "recipient": recipient
    })
    ctx.storage.set("messages", messages)
    ctx.logger.info(f"[{msg_type}] {content[:100]}")

@evaluator.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Evaluator Agent started with address: {evaluator.address}")

    # Initialize message storage
    ctx.storage.set("messages", [])

    # Store output address (set this to your output agent's address)
    ctx.storage.set("output_address", "agent1qtdp0gp2v9zlz55q4j09lk8gy63uawz5ygxje4qzcgkvy04d0lwwcr9kcg9")

    print(f"\n{'='*60}")
    print(f"⚖️  EVALUATOR AGENT")
    print(f"Address: {evaluator.address}")
    print(f"Port: 8002")
    print(f"{'='*60}\n")

@evaluator.on_query(model=TestRequest, replies={Response})
async def test_query_handler(ctx: Context, sender: str, _query: TestRequest):
    """Simple test query handler"""
    ctx.logger.info(f"Test query received from {sender}")
    ctx.logger.info(f"Message: {_query.message}")
    try:
        await ctx.send(sender, Response(text=f"success - Evaluator received: {_query.message}"))
    except Exception as e:
        ctx.logger.error(f"Error in test query: {e}")
        await ctx.send(sender, Response(text="fail"))

@evaluator.on_query(model=GetMessagesRequest, replies={MessagesResponse})
async def get_messages_handler(ctx: Context, sender: str, msg: GetMessagesRequest):
    """Query handler to get messages"""
    messages = ctx.storage.get("messages") or []
    new_messages = messages[msg.last_index:]

    await ctx.send(sender, MessagesResponse(
        messages=new_messages,
        last_index=len(messages)
    ))

@evaluator.on_message(AnalysisResult)
async def evaluate_email(ctx: Context, sender: str, msg: AnalysisResult):
    """Receive analysis and start dialogue"""
    ctx.logger.info(f"Received analysis from {sender}")
    add_message(ctx, "status", "Received analysis from Analyzer", recipient="Analyzer")
    add_message(ctx, "processing", "Starting dialogue with Analyzer...")

    try:
        # Store the analysis for later use
        ctx.storage.set("current_analysis", {
            "context_analysis": msg.context_analysis,
            "relationship_analysis": msg.relationship_analysis,
            "culture_analysis": msg.culture_analysis,
            "recipient_simulation": msg.recipient_simulation,
            "sender_advocacy": msg.sender_advocacy,
            "devils_advocate": msg.devils_advocate,
            "mediation_synthesis": msg.mediation_synthesis,
            "email_text": msg.email_text,
            "sender_info": msg.sender_info,
            "recipient_info": msg.recipient_info,
            "original_chat_sender": msg.original_chat_sender
        })

        # Initialize dialogue state
        ctx.storage.set("dialogue_round", 1)
        ctx.storage.set("dialogue_history", [])
        ctx.storage.set("analyzer_address", sender)

        # Start dialogue - ask first question
        add_message(ctx, "processing", "Reviewing analysis and formulating questions (Round 1)...")

        question_response = client.chat.completions.create(
            model="asi1-mini",
            messages=[
                {"role": "system", "content": "You are an evaluator reviewing an email analysis. Ask ONE specific, critical question about the analysis. Be concise (1-2 sentences)."},
                {"role": "user", "content": f"Review this analysis and ask a critical question:\n\nContext: {msg.context_analysis[:300]}\nRelationship: {msg.relationship_analysis[:300]}\nRisks: {msg.devils_advocate[:300]}"}
            ],
            max_tokens=150,
        )
        question_text = str(question_response.choices[0].message.content)

        add_message(ctx, "dialogue", f"Evaluator asks (Round 1): {question_text[:150]}...", recipient="Analyzer")

        # Send question to Analyzer
        question = DialogueQuestion(
            round_number=1,
            question=question_text,
            context=msg.context_analysis[:400],
            original_chat_sender=msg.original_chat_sender
        )
        await ctx.send(sender, question)
        ctx.logger.info("Sent first dialogue question to Analyzer")

    except Exception as e:
        ctx.logger.exception(f"Error: {e}")
        add_message(ctx, "error", f"Error starting dialogue: {str(e)}")

@evaluator.on_message(DialogueResponse)
async def handle_dialogue_response(ctx: Context, sender: str, msg: DialogueResponse):
    """Handle Analyzer's response and continue dialogue or proceed to evaluation"""
    ctx.logger.info(f"Received dialogue response (Round {msg.round_number}) from Analyzer")
    add_message(ctx, "dialogue", f"Analyzer responds (Round {msg.round_number}): {msg.response[:150]}...", recipient="Analyzer")

    try:
        current_round = ctx.storage.get("dialogue_round") or 1
        max_rounds = 3  # 3 rounds of back-and-forth

        # Store response in history
        dialogue_history = ctx.storage.get("dialogue_history") or []
        dialogue_history.append({
            "round": msg.round_number,
            "type": "response",
            "content": msg.response
        })
        ctx.storage.set("dialogue_history", dialogue_history)

        # Decide whether to continue dialogue or proceed to evaluation
        if current_round < max_rounds:
            # Continue dialogue - ask another question
            next_round = current_round + 1
            ctx.storage.set("dialogue_round", next_round)

            add_message(ctx, "processing", f"Formulating follow-up question (Round {next_round})...")

            # Generate next question based on previous response
            question_response = client.chat.completions.create(
                model="asi1-mini",
                messages=[
                    {"role": "system", "content": f"You are continuing a dialogue. Based on the Analyzer's response, ask ONE follow-up question or challenge. Be specific and concise (1-2 sentences). This is round {next_round} of {max_rounds}."},
                    {"role": "user", "content": f"Analyzer responded: {msg.response}\n\nAsk a follow-up question or challenge their reasoning."}
                ],
                max_tokens=150,
            )
            question_text = str(question_response.choices[0].message.content)

            add_message(ctx, "dialogue", f"Evaluator asks (Round {next_round}): {question_text[:150]}...", recipient="Analyzer")

            # Send next question
            question = DialogueQuestion(
                round_number=next_round,
                question=question_text,
                context=msg.response,
                original_chat_sender=msg.original_chat_sender
            )
            await ctx.send(sender, question)
            ctx.logger.info(f"Sent round {next_round} question to Analyzer")

        else:
            # Dialogue complete - proceed with evaluation
            add_message(ctx, "status", "Dialogue complete. Proceeding with evaluation...")
            await proceed_with_evaluation(ctx, msg.original_chat_sender)

    except Exception as e:
        ctx.logger.exception(f"Error in dialogue: {e}")
        add_message(ctx, "error", f"Error in dialogue: {str(e)}")

async def proceed_with_evaluation(ctx: Context, original_chat_sender: str):
    """Complete the evaluation after dialogue"""
    try:
        # Get stored analysis
        analysis = ctx.storage.get("current_analysis")
        if not analysis:
            ctx.logger.error("No analysis found in storage")
            return

        # 1. Tone Validation
        add_message(ctx, "processing", "Evaluating tone appropriateness...")
        tone_response = client.chat.completions.create(
            model="asi1-mini",
            messages=[
                {"role": "system", "content": "Evaluate tone appropriateness and professionalism. Be concise."},
                {"role": "user", "content": f"Evaluate tone:\n\nContext: {analysis['context_analysis'][:300]}\nRelationship: {analysis['relationship_analysis'][:300]}"}
            ],
            max_tokens=250,
        )
        tone_evaluation = str(tone_response.choices[0].message.content)
        add_message(ctx, "result", f"Tone Evaluation: {tone_evaluation[:200]}...")

        # 2. Goal Alignment
        add_message(ctx, "processing", "Assessing goal achievement...")
        goal_response = client.chat.completions.create(
            model="asi1-mini",
            messages=[
                {"role": "system", "content": "Assess whether email achieves its goals. Be concise."},
                {"role": "user", "content": f"Evaluate goals:\n\nContext: {analysis['context_analysis'][:300]}\nRecipient: {analysis['recipient_simulation'][:300]}"}
            ],
            max_tokens=250,
        )
        goal_alignment = str(goal_response.choices[0].message.content)
        add_message(ctx, "result", f"Goal Alignment: {goal_alignment[:200]}...")

        # 3. Risk Assessment
        add_message(ctx, "processing", "Calculating risk score...")
        risk_response = client.chat.completions.create(
            model="asi1-mini",
            messages=[
                {"role": "system", "content": "Assess communication risks. Provide a risk score (1-10). Be concise."},
                {"role": "user", "content": f"Assess risks:\n\nProblems: {analysis['devils_advocate'][:300]}\nRecipient: {analysis['recipient_simulation'][:300]}"}
            ],
            max_tokens=250,
        )
        risk_assessment = str(risk_response.choices[0].message.content)
        add_message(ctx, "result", f"Risk Assessment: {risk_assessment[:200]}...")

        # 4. Overall Score
        add_message(ctx, "processing", "Calculating overall score...")
        overall_response = client.chat.completions.create(
            model="asi1-mini",
            messages=[
                {"role": "system", "content": "Provide an overall score (0-10) and brief recommendation."},
                {"role": "user", "content": f"Score this:\nTone: {tone_evaluation[:200]}\nGoals: {goal_alignment[:200]}\nRisks: {risk_assessment[:200]}"}
            ],
            max_tokens=200,
        )
        overall_eval = str(overall_response.choices[0].message.content)

        # Extract score
        score = 7.0
        try:
            score_match = re.search(r'(\d+\.?\d*)\s*[/]?\s*10', overall_eval)
            if score_match:
                score = float(score_match.group(1))
        except:
            pass

        add_message(ctx, "result", f"Overall Score: {score}/10")

        # Create evaluation result
        evaluation = EvaluationResult(
            analysis_summary=analysis['mediation_synthesis'],
            tone_evaluation=tone_evaluation,
            goal_alignment=goal_alignment,
            risk_assessment=risk_assessment,
            overall_score=score,
            send_recommendation=overall_eval,
            original_chat_sender=original_chat_sender,
            email_text=analysis['email_text'],
            sender_info=analysis['sender_info'],
            recipient_info=analysis['recipient_info']
        )

        add_message(ctx, "complete", f"Evaluation complete! (Score: {score}/10) Sending to Output...", recipient="Output")

        # Send to output
        output_addr = ctx.storage.get("output_address")
        await ctx.send(output_addr, evaluation)
        ctx.logger.info(f"Sent evaluation to output at {output_addr}")

    except Exception as e:
        ctx.logger.exception(f"Error in proceed_with_evaluation: {e}")
        add_message(ctx, "error", f"Error in evaluation: {str(e)}")

if __name__ == "__main__":
    print("Starting Evaluator Agent...")
    evaluator.run()
