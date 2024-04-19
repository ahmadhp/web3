import asyncio
from web3 import ConcreteAgent, AgentOrchestrator


async def main():
    # Create instances of ConcreteAgent
    agent1 = ConcreteAgent(agent_id=1)
    agent2 = ConcreteAgent(agent_id=2)

    # Instantiate the AgentOrchestrator with the list of agents
    orchestrator = AgentOrchestrator()

    # Set up message handlers for each agent
    await orchestrator.setup_agents(
        [
            {
                'sender': agent1,
                'receiver': agent2
             },
            {
                'sender': agent2,
                'receiver': agent1
            },
        ]
    )

    # Start the behaviors of all agents
    await orchestrator.run_agents()


if __name__ == "__main__":
    asyncio.run(main())
