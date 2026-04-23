from __future__ import annotations

import json
from pathlib import Path

import typer

from langgraph_orchestrator.graph.workflow import build_workflow

app = typer.Typer(help="LangGraph orchestrator for external project workspaces.")


@app.command()
def run(task: str, target_path: str, publish: bool = False) -> None:
    workflow = build_workflow()
    result = workflow.invoke({"task": task, "target_path": str(Path(target_path).resolve()), "publish": publish})
    typer.echo(json.dumps(result, indent=2))


@app.command()
def review(task: str, target_path: str) -> None:
    workflow = build_workflow()
    result = workflow.invoke({"task": task, "target_path": str(Path(target_path).resolve()), "publish": False})
    typer.echo(json.dumps(result, indent=2))
