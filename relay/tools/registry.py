# relay/tools/registry.py
from dataclasses import dataclass
from typing import Callable, Any


@dataclass
class Tool:
    name: str
    description: str
    handler: Callable[..., Any]


class ToolRegistry:
    """Holds all tools Daedalus can use."""

    def __init__(self):
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool):
        """Add a tool to the registry."""
        self._tools[tool.name] = tool
        print(f"[ToolRegistry] Registered tool: {tool.name}")

    def execute(self, name: str, **kwargs) -> Any:
        """Run a tool by name."""
        if name not in self._tools:
            raise ValueError(f"Unknown tool: {name}")
        print(f"[ToolRegistry] Executing tool: {name}")
        return self._tools[name].handler(**kwargs)

    def list_tools(self) -> list[str]:
        """Return names of all available tools."""
        return list(self._tools.keys())

    def describe_tools(self) -> str:
        """Return a readable description of all tools."""
        lines = []
        for tool in self._tools.values():
            lines.append(f"- {tool.name}: {tool.description}")
        return "\n".join(lines)