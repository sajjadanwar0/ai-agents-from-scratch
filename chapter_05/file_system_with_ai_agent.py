#%%
import asyncio
import sys
from pathlib import Path

from chapter_05.gaia_dataset import reset_workspace, problems_with_files, WORK_DIR
from scratch_agents.agents.agent import Agent

# Assuming your project root is two levels up from the notebook
project_root = Path.cwd().parent  # or adjust to the correct folder
sys.path.append(str(project_root))

# Now imports should work
from chapter_03.custom_tavily_mcp import search_web
from scratch_agents.models.llm_client import LlmClient
from chapter_05.read_media_file_tool import read_media_file
from chapter_05.read_file_tool import read_file
from chapter_05.list_file_tools import list_files
from chapter_05.unzip_files_tool import unzip_file

tools = [
    search_web,
    unzip_file,
    list_files,
    read_file,
    read_media_file,
]
agent = Agent(
    model=LlmClient(model="gpt-5"),
    tools=tools,
    instructions="You are a helpful assistant that can search the web and explore files to answer questions.",
    max_steps=20
)

# Reset workspace to clean state
reset_workspace()
# Select a problem with zip file attachment
zip_problems = [p for p in problems_with_files if
p['file_name'].endswith('.zip')]
problem = zip_problems[1]
file_path = WORK_DIR / problem['file_name']
# Construct prompt including file location
prompt = f"""{problem['Question']}
The attached file is located at: {file_path}
"""
print(prompt)

async def main():
    response = await agent.run(prompt)
    print(response)


asyncio.run(main())