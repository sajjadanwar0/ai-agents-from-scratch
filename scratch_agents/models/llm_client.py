import json
from typing import List, Optional

from litellm import acompletion

from scratch_agents.models.llm_request import LlmRequest
from scratch_agents.models.llm_response import LlmResponse
from scratch_agents.types.contents import Message, ToolCall, ToolResult


class LlmClient:
    """Client for LLM API calls using LiteLLM."""

    def __init__(self, model: str, **config):
        self.model = model
        self.config = config

    async def generate(self, request: LlmRequest) -> LlmResponse:
        """Generate a response from the LLM."""
        try:
            messages = self._build_messages(request)
            tools = (
                [tool.tool_definition for tool in request.tools]
                if request.tools
                else None
            )

            response = await acompletion(
                model=self.model,
                messages=messages,
                tools=tools,
                **({"tool_choice": request.tool_choice} if request.tool_choice else {}),
                **self.config,
            )

            return self._parse_response(response)

        except Exception as e:
            return LlmResponse(error_message=str(e))

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_messages(self, request: LlmRequest) -> List[dict]:
        """Convert LlmRequest to OpenAI/LiteLLM message format."""
        messages: List[dict] = []

        # System instructions
        for instruction in request.instructions:
            messages.append({
                "role": "system",
                "content": instruction,
            })

        # Conversation + tools
        for item in request.contents:
            if isinstance(item, Message):
                messages.append({
                    "role": item.role,
                    "content": item.content,
                })

            elif isinstance(item, ToolCall):
                tool_call_dict = {
                    "id": item.tool_call_id,
                    "type": "function",
                    "function": {
                        "name": item.name,
                        "arguments": json.dumps(item.arguments),
                    },
                }

                # Tool calls must be attached to an assistant message
                if messages and messages[-1]["role"] == "assistant":
                    messages[-1].setdefault("tool_calls", []).append(tool_call_dict)
                else:
                    messages.append({
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [tool_call_dict],
                    })

            elif isinstance(item, ToolResult):
                messages.append({
                    "role": "tool",
                    "tool_call_id": item.tool_call_id,
                    "content": (
                        str(item.content[0]) if item.content else ""
                    ),
                })

        return messages

    def _parse_response(self, response) -> LlmResponse:
        """Convert LiteLLM response to LlmResponse."""
        choice = response.choices[0]
        content_items = []

        # Normal assistant text
        if choice.message.content:
            content_items.append(
                Message(
                    role="assistant",
                    content=choice.message.content,
                )
            )

        # Tool calls
        if choice.message.tool_calls:
            for tc in choice.message.tool_calls:
                content_items.append(
                    ToolCall(
                        tool_call_id=tc.id,
                        name=tc.function.name,
                        arguments=json.loads(tc.function.arguments),
                    )
                )

        return LlmResponse(
            content=content_items,
            usage_metadata={
                "input_tokens": response.usage.prompt_tokens,
                "output_tokens": response.usage.completion_tokens,
            },
        )