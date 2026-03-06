# relay/coordinator.py
import os
from dotenv import load_dotenv
from relay.agents.seraph import SeraphAgent
from relay.agents.daedalus import DaedalusAgent

load_dotenv()


class RelayCoordinator:
    """
    Connects Seraph and Daedalus end-to-end.
    Seraph plans, Daedalus executes each subtask automatically.
    """

    def __init__(self):
        self.seraph = SeraphAgent()
        self.daedalus = DaedalusAgent()

    def run(self, task: str) -> dict:
        """
        Full pipeline:
        1. Seraph receives task and creates a plan
        2. Extract subtasks from the plan
        3. Daedalus executes each subtask
        4. Return combined results
        """
        print(f"\n{'='*50}")
        print(f"[RELAY] Starting pipeline for task:")
        print(f"[RELAY] {task}")
        print(f"{'='*50}\n")

        # Step 1 — Seraph plans
        print("[RELAY] Routing to Seraph for planning...")
        plan = self.seraph.create_plan(task)

        # Step 2 — Extract executable subtasks
        print("\n[RELAY] Extracting subtasks from plan...")
        subtasks = self._extract_subtasks(plan)
        print(f"[RELAY] Found {len(subtasks)} executable subtasks")

        # Step 3 — Daedalus executes each subtask
        results = []
        for i, subtask in enumerate(subtasks, 1):
            print(f"\n[RELAY] Sending subtask {i}/{len(subtasks)} to Daedalus...")
            result = self.daedalus.execute(subtask)
            results.append({
                "subtask": subtask,
                "result": result
            })

        # Step 4 — Assemble final output
        print(f"\n[RELAY] Pipeline complete. {len(results)} subtasks executed.")

        return {
            "task": task,
            "plan": plan,
            "subtask_results": results,
            "total_subtasks": len(results)
        }

    def _extract_subtasks(self, plan: str) -> list[str]:
        """
        Pull executable subtask descriptions from Seraph's plan.
        Looks for lines starting with ### SUBTASK or numbered steps.
        Limits to first 3 to control API costs during testing.
        """
        subtasks = []
        lines = plan.split('\n')

        for line in lines:
            line = line.strip()
            # Match lines like "### SUBTASK 1: Do something"
            if line.startswith('### SUBTASK') or line.startswith('### Step'):
                # Extract just the description part after the colon
                if ':' in line:
                    description = line.split(':', 1)[1].strip()
                    if description:
                        subtasks.append(description)

        # Fallback — if no subtasks found, use the whole task
        if not subtasks:
            subtasks = [plan[:200]]

        # Limit to 3 subtasks to keep API costs low during testing
        return subtasks[:3]