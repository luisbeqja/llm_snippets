from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
import asyncio
import sys
import os

# Add project root to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import web_search from the tools package
from tools.web_search import web_search


# Create an agent that uses the OpenAI GPT-4o model.
model_client = OpenAIChatCompletionClient(
    model="gpt-4o",
    # You should consider using environment variables for API keys
    api_key="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",
)

tool_user = AssistantAgent(
    name="tool_user",
    model_client=model_client,
    tools=[web_search],
    system_message="You are a helpful AI assistant with access to a web search tool. Use the tool to find information when needed, then provide a thorough response to the user's query.",
)

tool_assistant = AssistantAgent(
    name="tool_assistant",
    model_client=model_client,
    tools=[web_search],
    system_message="You are a helpful AI assistant improve the web search tool response. Return a user friendly response to the user.",
)

critic_agent = AssistantAgent(
    "critic",
    model_client=model_client,
    system_message="Provide constructive feedback. Respond with 'APPROVE' to when your feedbacks are addressed.",
)

async def assistant_run() -> None:
    text_termination = TextMentionTermination("APPROVE")
    team = RoundRobinGroupChat([tool_user, tool_assistant, critic_agent], termination_condition=text_termination)
    
    """     async for message in team.run_stream(task="Where are the next Olimpiadi?"):  # type: ignore
        if isinstance(message, TaskResult):
            print("Stop Reason:", message.stop_reason)
        else:
            print(message.content) """
    
    result = await team.run(task="Who is Corrine Tellado?")
    print(result.messages[-2].content)


# Use asyncio.run when running in a script
if __name__ == "__main__":
    asyncio.run(assistant_run())