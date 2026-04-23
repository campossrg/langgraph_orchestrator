from __future__ import annotations

import subprocess


class GitPublisher:
    def publish(self, target_path: str, branch_name: str | None = None) -> str:
        branch = branch_name or "feature/langgraph-orchestrated-change"
        subprocess.run(["git", "checkout", "-b", branch], cwd=target_path, check=False, capture_output=True, text=True)
        result = subprocess.run(["git", "push", "-u", "origin", branch], cwd=target_path, check=False, capture_output=True, text=True)
        if result.returncode != 0:
            return f"Git push failed: {result.stderr.strip() or result.stdout.strip()}"
        return f"Pushed branch {branch} to origin."
