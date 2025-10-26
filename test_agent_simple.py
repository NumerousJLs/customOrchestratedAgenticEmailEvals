"""
Simple Test Agent - Basic Query Endpoint
"""
from uagents import Agent, Context, Model


class TestRequest(Model):
    message: str


class Response(Model):
    text: str


agent = Agent(
    name="test_agent_simple",
    seed="test_agent_simple_seed_2024",
    port=8005,
    endpoint=["http://localhost:8005/submit"],
)


@agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Starting up {agent.name}")
    ctx.logger.info(f"With address: {agent.address}")
    ctx.logger.info(f"And wallet address: {agent.wallet.address()}")

    print(f"\n{'='*60}")
    print(f"🧪 SIMPLE TEST AGENT")
    print(f"Name: {agent.name}")
    print(f"Address: {agent.address}")
    print(f"Port: 8005")
    print(f"{'='*60}\n")


@agent.on_query(model=TestRequest, replies={Response})
async def query_handler(ctx: Context, sender: str, _query: TestRequest):
    ctx.logger.info(f"Query received from {sender}")
    ctx.logger.info(f"Message: {_query.message}")
    try:
        # Simple echo response
        await ctx.send(sender, Response(text=f"success - received: {_query.message}"))
    except Exception as e:
        ctx.logger.error(f"Error: {e}")
        await ctx.send(sender, Response(text="fail"))


if __name__ == "__main__":
    print("Starting Simple Test Agent...")
    agent.run()
