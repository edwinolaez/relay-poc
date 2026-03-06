"""
Phase 2 integration test.

Run from the relay-poc root with your venv active:
    python -m pytest tests/test_phase2.py -v

Or run as a plain CLI script:
    python tests/test_phase2.py
"""

import asyncio
import os
import sys

# Make sure the project root is on the path when running as a script
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from relay.db.schema import MessageRole, TaskStatus
from relay.engine import RelayEngine

TEST_DB = "relay_test.db"


async def run_integration_test():
    print("\n=== RELAY Phase 2 — Integration Test ===\n")

    engine = RelayEngine(db_path=TEST_DB)
    await engine.start()

    try:
        # 1. Submit a task
        print("--- Step 1: Submit a task ---")
        task = await engine.submit_task(
            "Research the pros and cons of multi-agent AI systems."
        )
        task_id = task["id"]
        assert task["status"] == TaskStatus.PENDING.value, "Task should start as pending"
        print(f"  Task ID : {task_id}")
        print(f"  Status  : {task['status']}")

        # 2. Verify task persisted to DB
        print("\n--- Step 2: Verify task is in the database ---")
        fetched = await engine.get_task(task_id)
        assert fetched is not None, "Task not found in DB"
        assert fetched["description"] == task["description"]
        print(f"  Found in DB: {fetched['description'][:60]}...")

        # 3. Log some messages
        print("\n--- Step 3: Log messages ---")
        await engine.send_message(
            task_id, MessageRole.USER, "Please start the research task."
        )
        await engine.send_message(
            task_id, MessageRole.RELAY, "Task received. Routing to Seraph."
        )
        await engine.send_message(
            task_id, MessageRole.SERAPH, "Understood. I will decompose this task."
        )

        messages = await engine.get_messages(task_id)
        assert len(messages) == 3, f"Expected 3 messages, got {len(messages)}"
        print(f"  Messages stored: {len(messages)}")
        for m in messages:
            print(f"    [{m['role']}] {m['content'][:50]}")

        # 4. Check trace events
        print("\n--- Step 4: Check trace log ---")
        traces = await engine.get_traces(task_id)
        print(f"  Trace events: {len(traces)}")
        for t in traces:
            print(f"    {t['event']}")

        # 5. Complete the task
        print("\n--- Step 5: Complete the task ---")
        await engine.complete_task(task_id)
        updated = await engine.get_task(task_id)
        assert updated["status"] == TaskStatus.COMPLETED.value, "Task should be completed"
        print(f"  Final status: {updated['status']}")

        print("\n=== ALL TESTS PASSED ===\n")

    finally:
        await engine.stop()
        # Clean up test DB
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
            print(f"[cleanup] Removed {TEST_DB}")


if __name__ == "__main__":
    asyncio.run(run_integration_test())
