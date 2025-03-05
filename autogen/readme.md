AutoGen is an open-source programming framework for building AI agents and facilitating cooperation among multiple agents to solve tasks. AutoGen aims to provide an easy-to-use and flexible framework for accelerating development and research on agentic AI.

https://github.com/microsoft/autogen

# AutoGen Core Examples

This directory contains examples of using `autogen_core` for building agent-based systems.

## Projects

### 1. Quickstart Example - Number Processing
Located in `./quickstart/`

A simple example demonstrating basic `autogen_core` functionality with two agents:
- **Modifier Agent**: Decreases a number by 1
- **Checker Agent**: Continues until the number reaches 1

### 2. Multi-Agent Data Analysis
Located in `./multiagent/`

A more complex system with three specialized agents that collaborate to analyze data:
- **Data Collector Agent**: Gathers information
- **Data Analyst Agent**: Processes data and extracts insights
- **Report Generator Agent**: Creates a formatted report

## Getting Started

1. Install `autogen_core`:
```bash
pip install autogen_core
```

2. Run the examples:
```bash
# Quickstart example
python quickstart/main.py

# Multi-agent data analysis system
python multiagent/main.py
```

## Key Concepts

- **Agent Registration**: Registering agents with a runtime
- **Message Handlers**: Processing messages with decorated methods
- **Message Passing**: Communicating between agents
- **Runtime Management**: Starting/stopping the agent runtime

## Common Patterns

1. **Agent Definition**:
```python
@default_subscription
class MyAgent(RoutedAgent):
    def __init__(self):
        super().__init__("My agent description")
        
    @message_handler
    async def handle_message(self, message, ctx):
        # Process message
        # ...
        # Send response
        await self.publish_message(response_message, DefaultTopicId())
```

2. **Agent Registration**:
```python
await MyAgent.register(
    runtime,
    "my_agent",
    lambda: MyAgent()
)
```

3. **Message Sending**:
```python
await runtime.send_message(
    Message(content="Hello"),
    AgentId("target_agent", "default")
)
```

## Advanced Usage

Check the individual project READMEs for more detailed information on advanced usage patterns and customization options.
