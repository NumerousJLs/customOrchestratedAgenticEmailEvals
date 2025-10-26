"""
Test script for analyzer's simple test query endpoint
"""
import asyncio
from uagents import Model
from uagents.query import query


class TestRequest(Model):
    message: str


class Response(Model):
    text: str


async def main():
    # Analyzer's address (from analyzer.py with seed "analyzer_email_seed_2024")
    # This will be: agent1qw4m67px6nqk0zjmqgv23hux0phn5cukjj8ewt5qlmcvhwmaxxx8v2r3m85
    analyzer_address = "agent1qw4m67px6nqk0zjmqgv23hux0phn5cukjj8ewt5qlmcvhwmaxxx8v2r3m85"

    print(f"Testing Analyzer's simple query endpoint...")
    print(f"Address: {analyzer_address}")
    print(f"Expected endpoint: http://localhost:8001/submit\n")

    try:
        print("Sending test query...")
        response = await query(
            destination=analyzer_address,
            message=TestRequest(message="Hello, Analyzer!"),
            timeout=15.0
        )

        print(f"✓ Got response from analyzer")
        print(f"Response type: {type(response)}")

        if isinstance(response, Response):
            print(f"✓ Response text: {response.text}")
        else:
            print(f"Response: {response}")

    except TimeoutError:
        print("✗ Request timed out - Is the analyzer agent running on port 8001?")
    except Exception as e:
        print(f"✗ Error querying analyzer: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("="*60)
    print("ANALYZER SIMPLE QUERY TEST")
    print("="*60)
    print("\nMake sure analyzer.py is running first:")
    print("  python agents/analyzer.py")
    print("\n" + "="*60 + "\n")

    asyncio.run(main())
