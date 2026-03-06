# relay/genesys.py
import yaml
from pathlib import Path
from dataclasses import dataclass


@dataclass
class GeneSysIdentity:
    name: str
    role: str
    version: str
    description: str
    capabilities: list
    constraints: list
    raw_document: dict

    def to_system_prompt(self) -> str:
        """Convert GeneSys document into an LLM system prompt."""
        lines = [
            f"You are {self.name}, a {self.role}.",
            f"\nIDENTITY:\n{self.description}",
            f"\nCAPABILITIES:",
        ]
        for cap in self.capabilities:
            lines.append(f"  - {cap}")
        lines.append(f"\nCONSTRAINTS:")
        for con in self.constraints:
            lines.append(f"  - {con}")
        return "\n".join(lines)


def load_genesys(agent_name: str) -> GeneSysIdentity:
    """Load a GeneSys identity document by agent name."""
    path = Path(f"genesys/{agent_name.lower()}.yaml")

    if not path.exists():
        raise FileNotFoundError(
            f"No GeneSys document found for agent: {agent_name}"
        )

    doc = yaml.safe_load(path.read_text(encoding="utf-8"))

    return GeneSysIdentity(
        name=doc["agent"]["name"],
        role=doc["agent"]["role"],
        version=doc["agent"]["version"],
        description=doc["identity"]["description"],
        capabilities=doc["capabilities"],
        constraints=doc["constraints"],
        raw_document=doc,
    )