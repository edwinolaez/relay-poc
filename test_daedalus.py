# test_daedalus.py
from relay.agents.daedalus import DaedalusAgent

# Wake up Daedalus
daedalus = DaedalusAgent()

print("\n--- Test 1: Math ---")
result1 = daedalus.execute("Calculate 15 multiplied by 47")
print(f"Final result: {result1}")

print("\n--- Test 2: Echo ---")
result2 = daedalus.execute("Echo back this message: RELAY Phase 5 is working!")
print(f"Final result: {result2}")