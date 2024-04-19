import asyncio
import random


class AutonomousAgent:
    """A base class representing an autonomous agent."""

    def __init__(self):
        """Initialize the AutonomousAgent."""
        self.message_handlers = {}
        self.behaviors = []
        self.is_running = False
        self.inbox = []
        self.outbox = []

    def register_message_handler(self, message_type, handler):
        """Register a message handler for a specific message type.

        Args:
            message_type (str): The type of message to handle.
            handler (callable): The function to handle the message.
        """
        if message_type not in self.message_handlers:
            self.message_handlers[message_type] = []
        self.message_handlers[message_type].append(handler)

    def register_behavior(self, behavior):
        """Register a behavior for the agent.

        Args:
            behavior (callable): The behavior function to register.
        """
        self.behaviors.append(behavior)

    async def handle_message(self, message):
        """Handle an incoming message asynchronously.

        Args:
            message (dict): The message to handle.
        """
        message_type = message['type']
        if message_type in self.message_handlers:
            for handler in self.message_handlers[message_type]:
                await handler(message)

    async def run_behaviors(self):
        """Run the behaviors of the agent asynchronously."""
        self.is_running = True
        while self.is_running:
            for behavior in self.behaviors:
                message = behavior()
                if message:
                    await self.emit_message(message)
            for recieved_message in self.inbox:
                await self.handle_message(recieved_message)
                self.inbox.remove(recieved_message)
            await asyncio.sleep(2)

    def stop_behaviors(self):
        """Stop the behavior loop."""
        self.is_running = False

    async def emit_message(self, message):
        """Emit a message asynchronously.

        Args:
            message (dict): The message to emit.
        """
        print(f"Emitting message to Outbox of Agent {self.agent_id}", message)
        self.outbox.append(message)


class ConcreteAgent(AutonomousAgent):
    """A concrete implementation of an autonomous agent."""

    def __init__(self, agent_id):
        """Initialize the ConcreteAgent.

        Args:
            agent_id (int): The ID of the agent.
        """
        super().__init__()
        self.agent_id = agent_id

        self.register_message_handler("hello", self.handle_hello_message)
        self.register_behavior(self.generate_random_message)

    async def handle_hello_message(self, message):
        """Handle a hello message asynchronously.

        Args:
            message (dict): The hello message to handle.
        """
        if "hello" in message.get("content", "").lower():
            print(f"Agent {self.agent_id} received hello message:", message)

    def generate_random_message(self):
        """Generate a random message.

        Returns:
            dict: A random message.
        """
        words = ["hello", "sun", "world", "space", "moon", "crypto", "sky", "ocean", "universe", "human"]
        message = " ".join(random.choices(words, k=2))
        return {"type": "random", "content": message}
