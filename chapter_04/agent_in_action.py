import asyncio
import os
from typing import Literal, List

from pydantic import BaseModel

from chapter_04.LoadMCPTools import load_mcp_tools
from scratch_agents.agents.agent import Agent
from scratch_agents.models.llm_client import LlmClient


class SentimentAnalysis(BaseModel):
    sentiment: Literal["positive", "negative", "neutral"]
    confidence: float
    key_phrases: List[str]


async def main():
    tavily_connection = {
        "command": "npx",
        "args": ["-y", "tavily-mcp@latest"],
        "env": {"TAVILY_API_KEY": os.getenv("TAVILY_API_KEY")}
    }
    mcp_tools = await load_mcp_tools(tavily_connection)
    print(mcp_tools)

asyncio.run(main())