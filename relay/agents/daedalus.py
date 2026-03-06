# relay/agents/daedalus.py
import os
from dotenv import load_dotenv
import anthropic
from relay.genesys import load_genesys
from relay.tools.registry import ToolRegistry, Tool

load_dotenv()


def build_default_tools() -> ToolRegistry:
    """Build Daedalus's default tool belt."""
    registry = ToolRegistry()

    # Tool 1 — Calculator
    def calculate(expression: str) -> str:
        try:
            result = eval(expression)
            return f"Result: {expression} = {result}"
        except Exception as e:
            return f"Calculation error: {e}"

    # Tool 2 — Summarizer
    def summarize(text: str, max_sentences: int = 3) -> str:
        sentences = text.split(".")
        shortened = ".".join(sentences[:max_sentences])
        return f"Summary: {shortened}."

    # Tool 3 — Echo (useful for testing)
    def echo(message: str) -> str:
        return f"Echo: {message}"

    registry.register(Tool(
        name="calculate",
        description="Evaluate a math expression. Pass expression as a string.",
        handler=calculate
    ))
    registry.register(Tool(
        name="summarize",
        description="Summarize a block of text into key sentences.",
        handler=summarize
    ))
    registry.register(Tool(
        name="echo",
        description="Echo a message back. Useful for testing.",
        handler=echo
    ))

    return registry


class DaedalusAgent:
    """
    Daedalus — the technical execution agent.
    Receives subtasks, uses tools, returns results.
    """

    def __init__(self):
        self.identity = load_genesys("daedalus")
        self.client = anthropic.Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )
        self.model = "claude-sonnet-4-20250514"
        self.tools = build_default_tools()
        print(f"[Daedalus] Loaded identity: {self.identity.name} v{self.identity.version}")
        print(f"[Daedalus] Tools available: {self.tools.list_tools()}")

    def execute(self, subtask: str) -> str:
        """
        Receive a subtask, decide which tool to use,
        execute it, and return the result.
        """
        print(f"[Daedalus] Received subtask: {subtask}")

        # Ask Claude (as Daedalus) which tool to use
        tool_descriptions = self.tools.describe_tools()

        response = self.client.messages.create(
            model=self.model,
            max_tokens=512,
            system=self.identity.to_system_prompt(),
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"You have these tools available:\n{tool_descriptions}\n\n"
                        f"Subtask to execute: {subtask}\n\n"
                        f"Choose the best tool and respond in this exact format:\n"
                        f"TOOL: <tool_name>\n"
                        f"INPUT: <input to pass to the tool>\n"
                        f"REASON: <why you chose this tool>"
                    )
                }
            ]
        )

        decision = response.content[0].text
        print(f"[Daedalus] Tool decision:\n{decision}")

        # Parse the decision and execute the tool
        lines = decision.strip().split("\n")
        tool_name = None
        tool_input = None

        for line in lines:
            if line.startswith("TOOL:"):
                tool_name = line.replace("TOOL:", "").strip()
            elif line.startswith("INPUT:"):
                tool_input = line.replace("INPUT:", "").strip()

        if tool_name and tool_input:
            result = self.tools.execute(tool_name, **{
                "expression" if tool_name == "calculate" else
                "text" if tool_name == "summarize" else
                "message": tool_input
            })
            print(f"[Daedalus] Tool result: {result}")
            return result
        else:
            return f"[Daedalus] Could not parse tool decision: {decision}"