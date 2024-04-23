import unittest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock

from web3 import AutonomousAgent, ConcreteAgent


class TestAutonomousAgent(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.agent = ConcreteAgent("agent1")
        self.event = asyncio.Event()

    async def test_handle_message(self):
        handler_mock = AsyncMock()
        self.agent.register_message_handler("test", handler_mock)
        message = {"type": "test", "content": "Test message"}
        await self.agent.handle_message(message)
        handler_mock.assert_called_once_with(message)

    def async_return(self, result):
        """ Alternative to AsyncMock to mock a callable
        """
        func = asyncio.Future()
        func.set_result(result)
        return func
    async def test_run_behaviors(self):
        behavior_mock = MagicMock(return_value=self.async_return({"type": "test", "content": "Test behavior"}))
        self.agent.register_behavior(behavior_mock)
        _ = asyncio.create_task(self.agent.run_behaviors())
        await asyncio.sleep(5)
        self.agent.stop_behaviors()
        behavior_mock.assert_called()

class TestConcreteAgent(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.agent = ConcreteAgent(agent_id=1)

    async def test_generate_random_message(self):
        message = self.agent.generate_random_message()
        self.assertEqual(len(message['content'].split()), 2)

    async def test_handle_hello_message(self):
        message = {"type": "hello", "content": "Hello, world!"}
        with patch('builtins.print') as mock_print:
            await self.agent.handle_hello_message(message)
            mock_print.assert_called_once_with(f"Agent {self.agent.agent_id} received hello message:", message)


if __name__ == '__main__':
    unittest.main()
