#%%
from datasets import load_dataset
from huggingface_hub import snapshot_download
from pathlib import Path
import shutil

dataset = load_dataset("gaia-benchmark/GAIA", "2023_all", split="validation")
NOTEBOOK_DIR = Path.cwd()
PROJECT_ROOT = NOTEBOOK_DIR.parent
CACHE_DIR = PROJECT_ROOT / "gaia_cache"


snapshot_download(
    repo_id="gaia-benchmark/GAIA",
    repo_type="dataset",
    allow_patterns="2023/validation/*",
    local_dir=CACHE_DIR,
)


WORK_DIR = NOTEBOOK_DIR / "gaia_workspace"


def reset_workspace():
    """Restore the workspace to its initial state."""
    shutil.rmtree(WORK_DIR, ignore_errors=True)
    shutil.copytree(CACHE_DIR, "2023/validation", dirs_exist_ok=True)
    print(f"Workspace reset:  {WORK_DIR}")

reset_workspace()


problems_with_files = [p for p in dataset if p.get("file_name")]
problem_with_zip = [p for p in problems_with_files if p['file_name'].endswith(".zip")]

print(f"Total problems: {len(dataset)}")
print(f"Problems with attachments: {len(problems_with_files)}")
print(f"Total problems with zip files: {len(problem_with_zip)}")

problem = problem_with_zip[0]
print(f"Question: {problem['Question'][:100]}")
print(f"File Name: {problem['file_name']}")

file_path = WORK_DIR / problem["file_name"]
print(f"File exists: {file_path.exists()}")
#%% md
