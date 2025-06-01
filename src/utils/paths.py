from pathlib import Path


def find_project_root(
    current_path: Path,
    marker_names=('pyproject.toml',)
) -> Path:
    for parent in current_path.resolve().parents:
        if any((parent / marker).exists() for marker in marker_names):
            return parent
    raise RuntimeError("Could not find project root.")

def get_output_path(filename: str) -> Path:
    project_root = find_project_root(Path(__file__))
    return project_root / "data" / "output" /filename