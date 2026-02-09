from abc import abstractmethod, ABC
from typing import Dict, Any

from chapter_04.agent_communication import ExecutionContext


class BaseTool(ABC):
    """Abstract base class for all tools."""

    def __init__(
            self,
            name: str = None,
            description: str = None,
            tool_definition: Dict[str, Any] = None,
    ):
        self.name = name or self.__class__.__name__
        self.description = description or self.__class__.__doc__ or ''
        self._tool_definition = tool_definition

    @property
    def tool_definition(self)->Dict[str, Any]|None:
        return self._tool_definition

    @abstractmethod
    async  def execute(self, context: ExecutionContext, **kwargs) -> Any:
        pass

    async def __call__(self, context: ExecutionContext, **kwargs) -> Any:
        return await self.execute(context, **kwargs)