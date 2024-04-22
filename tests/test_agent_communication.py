import unittest
import asyncio
from web3 import ConcreteAgent, AgentOrchestrator

class TestAgentOrchestrator(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.agent1 = ConcreteAgent(agent_id=1)
        self.agent2 = ConcreteAgent(agent_id=2)

        self.orchestrator = AgentOrchestrator()

    async def asyncTearDown(self):
        # Ensure that behaviors are stopped and queues are cleared after each test
        self.agent1.stop_behaviors()
        self.agent2.stop_behaviors()
        self.agent1.outbox.clear()
        self.agent2.outbox.clear()
        self.agent1.inbox.clear()
        self.agent2.inbox.clear()

    # Integration Test to validate the message is added to outbox and removed from the inbox
    async def test_message_passing(self):
        await self.orchestrator.setup_agents([
            {'sender': self.agent1, 'receiver': self.agent2},
        ])

        # validate the agent1 is not running
        self.assertFalse(self.agent1.is_running)
        # validate the agent2 is not running
        self.assertFalse(self.agent2.is_running)

        # Create a task to run the agents
        task = asyncio.create_task(self.orchestrator.run_agents())

        try:
            # wait for agents to communicate
            await asyncio.wait_for(task, timeout=3)
        except asyncio.TimeoutError:
            # validate the agent1 is running
            self.assertTrue(self.agent1.is_running)
            # validate the agent2 is running
            self.assertTrue(self.agent2.is_running)
            self.orchestrator.stop_agents()

        # outbox is non-empty
        self.assertTrue(self.agent1.outbox)
        # validate the message is consumed
        self.assertFalse(self.agent2.inbox)