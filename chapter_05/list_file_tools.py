from pathlib import Path


def list_files(path: str = '.') -> str:
    """List files and directories in the given path"""

    path = Path(path)

    if not path.exists():
        return f"Path {path} does not exist"

    if not path.is_dir():
        return f"Path {path} is not a directory"

    items = []

    for item in sorted(path.iterdir()):
        if item.name.startswith("."):
            continue
        if item.is_dir():
            items.append(f"{item.name}/")
        else:
            items.append(f"{item.name}")
    # Sort directories first
    dirs = [i for i in items if i.endswith('/')]
    files = [i for i in items if not i.endsWith('/')]

    result = f"Directory: {path}\n"

    for item in dirs + files:
        result += f"{item}\n"

    return result
