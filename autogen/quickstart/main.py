from autogen_core import AgentId, SingleThreadedAgentRuntime
from agent_modules import Modifier, Checker, Message
# Create an local embedded runtime.
runtime = SingleThreadedAgentRuntime()

# Start the runtime and send a direct message to the checker.
async def main():
    # Register agents inside the async function
    await Modifier.register(
        runtime,
        "modifier",
        # Modify the value by subtracting 1
        lambda: Modifier(modify_val=lambda x: x - 1),
    )

    await Checker.register(
        runtime,
        "checker",
        # Run until the value is less than or equal to 1
        lambda: Checker(run_until=lambda x: x <= 1),
    )
    
    # Start the runtime
    runtime.start()
    await runtime.send_message(Message(10), AgentId("checker", "default"))
    await runtime.stop_when_idle()

import asyncio
asyncio.run(main())