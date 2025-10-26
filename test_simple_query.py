"""
Test script for simple query agent
"""
import asyncio
from uagents import Model
from uagents.query import query


class TestRequest(Model):
    message: str


class Response(Model):
    text: str


async def main():
    # Address of the simple test agent (will be printed when agent starts)
    # Replace this with the actual address printed by test_agent_simple.py
    test_agent_address = "agent1q..."  # UPDATE THIS

    print(f"Querying test agent at {test_agent_address}...")

    try:
        response = await query(
            destination=test_agent_address,
            message=TestRequest(message="Hello, test agent!"),
            timeout=15.0
        )

        print(f"✓ Got response from test agent, type: {type(response)}")

        if isinstance(response, Response):
            print(f"Response text: {response.text}")
        else:
            print(f"Unexpected response type: {response}")

    except Exception as e:
        print(f"✗ Error querying test agent: {e}")


if __name__ == "__main__":
    asyncio.run(main())
