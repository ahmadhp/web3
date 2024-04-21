# Autonomous Agent System

This repository contains a Python (3.10) implementation of an autonomous agent system. The system consists of a base class `AutonomousAgent` that defines the core functionality and behavior of an autonomous agent, along with a concrete subclass `ConcreteAgent` that implements specific message handling and behaviors.

## Features

- **Message Handling**: The `AutonomousAgent` class provides methods for registering message handlers and handling incoming messages asynchronously.
- **Behavior Execution**: Agents can register behaviors that are executed asynchronously.
- **Communication**: Agents can communicate with each other by emitting and handling messages.
- **Orchestrator**: An Orchestrator which configures sending messages automatically from a specific agents outbox to another's inbox

## Installation

1. Clone the repository to your local machine:
    ```bash
    git clone https://github.com/ahmadhp/web3
    ```

2. Navigate to the project directory:
    ```bash
    cd web3
   python main.py
    ```


## Testing

To run the unit tests for the agent system, use the following command:
```bash
python3 -m unittest discover tests
```

![Integration Test Run](https://github.com/ahmadhp/web3/blob/feature/add-autonomous-agent-classes/integrationtest.png)

![Unit Test Run](https://github.com/ahmadhp/web3/blob/feature/add-autonomous-agent-classes/unittests.png)
