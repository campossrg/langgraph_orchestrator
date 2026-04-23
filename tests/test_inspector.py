from pathlib import Path

from langgraph_orchestrator.adapters.filesystem import LocalWorkspaceInspector


def test_detects_jib_in_maven_project(tmp_path: Path) -> None:
    (tmp_path / "pom.xml").write_text("<artifactId>jib-maven-plugin</artifactId>", encoding="utf-8")

    inspector = LocalWorkspaceInspector()
    signals = inspector.inspect(str(tmp_path))

    assert signals.has_maven is True
    assert signals.has_jib is True
