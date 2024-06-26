import asyncio


class AgentOrchestrator:
    """Agents orchestrator for intercommunication between the agents
    """

    def __init__(self):
        self.agents = []

    def pass_message(self, receiver, sender):
        """Message communication for the agents
        """
        if len(sender.outbox) >= 1:
            print(f'Passing message from Outbox of Agent {sender.agent_id} to Inbox of {receiver.agent_id}')
            receiver.inbox.append(sender.outbox[-1])

    async def alert_user(self, sender, message):
        """Message alerts by the agents
        """
        print('Message received by agent', sender.agent_id, ':', message)

    async def setup_agents(self, config):
        """Sets up the agents
        """
        for obj in config:
            sender = obj['sender']
            receiver = obj['receiver']
            print('Setting up message handler to send outbox message of Agent', sender.agent_id, 'to inbox of Agent',
                  receiver.agent_id)
            sender.register_behavior(lambda: self.pass_message(receiver, sender))
            receiver.register_message_handler("random",
                                              lambda msg, other_agent=receiver: self.alert_user(receiver, msg))

            self.agents.extend([sender, receiver])

    async def run_agents(self):
        """Runs the agents
        """
        await asyncio.gather(*(agent.run_behaviors() for agent in self.agents))

    async def stop_agents(self):
        """Stops the agents
        """
        for task in asyncio.all_tasks():
            task.cancel()
