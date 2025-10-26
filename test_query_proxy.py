"""
Test the query proxy pattern with the agents
"""
import asyncio
import httpx

async def test_proxy():
    """Test the FastAPI proxy"""
    base_url = "http://localhost:5000"

    print("="*60)
    print("TESTING QUERY PROXY")
    print("="*60)

    async with httpx.AsyncClient(timeout=30.0) as client:
        # 1. Check if proxy is running
        print("\n1. Checking proxy status...")
        try:
            response = await client.get(f"{base_url}/")
            print(f"✓ Proxy is running: {response.json()}")
        except Exception as e:
            print(f"✗ Proxy not running: {e}")
            return

        # 2. Send an email for analysis
        print("\n2. Submitting email for analysis...")
        email_data = {
            "email_text": "Hi team, I need this done by EOD today. Thanks!",
            "sender_info": "Manager to Team",
            "recipient_info": "Engineering Team"
        }

        try:
            response = await client.post(f"{base_url}/analyze", json=email_data)
            print(f"✓ Email submitted: {response.json()}")
        except Exception as e:
            print(f"✗ Failed to submit email: {e}")

        # 3. Wait for processing
        print("\n3. Waiting for agents to process...")
        await asyncio.sleep(5)

        # 4. Query messages from all agents
        print("\n4. Querying messages from all agents...")
        try:
            response = await client.get(f"{base_url}/messages")
            data = response.json()
            print(f"✓ Retrieved {data['total']} messages")

            print("\nMessages:")
            for msg in data["messages"][:10]:  # Show first 10
                print(f"  [{msg['agent']}] {msg['type']}: {msg['content'][:80]}...")

        except Exception as e:
            print(f"✗ Failed to query messages: {e}")

        # 5. Query specific agent (Analyzer)
        print("\n5. Querying Analyzer agent specifically...")
        try:
            response = await client.get(f"{base_url}/messages/analyzer")
            data = response.json()
            if "messages" in data:
                print(f"✓ Retrieved {len(data['messages'])} messages from Analyzer")
            else:
                print(f"✗ Error: {data}")
        except Exception as e:
            print(f"✗ Failed to query Analyzer: {e}")

    print("\n" + "="*60)
    print("TEST COMPLETE")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(test_proxy())
