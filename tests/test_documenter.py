from pathlib import Path

from langgraph_orchestrator.agents.documenter import DocumenterAgent
from langgraph_orchestrator.application.workspace import TargetWorkspaceService
from langgraph_orchestrator.domain.models import ProjectSignals


def test_documenter_creates_docs_and_version(tmp_path: Path) -> None:
    agent = DocumenterAgent(workspace=TargetWorkspaceService())
    signals = ProjectSignals()

    result = agent.run("Update docs", str(tmp_path), signals)

    assert result.status == "completed"
    assert (tmp_path / "README.md").exists()
    assert (tmp_path / "CHANGELOG.md").exists()
    assert (tmp_path / "docs" / "obsidian" / "notes.md").exists()
    assert (tmp_path / "VERSION").read_text(encoding="utf-8").strip() == "0.1.1"
