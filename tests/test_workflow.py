from pathlib import Path

from langgraph_orchestrator.graph.workflow import build_workflow


def test_workflow_runs_architect_review_for_java_backend(tmp_path: Path) -> None:
    (tmp_path / "pom.xml").write_text("<project></project>", encoding="utf-8")

    workflow = build_workflow()
    result = workflow.invoke(
        {
            "task": "Implement endpoint and update changelog",
            "target_path": str(tmp_path),
            "publish": False,
        }
    )

    assert len(result["results"]) == 3
    assert result["results"][-1]["agent"] == "architect"
    assert result["publish_decision"]["approved"] is False
