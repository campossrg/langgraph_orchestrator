from __future__ import annotations

from langgraph_orchestrator.adapters.llm import LlmClient
from langgraph_orchestrator.application.workspace import TargetWorkspaceService
from langgraph_orchestrator.domain.models import AgentName, AgentResult, ProjectSignals


class ArchitectAgent:
    def __init__(self, workspace: TargetWorkspaceService, llm: LlmClient | None = None) -> None:
        self._workspace = workspace
        self._llm = llm

    def run(self, task: str, target_path: str, signals: ProjectSignals) -> AgentResult:
        tree_preview = self._workspace.summarize_tree(target_path)
        details = [
            f"Task: {task}",
            "Architect lane reviews ports-and-adapters separation before publication.",
            f"Maven detected: {signals.has_maven}",
            f"Gradle detected: {signals.has_gradle}",
            f"JIB configuration detected: {signals.has_jib}",
            f"Workspace preview: {', '.join(tree_preview)}",
        ]

        if self._llm and self._llm.enabled:
            details.append(
                self._llm.ask(
                    "You are a software architect focused on hexagonal architecture. Review the target workspace signals and provide concise approval guidance.",
                    f"Task: {task}\nTarget path: {target_path}\nSignals: {signals.model_dump_json()}\nWorkspace preview: {tree_preview}",
                )
            )

        if not (signals.has_maven or signals.has_gradle):
            return AgentResult(
                agent=AgentName.ARCHITECT,
                status="needs_changes",
                summary="Architect could not verify backend architecture because no Java build files were detected.",
                details=details,
            )

        return AgentResult(
            agent=AgentName.ARCHITECT,
            status="completed",
            summary="Architect review passed initial workspace checks for a Java backend target.",
            details=details,
        )
