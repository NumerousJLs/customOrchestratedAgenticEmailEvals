"""
Output Agent - Final Feedback and Email Rewrites
"""
from uagents import Agent, Context, Model
from openai import OpenAI
from typing import List
import time

# Initialize OpenAI
client = OpenAI(
    base_url='https://api.asi1.ai/v1',
    api_key='sk_a77e3af6ceb240939b2c03ce2d30a9f750fb81f4266d44d192d3a4af763f7b8c',
)

# Models
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

class FinalOutput(Model):
    feedback: str
    rewritten_email: str
    overall_score: float
    original_chat_sender: str = ""

# Create output agent
output_agent = Agent(
    name="output",
    seed="output_email_seed_2024",
    port=8003,
    endpoint=["http://localhost:8003/submit"]
)

def add_message(ctx: Context, msg_type: str, content: str, recipient: str = ""):
    """Add a message to storage"""
    messages = ctx.storage.get("messages") or []
    messages.append({
        "timestamp": time.time(),
        "agent": "Output",
        "type": msg_type,
        "content": content,
        "recipient": recipient
    })
    ctx.storage.set("messages", messages)
    ctx.logger.info(f"[{msg_type}] {content[:100]}")

@output_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Output Agent started with address: {output_agent.address}")

    # Initialize message storage
    ctx.storage.set("messages", [])

    print(f"\n{'='*60}")
    print(f"📝 OUTPUT AGENT")
    print(f"Address: {output_agent.address}")
    print(f"Port: 8003")
    print(f"{'='*60}\n")

@output_agent.on_query(model=GetMessagesRequest, replies={MessagesResponse})
async def get_messages_handler(ctx: Context, sender: str, msg: GetMessagesRequest):
    """Query handler to get messages"""
    messages = ctx.storage.get("messages") or []
    new_messages = messages[msg.last_index:]

    await ctx.send(sender, MessagesResponse(
        messages=new_messages,
        last_index=len(messages)
    ))

@output_agent.on_message(EvaluationResult)
async def generate_output(ctx: Context, sender: str, msg: EvaluationResult):
    """Generate final output"""
    ctx.logger.info(f"Received evaluation from {sender}")
    add_message(ctx, "status", "Received evaluation from Evaluator", recipient="Evaluator")
    add_message(ctx, "processing", "Starting output generation...")

    try:
        # 1. Generate Feedback
        add_message(ctx, "processing", "Synthesizing feedback...")
        feedback_response = client.chat.completions.create(
            model="asi1-mini",
            messages=[
                {"role": "system", "content": "Synthesize evaluation into actionable feedback. Be concise but helpful. Include: summary, strengths, issues, action items."},
                {"role": "user", "content": f"Score: {msg.overall_score}/10\n\nTone: {msg.tone_evaluation[:200]}\nGoals: {msg.goal_alignment[:200]}\nRisks: {msg.risk_assessment[:200]}"}
            ],
            max_tokens=600,
        )
        feedback = str(feedback_response.choices[0].message.content)
        add_message(ctx, "result", "Feedback generated")

        # 2. Generate Rewrites
        add_message(ctx, "processing", "Generating rewritten versions...")
        rewrite_response = client.chat.completions.create(
            model="asi1-mini",
            messages=[
                {"role": "system", "content": "Generate THREE versions: 1) CONSERVATIVE (minimal changes), 2) RECOMMENDED (balanced), 3) BOLD (major revisions). Explain each briefly."},
                {"role": "user", "content": f"Rewrite:\n\nORIGINAL:\n{msg.email_text}\n\nEVALUATION:\nScore: {msg.overall_score}/10\nTone Issues: {msg.tone_evaluation[:200]}\nGoal Issues: {msg.goal_alignment[:200]}"}
            ],
            max_tokens=1200,
        )
        rewritten_email = str(rewrite_response.choices[0].message.content)
        add_message(ctx, "result", "Rewrites generated")

        # Create final output
        final_output = FinalOutput(
            feedback=feedback,
            rewritten_email=rewritten_email,
            overall_score=msg.overall_score,
            original_chat_sender=msg.original_chat_sender
        )

        add_message(ctx, "complete", f"Output generation complete! (Score: {msg.overall_score}/10)")
        add_message(ctx, "result", f"FEEDBACK: {feedback[:200]}...")
        add_message(ctx, "result", f"REWRITES: {rewritten_email[:200]}...")

        ctx.logger.info(f"\n{'='*60}")
        ctx.logger.info("FINAL OUTPUT")
        ctx.logger.info(f"{'='*60}")
        ctx.logger.info(f"Score: {msg.overall_score}/10\n")
        ctx.logger.info("Feedback:")
        ctx.logger.info(feedback)
        ctx.logger.info(f"\n{'='*60}")
        ctx.logger.info("Rewrites:")
        ctx.logger.info(rewritten_email)
        ctx.logger.info(f"{'='*60}\n")

        # If you want to send the output to another agent, uncomment:
        # recipient_address = ctx.storage.get("recipient_address")
        # if recipient_address:
        #     await ctx.send(recipient_address, final_output)

    except Exception as e:
        ctx.logger.exception(f"Error: {e}")
        add_message(ctx, "error", f"Error during output generation: {str(e)}")

if __name__ == "__main__":
    print("Starting Output Agent...")
    output_agent.run()
