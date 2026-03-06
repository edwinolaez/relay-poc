# test_seraph.py
from relay.agents.seraph import SeraphAgent

# Wake up Seraph
seraph = SeraphAgent()

# Give him a real task
plan = seraph.create_plan(
    "Research the top 3 benefits of multi-agent AI systems "
    "and summarize them in plain English."
)

print("\n=== SERAPH'S PLAN ===")
print(plan)