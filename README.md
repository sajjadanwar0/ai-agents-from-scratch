# 🤖 AI Agents From Scratch

Build AI agents from first principles using Python — no heavyweight frameworks, just clean abstractions over the OpenAI API.

This repository walks you through building a fully functional AI agent system step by step, covering everything from basic LLM calls to tool-calling agents with memory, sessions, and structured output. Each chapter introduces a new concept with working code you can run immediately.

## Why This Repo?

Most agent tutorials either hand-wave with pseudocode or throw you into LangChain/CrewAI without explaining what's happening underneath. This repo takes a different approach: you build the primitives yourself — the LLM wrapper, tool system, agent loop, memory strategies, and session management — so you actually understand what frameworks are doing under the hood.

## Repository Structure

```
ai-agents-from-scratch/
├── chapter_02/                    # Getting started with LLMs
│   └── getting_started.ipynb      # Basic OpenAI API usage
├── chapter_03/                    # Tools & MCP
│   ├── tools.ipynb                # Tool creation and usage
│   └── custom_tavily_mcp.py       # Custom MCP server with Tavily search
├── chapter_04/                    # Building the agent
│   ├── basic_agent.ipynb          # Agent notebook walkthrough
│   ├── BaseTool.py                # Abstract tool interface
│   ├── FunctionTool.py            # Function-based tool wrapper
│   ├── LoadMCPTools.py            # MCP tool loader
│   ├── agent_communication.py     # Agent communication patterns
│   ├── agent_in_action.py         # Running agents end-to-end
│   └── gaia_benchmark.py          # GAIA benchmark evaluation
├── chapter_05/                    # Advanced capabilities
│   ├── file_system_with_ai_agent.py  # File system agent
│   ├── gaia_dataset.py            # GAIA dataset loader
│   ├── get_embedding.ipynb        # Embeddings walkthrough
│   ├── list_file_tools.py         # File listing tool
│   ├── read_file_tool.py          # File reading tool
│   ├── read_media_file_tool.py    # Media file reading tool
│   └── unzip_files_tool.py        # Zip extraction tool
├── scratch_agents/                # Core framework library
│   ├── agents/                    # Agent implementations
│   │   ├── agent.py               # Simple agent class
│   │   ├── agent_result.py        # Agent result container
│   │   ├── tool_calling_agent_ch4_base.py       # Base tool-calling agent
│   │   ├── tool_calling_agent_ch4_callback.py   # Agent with callbacks
│   │   ├── tool_calling_agent_ch4_structured_output.py  # Structured output agent
│   │   ├── tool_calling_agent_ch6.py            # Full-featured agent
│   │   ├── execution_context_ch4.py  # Ch4 execution context
│   │   └── execution_context_ch6.py  # Ch6 execution context
│   ├── models/                    # LLM abstraction layer
│   │   ├── base_llm.py            # Abstract LLM interface
│   │   ├── llm_client.py          # LLM client wrapper
│   │   ├── llm_communication_layer.py  # Communication layer
│   │   ├── llm_request.py         # Request model
│   │   ├── llm_response.py        # Response model
│   │   └── openai.py              # OpenAI implementation
│   ├── tools/                     # Tool system
│   │   ├── base_tool.py           # Abstract tool with schema generation
│   │   ├── function_tool.py       # Wraps plain functions as tools
│   │   ├── decorator.py           # @tool decorator
│   │   ├── schema_utils.py        # JSON schema utilities
│   │   ├── calculator.py          # Calculator tool
│   │   ├── search_web.py          # Web search tool
│   │   ├── wikipedia.py           # Wikipedia lookup tool
│   │   ├── conversation_search.py # Conversation memory search
│   │   └── core_memory_upsert.py  # Core memory update tool
│   ├── memory/                    # Memory strategies
│   │   ├── base_memory_strategy.py     # Abstract memory strategy
│   │   ├── sliding_window_strategy.py  # Keep last N messages
│   │   ├── core_memory_strategy.py     # Persona + user info injection
│   │   └── summarization_strategy.py   # Summarize older messages
│   ├── sessions/                  # Session management
│   │   ├── session.py             # Session container (events, state, core memory)
│   │   ├── base_session_manager.py      # Session manager interface
│   │   ├── in_memory_session_manager.py # In-memory implementation
│   │   ├── base_cross_session_manager.py   # Cross-session interface
│   │   ├── task_cross_session_manager.py   # Task-based cross-session
│   │   └── user_cross_session_manager.py   # User-based cross-session
│   └── types/                     # Core data types
│       ├── contents.py            # Message, ToolCall, ToolResult
│       └── events.py              # Event system
├── .env.example
├── requirements.txt
└── .gitignore
```

## Chapters

### Chapter 2 — Getting Started
Introduction to calling LLMs with the OpenAI API. Covers basic prompt construction, API configuration, and handling responses.

### Chapter 3 — Tools
Learn how to give agents capabilities by defining tools. Build custom tools including a Tavily-powered MCP search server, and understand how tool definitions (JSON schemas) are passed to LLMs for function calling.

### Chapter 4 — Building the Agent
The core of the repo. Build a tool-calling agent from scratch with the Think → Act → Observe loop:

1. **Think** — send the conversation to the LLM and get a response
2. **Act** — execute any tool calls the LLM requests
3. **Observe** — feed tool results back and repeat

This chapter progressively builds from a basic agent to ones with callbacks, structured output via a `final_answer` tool pattern, and GAIA benchmark evaluation.

### Chapter 5 — Advanced Capabilities
Extend the agent with file system tools (list, read, unzip, media reading), embeddings for semantic search, and dataset evaluation using the GAIA benchmark.

## Core Concepts

### Agent Architecture
```
User Input
    ↓
┌─────────────────────────┐
│       Agent Loop         │
│  ┌───────────────────┐  │
│  │  Think (LLM call) │──┼──→ If text response → Return to user
│  └───────┬───────────┘  │
│          ↓ tool calls   │
│  ┌───────────────────┐  │
│  │  Act (run tools)  │  │
│  └───────┬───────────┘  │
│          ↓ results      │
│  ┌───────────────────┐  │
│  │ Observe (feedback) │──┼──→ Loop back to Think
│  └───────────────────┘  │
└─────────────────────────┘
```

### Tool System
Tools are defined as classes extending `BaseTool` or as decorated functions using `@tool`. Each tool auto-generates an OpenAI-compatible JSON schema from its Pydantic model or function signature, so the LLM knows how to call it.

### Memory Strategies
Memory is implemented as composable `before_llm_callbacks` that modify the LLM request before it's sent:

- **Sliding Window** — keeps only the last N messages to stay within context limits
- **Core Memory** — injects persistent persona/user info into every request
- **Summarization** — compresses older messages into summaries

### Session Management
Sessions track conversation state, events, and core memory per user. Cross-session managers enable sharing context across conversations (by user or by task).

## Getting Started

### Prerequisites
- Python 3.11+
- An OpenAI API key
- (Optional) Tavily API key for web search, Anthropic API key, HuggingFace token

### Installation

```bash
git clone https://github.com/sajjadanwar0/ai-agents-from-scratch.git
cd ai-agents-from-scratch

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your API keys:
#   OPENAI_API_KEY=sk-...
#   TAVILY_API_KEY=tvly-...    (optional)
#   ANTHROPIC_API_KEY=sk-...   (optional)
#   HF_TOKEN=hf_...            (optional)
```

### Quick Start

Start with the notebooks in order:

```bash
jupyter notebook chapter_02/getting_started.ipynb
```

Or use the agent directly in code:

```python
from scratch_agents.models.openai import OpenAILlm
from scratch_agents.agents.tool_calling_agent_ch4_base import ToolCallingAgent
from scratch_agents.tools.calculator import Calculator
from scratch_agents.tools.search_web import SearchWeb

# Initialize the LLM
model = OpenAILlm(model="gpt-4o-mini")

# Create an agent with tools
agent = ToolCallingAgent(
    name="assistant",
    model=model,
    tools=[Calculator(), SearchWeb()],
    instructions="You are a helpful assistant. Use tools when needed.",
    max_steps=10,
)

# Run the agent
result = await agent.run("What is 42 * 17 and who is the president of France?")
```

## Key Dependencies

| Package | Purpose |
|---------|---------|
| `openai` | LLM API client |
| `pydantic` | Data validation & schema generation |
| `python-dotenv` | Environment variable management |

