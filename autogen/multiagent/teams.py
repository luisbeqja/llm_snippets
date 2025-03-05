import asyncio
import os
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.base import TaskResult
from autogen_agentchat.conditions import ExternalTermination, TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Create an OpenAI model client.
model_client = OpenAIChatCompletionClient(
    model="gpt-4o-2024-08-06",
    api_key=os.getenv("OPENAI_API_KEY"),
)

# Create the primary agent.
primary_agent = AssistantAgent(
    "primary",
    model_client=model_client,
    system_message="You are a helpful AI assistant.",
)

# Create the critic agent.
critic_agent = AssistantAgent(
    "critic",
    model_client=model_client,
    system_message="Provide constructive feedback. Respond with 'APPROVE' to when your feedbacks are addressed.",
)

# Define a termination condition that stops the task if the critic approves.
text_termination = TextMentionTermination("APPROVE")

# Create a team with the primary and critic agents.
async def main():
    team = RoundRobinGroupChat([primary_agent, critic_agent], termination_condition=text_termination)
    
    # When running inside a script, use a async main function and call it from `asyncio.run(...)`.
    await team.reset()  # Reset the team for a new task.
    async for message in team.run_stream(task="Write a short poem about the fall season."):  # type: ignore
        if isinstance(message, TaskResult):
            print("Stop Reason:", message.stop_reason)
        else:
            print(message.content)
"""     result = await team.run(task="Write a short poem about the fall season.")
    print(result) """

asyncio.run(main())