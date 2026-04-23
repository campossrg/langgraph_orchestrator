from __future__ import annotations

import subprocess
from pathlib import Path


class TargetWorkspaceService:
    def summarize_tree(self, target_path: str) -> list[str]:
        root = Path(target_path)
        if not root.exists():
            return [f"Target path does not exist: {target_path}"]

        entries = sorted(child.name for child in root.iterdir())
        preview = entries[:15]
        if len(entries) > 15:
            preview.append(f"... and {len(entries) - 15} more")
        return preview

    def run_command(self, target_path: str, command: list[str]) -> str:
        result = subprocess.run(command, cwd=target_path, check=False, capture_output=True, text=True)
        output = (result.stdout or result.stderr).strip()
        return output or f"Command finished with exit code {result.returncode}."

    def ensure_file(self, target_path: str, relative_path: str, content: str) -> str:
        file_path = Path(target_path) / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        if not file_path.exists():
            file_path.write_text(content, encoding="utf-8")
            return f"Created {relative_path}."
        return f"Kept existing {relative_path}."

    def bump_version_file(self, target_path: str) -> str:
        version_file = Path(target_path) / "VERSION"
        current = "0.1.0"
        if version_file.exists():
            current = version_file.read_text(encoding="utf-8").strip() or current

        parts = current.split(".")
        if len(parts) != 3 or not all(part.isdigit() for part in parts):
            next_version = "0.1.0"
        else:
            major, minor, patch = [int(part) for part in parts]
            next_version = f"{major}.{minor}.{patch + 1}"

        version_file.write_text(next_version, encoding="utf-8")
        return next_version
