"""
Analyzer Agent - Email Analysis with Dialogue Support & Query API
"""
from uagents import Agent, Context, Model, Protocol
from openai import OpenAI
from typing import List
import time
from datetime import datetime
from uuid import uuid4
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    StartSessionContent,
    TextContent,
    chat_protocol_spec,
)

# Initialize OpenAI
client = OpenAI(
    base_url='https://api.asi1.ai/v1',
    api_key='sk_a77e3af6ceb240939b2c03ce2d30a9f750fb81f4266d44d192d3a4af763f7b8c',
)

# Models
class EmailInput(Model):
    email_text: str
    sender_info: str
    recipient_info: str
    original_chat_sender: str = ""

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

# Create analyzer agent
analyzer = Agent(
    name="analyzer",
    seed="analyzer_email_seed_2024",
    port=8001,
    endpoint=["http://localhost:8001/submit"]
)

# Helper function to create chat messages
def create_text_chat(text: str, end_session: bool = False) -> ChatMessage:
    content = [TextContent(type="text", text=text)]
    if end_session:
        content.append(EndSessionContent(type="end-session"))
    return ChatMessage(timestamp=datetime.utcnow(), msg_id=uuid4(), content=content)

# Create chat protocol compatible with the chat protocol spec
chat_protocol = Protocol(spec=chat_protocol_spec)

def add_message(ctx: Context, msg_type: str, content: str, recipient: str = ""):
    """Add a message to storage"""
    messages = ctx.storage.get("messages") or []
    messages.append({
        "timestamp": time.time(),
        "agent": "Analyzer",
        "type": msg_type,
        "content": content,
        "recipient": recipient
    })
    ctx.storage.set("messages", messages)
    ctx.logger.info(f"[{msg_type}] {content[:100]}")

@analyzer.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Analyzer Agent started with address: {analyzer.address}")

    # Initialize message storage
    ctx.storage.set("messages", [])

    # Store evaluator address (set this to your evaluator's address)
    ctx.storage.set("evaluator_address", "agent1qw4m67px6nqk0zjmqgv23hux0phn5cukjj8ewt5qlmcvhwmaxxx8v2r3m85")

    print(f"\n{'='*60}")
    print(f"📊 ANALYZER AGENT")
    print(f"Address: {analyzer.address}")
    print(f"Port: 8001")
    print(f"{'='*60}\n")

@analyzer.on_query(model=TestRequest, replies={Response})
async def test_query_handler(ctx: Context, sender: str, _query: TestRequest):
    """Simple test query handler"""
    ctx.logger.info(f"Test query received from {sender}")
    ctx.logger.info(f"Message: {_query.message}")
    try:
        # Simple echo response
        await ctx.send(sender, Response(text=f"success - Analyzer received: {_query.message}"))
    except Exception as e:
        ctx.logger.error(f"Error in test query: {e}")
        await ctx.send(sender, Response(text="fail"))

@analyzer.on_query(model=GetMessagesRequest, replies={MessagesResponse})
async def get_messages_handler(ctx: Context, sender: str, msg: GetMessagesRequest):
    """Query handler to get messages"""
    messages = ctx.storage.get("messages") or []
    new_messages = messages[msg.last_index:]

    await ctx.send(sender, MessagesResponse(
        messages=new_messages,
        last_index=len(messages)
    ))

@analyzer.on_message(EmailInput)
async def analyze_email(ctx: Context, sender: str, msg: EmailInput):
    """Analyze the email"""
    ctx.logger.info(f"Received email from {sender}")
    add_message(ctx, "status", "Starting email analysis...")

    try:
        # 1. Context Analysis
        add_message(ctx, "processing", "Analyzing email context and intent...")
        context_response = client.chat.completions.create(
            model="asi1-mini",
            messages=[
                {"role": "system", "content": "You are an expert at analyzing email context, intent, tone, urgency. Be concise (2-3 sentences)."},
                {"role": "user", "content": f"Analyze this email:\n\nFrom: {msg.sender_info}\nTo: {msg.recipient_info}\n\nEmail:\n{msg.email_text}"}
            ],
            max_tokens=250,
        )
        context_analysis = str(context_response.choices[0].message.content)
        add_message(ctx, "result", f"Context Analysis: {context_analysis[:200]}...")

        # 2. Relationship Analysis
        add_message(ctx, "processing", "Analyzing relationship dynamics...")
        relationship_response = client.chat.completions.create(
            model="asi1-mini",
            messages=[
                {"role": "system", "content": "Analyze relationship dynamics and power structures. Be concise (2-3 sentences)."},
                {"role": "user", "content": f"Analyze relationship:\n\nFrom: {msg.sender_info}\nTo: {msg.recipient_info}\n\nEmail:\n{msg.email_text}"}
            ],
            max_tokens=250,
        )
        relationship_analysis = str(relationship_response.choices[0].message.content)
        add_message(ctx, "result", f"Relationship: {relationship_analysis[:200]}...")

        # 3. Culture Analysis
        add_message(ctx, "processing", "Detecting cultural context...")
        culture_response = client.chat.completions.create(
            model="asi1-mini",
            messages=[
                {"role": "system", "content": "Detect cultural context and communication styles. Be concise (2-3 sentences)."},
                {"role": "user", "content": f"Analyze cultural aspects:\n\nFrom: {msg.sender_info}\nTo: {msg.recipient_info}"}
            ],
            max_tokens=200,
        )
        culture_analysis = str(culture_response.choices[0].message.content)
        add_message(ctx, "result", f"Culture: {culture_analysis[:150]}...")

        # 4. Recipient Simulation
        add_message(ctx, "processing", "Simulating recipient reaction...")
        recipient_response = client.chat.completions.create(
            model="asi1-mini",
            messages=[
                {"role": "system", "content": "Simulate how recipient would react. Be brief (2-3 sentences)."},
                {"role": "user", "content": f"How would {msg.recipient_info} react to:\n{msg.email_text}"}
            ],
            max_tokens=200,
        )
        recipient_simulation = str(recipient_response.choices[0].message.content)
        add_message(ctx, "result", f"Recipient View: {recipient_simulation[:150]}...")

        # 5. Sender Advocacy
        add_message(ctx, "processing", "Defending sender intentions...")
        sender_response = client.chat.completions.create(
            model="asi1-mini",
            messages=[
                {"role": "system", "content": "Defend sender's intentions. Be brief."},
                {"role": "user", "content": f"What are valid reasons for {msg.sender_info} to write:\n{msg.email_text}"}
            ],
            max_tokens=150,
        )
        sender_advocacy = str(sender_response.choices[0].message.content)

        # 6. Devil's Advocate
        add_message(ctx, "processing", "Identifying potential risks...")
        devils_response = client.chat.completions.create(
            model="asi1-mini",
            messages=[
                {"role": "system", "content": "Identify risks and problems. Be brief."},
                {"role": "user", "content": f"What could go wrong with this email:\n{msg.email_text}"}
            ],
            max_tokens=150,
        )
        devils_advocate = str(devils_response.choices[0].message.content)

        # 7. Mediation
        mediation_synthesis = "Analysis complete with balanced perspective from multiple viewpoints."

        # Create analysis result
        analysis = AnalysisResult(
            context_analysis=context_analysis,
            relationship_analysis=relationship_analysis,
            culture_analysis=culture_analysis,
            recipient_simulation=recipient_simulation,
            sender_advocacy=sender_advocacy,
            devils_advocate=devils_advocate,
            mediation_synthesis=mediation_synthesis,
            original_chat_sender=msg.original_chat_sender,
            email_text=msg.email_text,
            sender_info=msg.sender_info,
            recipient_info=msg.recipient_info
        )

        add_message(ctx, "complete", "Analysis complete! Sending to Evaluator...", recipient="Evaluator")

        # Send to evaluator
        evaluator_addr = ctx.storage.get("evaluator_address")
        await ctx.send(evaluator_addr, analysis)
        ctx.logger.info(f"Sent analysis to evaluator at {evaluator_addr}")

    except Exception as e:
        ctx.logger.exception(f"Error: {e}")
        add_message(ctx, "error", f"Error during analysis: {str(e)}")

@analyzer.on_message(DialogueQuestion)
async def handle_dialogue_question(ctx: Context, sender: str, msg: DialogueQuestion):
    """Respond to Evaluator's questions during dialogue"""
    ctx.logger.info(f"Received dialogue question (Round {msg.round_number}) from Evaluator")
    add_message(ctx, "dialogue", f"Evaluator asks (Round {msg.round_number}): {msg.question[:150]}...", recipient="Evaluator")

    try:
        # Store dialogue history
        dialogue_history = ctx.storage.get("dialogue_history") or []
        dialogue_history.append({
            "round": msg.round_number,
            "type": "question",
            "content": msg.question
        })
        ctx.storage.set("dialogue_history", dialogue_history)

        # Generate response using LLM
        add_message(ctx, "processing", f"Formulating response to Evaluator (Round {msg.round_number})...")
        response_obj = client.chat.completions.create(
            model="asi1-mini",
            messages=[
                {"role": "system", "content": "You are the Analyzer defending and clarifying your analysis. Be thoughtful but concise (2-4 sentences)."},
                {"role": "user", "content": f"Evaluator asks: {msg.question}\n\nYour analysis context: {msg.context}\n\nProvide a clear response."}
            ],
            max_tokens=250,
        )
        response_text = str(response_obj.choices[0].message.content)

        add_message(ctx, "dialogue", f"Analyzer responds (Round {msg.round_number}): {response_text[:150]}...", recipient="Evaluator")

        # Store in dialogue history
        dialogue_history.append({
            "round": msg.round_number,
            "type": "response",
            "content": response_text
        })
        ctx.storage.set("dialogue_history", dialogue_history)

        # Send response back to Evaluator
        dialogue_response = DialogueResponse(
            round_number=msg.round_number,
            response=response_text,
            original_chat_sender=msg.original_chat_sender
        )
        await ctx.send(sender, dialogue_response)
        ctx.logger.info(f"Sent dialogue response to Evaluator")

    except Exception as e:
        ctx.logger.exception(f"Error in dialogue: {e}")
        add_message(ctx, "error", f"Error in dialogue: {str(e)}")

# Chat Protocol Handlers
@chat_protocol.on_message(ChatMessage)
async def handle_chat_message(ctx: Context, sender: str, msg: ChatMessage):
    """Handle incoming chat messages"""
    # Send acknowledgement for receiving the message
    await ctx.send(
        sender,
        ChatAcknowledgement(timestamp=datetime.now(), acknowledged_msg_id=msg.msg_id),
    )

    # Greet if a session starts
    if any(isinstance(item, StartSessionContent) for item in msg.content):
        greeting = "Hi! I'm the Analyzer agent. I specialize in email analysis, relationship dynamics, and cultural context. How can I help?"
        add_message(ctx, "chat", f"Chat started with {sender[:16]}... - Sent greeting")
        await ctx.send(sender, create_text_chat(greeting, end_session=False))
        return

    # Get text from message
    text = msg.text()
    if not text:
        return

    # Store incoming chat message
    add_message(ctx, "chat", f"Chat from {sender[:16]}...: {text[:100]}", recipient=sender[:16])

    try:
        # Generate response using LLM
        r = client.chat.completions.create(
            model="asi1-mini",
            messages=[
                {"role": "system", "content": """You are the Analyzer agent, an expert in email analysis. You help users understand:
- Email context, intent, tone, and urgency
- Relationship dynamics and power structures
- Cultural communication styles
- Recipient perspectives and reactions
- Risk assessment and mediation

Provide helpful, concise responses about email analysis topics."""},
                {"role": "user", "content": text},
            ],
            max_tokens=2048,
        )

        response = str(r.choices[0].message.content)

        # Store outgoing chat response
        add_message(ctx, "chat", f"Chat to {sender[:16]}...: {response[:100]}", recipient=sender[:16])

    except Exception as e:
        ctx.logger.exception('Error querying model for chat')
        response = f"An error occurred while processing your message. Please try again later."
        add_message(ctx, "error", f"Chat error with {sender[:16]}...: {str(e)}")

    await ctx.send(sender, create_text_chat(response, end_session=True))

@chat_protocol.on_message(ChatAcknowledgement)
async def handle_chat_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    """Handle chat acknowledgements"""
    # Log acknowledgements but don't need to store them
    ctx.logger.debug(f"Received chat acknowledgement from {sender}")

# Include the chat protocol with the analyzer agent
analyzer.include(chat_protocol, publish_manifest=True)

if __name__ == "__main__":
    print("Starting Analyzer Agent...")
    analyzer.run()
