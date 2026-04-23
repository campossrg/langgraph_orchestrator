from __future__ import annotations

from langgraph_orchestrator.adapters.llm import LlmClient
from langgraph_orchestrator.application.workspace import TargetWorkspaceService
from langgraph_orchestrator.domain.models import AgentName, AgentResult, ProjectSignals


class DeveloperAgent:
    def __init__(self, workspace: TargetWorkspaceService, llm: LlmClient | None = None) -> None:
        self._workspace = workspace
        self._llm = llm

    def run(self, task: str, target_path: str, signals: ProjectSignals) -> AgentResult:
        java_hint = "Java backend detected." if signals.has_maven or signals.has_gradle else "No Java build detected."
        tree_preview = self._workspace.summarize_tree(target_path)
        details = [
            f"Task: {task}",
            java_hint,
            f"Workspace preview: {', '.join(tree_preview)}",
            "This scaffold leaves concrete code-editing tooling pluggable so the orchestrator can be pointed at external workspaces.",
        ]

        if self._llm and self._llm.enabled:
            details.append(
                self._llm.ask(
                    "You are a software developer agent. Produce concise implementation guidance for the requested task over the given target workspace.",
                    f"Task: {task}\nTarget path: {target_path}\nSignals: {signals.model_dump_json()}\nWorkspace preview: {tree_preview}",
                )
            )

        return AgentResult(
            agent=AgentName.DEVELOPER,
            status="completed",
            summary=f"Developer lane prepared implementation guidance for {target_path}.",
            details=details,
        )
