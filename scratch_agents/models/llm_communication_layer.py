import asyncio

from scratch_agents.models.llm_client import LlmClient
from scratch_agents.models.llm_request import LlmRequest
from scratch_agents.types.contents import Message

async def main():
    client = LlmClient(model="gpt-5-mini")

    request = LlmRequest(
        instructions=["You are a helpful assistant"],
        contents=[Message(role="user", content="What is 2 + 2?")],
    )

    response = await client.generate(request)

    for item in response.content:
        if isinstance(item, Message):
            print(item.content)

asyncio.run(main())