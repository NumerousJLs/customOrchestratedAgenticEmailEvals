"""
Get all agent addresses for the orchestrator
"""
from uagents import Agent

# Agent configurations (name, seed, port)
agents_config = [
    # Layer 1: Context Extraction
    ("context_analyzer", "context_analyzer_seed_123", 8101),
    ("relationship_mapper", "relationship_mapper_seed_456", 8102),
    ("culture_detector", "culture_detector_seed_789", 8103),

    # Layer 2: Simulation
    ("recipient_persona", "recipient_persona_seed_201", 8201),
    ("sender_advocate", "sender_advocate_seed_202", 8202),
    ("devils_advocate", "devils_advocate_seed_203", 8203),
    ("mediator", "mediator_seed_204", 8204),

    # Layer 3: Evaluation
    ("tone_validator", "tone_validator_seed_301", 8301),
    ("goal_alignment", "goal_alignment_seed_302", 8302),
    ("risk_assessor", "risk_assessor_seed_303", 8303),

    # Layer 4: Output
    ("feedback_synthesizer", "feedback_synthesizer_seed_401", 8401),
    ("email_rewriter", "email_rewriter_seed_402", 8402),
]

print("Agent Addresses:")
print("="*80)

agent_addresses = {}

for name, seed, port in agents_config:
    agent = Agent(name=name, seed=seed, port=port)
    address = agent.address
    agent_addresses[name] = address
    print(f"{name:25} -> {address}")

print("\n" + "="*80)
print("\nPython dict for orchestrator:")
print("="*80)
print("self.agents = {")
for name, address in agent_addresses.items():
    print(f'    "{name}": "{address}",')
print("}")
