# relay/agents/seraph.py
import os
from dotenv import load_dotenv
import anthropic
from relay.genesys import load_genesys

load_dotenv()


class SeraphAgent:
    """
    Seraph — the strategic planning agent.
    Receives a task, sends it to Claude, returns a plan.
    """

    def __init__(self):
        self.identity = load_genesys("seraph")
        self.client = anthropic.Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )
        self.model = "claude-sonnet-4-20250514"
        print(f"[Seraph] Loaded identity: {self.identity.name} v{self.identity.version}")

    def create_plan(self, task_description: str) -> str:
        """
        Send a task to Claude and get back a plan.
        """
        print(f"[Seraph] Received task: {task_description}")
        print(f"[Seraph] Thinking...")

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=self.identity.to_system_prompt(),
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Please decompose this task into a clear, "
                        f"ordered execution plan:\n\n{task_description}"
                    )
                }
            ]
        )

        plan = response.content[0].text
        print(f"[Seraph] Plan created successfully.")
        return plan