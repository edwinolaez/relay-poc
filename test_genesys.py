# test_genesys.py
from relay.genesys import load_genesys

# Load Seraph's identity
seraph = load_genesys("seraph")
print("=== SERAPH IDENTITY ===")
print(f"Name: {seraph.name}")
print(f"Role: {seraph.role}")
print(f"Version: {seraph.version}")
print(f"\nCapabilities: {seraph.capabilities}")
print(f"\nConstraints: {seraph.constraints}")
print("\n=== SERAPH SYSTEM PROMPT ===")
print(seraph.to_system_prompt())

print("\n" + "="*50 + "\n")

# Load Daedalus's identity
daedalus = load_genesys("daedalus")
print("=== DAEDALUS IDENTITY ===")
print(f"Name: {daedalus.name}")
print(f"Role: {daedalus.role}")
print(f"\nCapabilities: {daedalus.capabilities}")
print("\n=== DAEDALUS SYSTEM PROMPT ===")
print(daedalus.to_system_prompt())