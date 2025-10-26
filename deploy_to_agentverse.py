"""
Agentverse Deployment Helper
Assists with deploying agents to Agentverse using Chat Protocol.

Based on: https://docs.agentverse.ai/documentation/launch-agents/connect-your-agents-chat-protocol-integration
"""
import subprocess
import time
import os
import sys
import json
from typing import List, Dict


class AgentverseDeployer:
    """Helper for deploying agents to Agentverse."""

    def __init__(self):
        self.agentverse_api_key = os.getenv("AGENTVERSE_API_KEY")
        self.agent_seed_phrase = os.getenv("AGENT_SEED_PHRASE")

        # Agent configurations
        self.agents = [
            # Layer 1: Context Extraction
            {"name": "context_analyzer", "port": 8101, "script": "agents/layer1_context/context_analyzer_chat.py"},
            # Add more agents as needed
        ]

    def check_prerequisites(self) -> bool:
        """Check if prerequisites are met."""
        print("\n🔍 Checking Prerequisites...")
        print("="*70)

        all_good = True

        # Check Python
        python_version = sys.version_info
        if python_version.major >= 3 and python_version.minor >= 8:
            print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
        else:
            print(f"❌ Python 3.8+ required (you have {python_version.major}.{python_version.minor})")
            all_good = False

        # Check environment variables
        if self.agentverse_api_key:
            print(f"✅ AGENTVERSE_API_KEY is set")
        else:
            print(f"⚠️  AGENTVERSE_API_KEY not set (optional for local testing)")

        if self.agent_seed_phrase:
            print(f"✅ AGENT_SEED_PHRASE is set")
        else:
            print(f"⚠️  AGENT_SEED_PHRASE not set (using default seeds)")

        # Check for cloudflared
        try:
            result = subprocess.run(
                ["cloudflared", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                print(f"✅ cloudflared installed")
            else:
                print(f"⚠️  cloudflared not working properly")
        except FileNotFoundError:
            print(f"⚠️  cloudflared not installed")
            print(f"   Install: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/")
            all_good = False
        except Exception as e:
            print(f"⚠️  Could not check cloudflared: {e}")

        # Check Anthropic API key
        if os.getenv("ANTHROPIC_API_KEY"):
            print(f"✅ ANTHROPIC_API_KEY is set")
        else:
            print(f"❌ ANTHROPIC_API_KEY not set (required for agents)")
            all_good = False

        print("="*70)
        return all_good

    def start_local_agent(self, agent_config: Dict) -> subprocess.Popen:
        """Start an agent locally."""
        print(f"  → Starting {agent_config['name']} on port {agent_config['port']}...")

        try:
            process = subprocess.Popen(
                [sys.executable, agent_config['script']],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=os.environ.copy()
            )
            time.sleep(2)

            if process.poll() is None:
                print(f"  ✅ {agent_config['name']} started (PID: {process.pid})")
                return process
            else:
                print(f"  ❌ {agent_config['name']} failed to start")
                return None
        except Exception as e:
            print(f"  ❌ Error starting {agent_config['name']}: {e}")
            return None

    def create_tunnel(self, port: int) -> Dict[str, str]:
        """Create cloudflared tunnel for an agent."""
        print(f"  → Creating tunnel for port {port}...")

        try:
            # Start cloudflared tunnel
            process = subprocess.Popen(
                ["cloudflared", "tunnel", "--url", f"http://localhost:{port}"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Wait for tunnel URL (typically in stderr)
            time.sleep(3)

            # Try to get the URL from stderr
            # cloudflared prints the URL to stderr
            tunnel_url = None
            for _ in range(10):
                line = process.stderr.readline()
                if "trycloudflare.com" in line:
                    # Extract URL
                    parts = line.split()
                    for part in parts:
                        if "trycloudflare.com" in part:
                            tunnel_url = part.strip()
                            break
                    break
                time.sleep(0.5)

            if tunnel_url:
                print(f"  ✅ Tunnel created: {tunnel_url}")
                return {
                    "url": tunnel_url,
                    "process": process
                }
            else:
                print(f"  ⚠️  Could not detect tunnel URL automatically")
                print(f"     Check cloudflared output manually")
                return {
                    "url": f"https://<random>.trycloudflare.com",
                    "process": process
                }

        except Exception as e:
            print(f"  ❌ Error creating tunnel: {e}")
            return None

    def print_registration_instructions(self, agent_name: str, tunnel_url: str):
        """Print instructions for registering on Agentverse."""
        print(f"\n📋 Registration Instructions for {agent_name}")
        print("="*70)
        print("\n1. Go to: https://agentverse.ai/")
        print("2. Navigate to: Agents tab → '+ Launch an Agent'")
        print("3. Select: 'Chat Protocol'")
        print(f"4. Enter agent name: {agent_name}")
        print(f"5. Enter endpoint URL: {tunnel_url}")
        print("\n6. Run the registration command (if provided by Agentverse)")
        print(f"   Example:")
        print(f"   export AGENTVERSE_API_KEY=your_key")
        print(f"   export AGENT_SEED_PHRASE=your_seed")
        print(f"   # Then re-run the registration script")
        print("\n7. Click 'Evaluate Registration' to verify")
        print("8. Copy the agent address (starts with 'agent1q...')")
        print("\n="*70)

    def deploy_local_with_tunnel(self):
        """Deploy agents locally with cloudflared tunnels."""
        print("\n🚀 Deploying Agents Locally with Tunnels")
        print("="*70)

        if not self.check_prerequisites():
            print("\n❌ Prerequisites not met. Please fix the issues above.")
            return

        print("\n📦 Starting Agents...")
        print("="*70)

        agent_processes = []
        tunnel_processes = []
        agent_urls = {}

        try:
            for agent_config in self.agents:
                print(f"\n🤖 {agent_config['name']}")

                # Start agent
                agent_process = self.start_local_agent(agent_config)
                if agent_process:
                    agent_processes.append(agent_process)

                    # Create tunnel
                    tunnel_info = self.create_tunnel(agent_config['port'])
                    if tunnel_info:
                        tunnel_processes.append(tunnel_info['process'])
                        agent_urls[agent_config['name']] = tunnel_info['url']

                        # Print registration instructions
                        self.print_registration_instructions(
                            agent_config['name'],
                            tunnel_info['url']
                        )

            print("\n" + "="*70)
            print("✅ All agents started with tunnels!")
            print("="*70)

            print("\n📝 Agent Endpoints Summary:")
            print("="*70)
            for name, url in agent_urls.items():
                print(f"{name:25} -> {url}")

            print("\n" + "="*70)
            print("💡 Next Steps:")
            print("="*70)
            print("1. Register each agent on Agentverse (see instructions above)")
            print("2. Copy the agent addresses (agent1q...)")
            print("3. Update your orchestrator with these addresses")
            print("4. Test the agents through Agentverse chat interface")
            print("\n⚠️  Keep this script running to maintain the tunnels!")
            print("   Press Ctrl+C to stop all agents and tunnels")
            print("="*70 + "\n")

            # Keep running
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n\n🛑 Shutting down...")

        finally:
            print("Stopping agents...")
            for process in agent_processes:
                process.terminate()

            print("Stopping tunnels...")
            for process in tunnel_processes:
                process.terminate()

            print("✅ All processes stopped.")

    def print_hosted_agent_guide(self):
        """Print guide for deploying as hosted agents."""
        print("\n📚 Hosted Agent Deployment Guide")
        print("="*70)
        print("\nHosted agents run entirely on Agentverse (no local setup needed)")
        print("\nSteps:")
        print("1. Go to https://agentverse.ai/")
        print("2. Click 'Agents' → '+ Launch an Agent'")
        print("3. Select 'Create an Agentverse hosted Agent'")
        print("4. Copy your agent code:")
        print("   - Copy agents/shared/chat_protocol_agent.py")
        print("   - Copy agents/layer1_context/context_analyzer_chat.py")
        print("   - Merge into single file for Agentverse editor")
        print("5. Set environment variables in Agentverse:")
        print("   - ANTHROPIC_API_KEY=your_key")
        print("6. Click 'Deploy Agent'")
        print("7. Copy the agent address")
        print("\nRepeat for each of your 12 agents.")
        print("="*70 + "\n")


def main():
    """Main deployment flow."""
    deployer = AgentverseDeployer()

    print("\n🌐 AgentMail - Agentverse Deployment Helper")
    print("="*70)
    print("\nChoose deployment method:")
    print("1. Local agents with cloudflared tunnels (Testing)")
    print("2. Hosted agents on Agentverse (Production)")
    print("3. Check prerequisites only")
    print("="*70)

    choice = input("\nEnter choice (1-3): ").strip()

    if choice == "1":
        deployer.deploy_local_with_tunnel()
    elif choice == "2":
        deployer.print_hosted_agent_guide()
    elif choice == "3":
        deployer.check_prerequisites()
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()
