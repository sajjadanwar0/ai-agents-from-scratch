from typing import List, Optional, Type

from pydantic import BaseModel

from scratch_agents.models.llm_client import LlmClient
from scratch_agents.tools.base_tool import BaseTool
from scratch_agents.tools.decorator import tool


class Agent:
    def __init__(
            self,
            model: LlmClient,
            tools: List[BaseTool] = None,
            instructions: str = "",
            max_steps: int = 10,
            output_type: Optional[Type[BaseModel]] = None,  # New parameter
    ):
        self.model = model
        self.instructions = instructions
        self.max_steps = max_steps
        self.output_type = output_type
        self.output_tool_name = None  # Will be set if output_type provided
        self.tools = self._setup_tools(tools or [])

    def _setup_tools(self, tools: List[BaseTool]) -> List[BaseTool]:
        if self.output_type is not None:
            @tool(
                name="final_answer",
                description="Return the final structured answer matching the required schema."
            )
            def final_answer(output: self.output_type) -> self.output_type:
                return output

            tools = list(tools)  # Create a copy to avoid modifying the original
            tools.append(final_answer)
            self.output_tool_name = "final_answer"
        return tools

    def run(self, prompt: str) -> Any:
        """
        Simple run method: sends instructions + prompt to the LLM model.
        """
        full_prompt = f"{self.instructions}\n\n{prompt}"
        return self.model(full_prompt)