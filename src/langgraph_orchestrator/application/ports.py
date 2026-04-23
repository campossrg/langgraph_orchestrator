from __future__ import annotations

from typing import Protocol

from langgraph_orchestrator.domain.models import AgentResult, ProjectSignals


class WorkspaceInspector(Protocol):
    def inspect(self, target_path: str) -> ProjectSignals: ...


class Publisher(Protocol):
    def publish(self, target_path: str, branch_name: str | None = None) -> str: ...


class AgentRunner(Protocol):
    def run(self, task: str, target_path: str, signals: ProjectSignals) -> AgentResult: ...
