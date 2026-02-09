import inspect
from typing import Callable, Dict, Any

from docutils.nodes import description

from chapter_04.agent_communication import ExecutionContext
from scratch_agents.tools.base_tool import BaseTool
from scratch_agents.tools.schema_utils import function_to_input_schema, format_tool_definition


class FunctionTool(BaseTool):
    """Wraps a Python function as a BaseTool."""

    def __init__(
            self,
            func: Callable,
            name: str = None,
            description: str = None,
            tool_definition: Dict[str, Any] = None
    ):
        self.func = func
        self.needs_context = 'context' in inspect.signature(func).parameters

        name = name or func.__name__
        description = description or (func.__doc__ or '').strip()
        tool_definition = tool_definition or self._generate_definition()

        super().__init__(
            name=name,
            description=description,
            tool_definition=tool_definition
        )

    async def execute(self, context: ExecutionContext, **kwargs) -> Any:
        """Execute the wrapped function."""
        if self.needs_context:
            result = self.func(context=context, **kwargs)
        else:
            result = self.func(**kwargs)
        return result

    def _generate_definition(self) -> Dict[str, Any]:
        """Generate tool definition from function signature."""
        parameters = function_to_input_schema(self.func)

        return format_tool_definition(self.name, self.description, parameters)
