from dataclasses import dataclass

from pydantic import BaseModel

from scratch_agents.agents.execution_context_ch4 import ExecutionContext


@dataclass
class AgentResult:
    """Result of an agent execution"""
    output: str | BaseModel
    context: ExecutionContext | None = None

