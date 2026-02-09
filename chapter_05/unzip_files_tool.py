import zipfile
from os import mkdir
from pathlib import Path

from dill.pointers import parent


def unzip_file(zip_path: str, extract_to: str = None) -> str:
    """Extract zip archive to extract dir"""
    zip_path = Path(zip_path)

    if not zip_path.exists():
        return f"file {zip_path} does not exist"

    # Default extraction path: create folder with zip filename
    if extract_to is None:
        extract_to = zip_path.parent / zip_path.stem
    else:
        extract_to = Path(extract_to)

    extract_to.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        file_list = zip_ref.namelist()
        zip_ref.extractall(extract_to)

    # Format Results
    result = f"Extracted {len(file_list)} files to {extract_to}/\n\n"

    result += "Contents:\n"
    for f in file_list[:20]:
        result += f" - {f}\n"
        if len(file_list) > 20:
            result += f" ... and {len(file_list) - 20} more files\n"
    return result