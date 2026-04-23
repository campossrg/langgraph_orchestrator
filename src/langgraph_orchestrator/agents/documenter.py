from __future__ import annotations

from langgraph_orchestrator.adapters.llm import LlmClient
from langgraph_orchestrator.application.workspace import TargetWorkspaceService
from langgraph_orchestrator.domain.models import AgentName, AgentResult, ProjectSignals


class DocumenterAgent:
    def __init__(self, workspace: TargetWorkspaceService, llm: LlmClient | None = None) -> None:
        self._workspace = workspace
        self._llm = llm

    def run(self, task: str, target_path: str, signals: ProjectSignals) -> AgentResult:
        readme_result = self._workspace.ensure_file(
            target_path,
            "README.md",
            "# Project\n\nThis README was initialized by the orchestrator documenter lane.\n",
        )
        changelog_result = self._workspace.ensure_file(
            target_path,
            "CHANGELOG.md",
            "# Changelog\n\n## Unreleased\n\n- Initialized by the orchestrator.\n",
        )
        obsidian_result = self._workspace.ensure_file(
            target_path,
            "docs/obsidian/notes.md",
            "# Notes\n\nInitialized by the orchestrator documenter lane.\n",
        )
        version = self._workspace.bump_version_file(target_path)

        details = [
            f"Task: {task}",
            f"README present: {signals.has_readme}",
            f"CHANGELOG present: {signals.has_changelog}",
            f"Obsidian docs present: {signals.has_obsidian_docs}",
            readme_result,
            changelog_result,
            obsidian_result,
            f"Version updated to: {version}",
            "Documenter lane is responsible for README, changelog, docs, and version updates in the target workspace.",
        ]

        if self._llm and self._llm.enabled:
            details.append(
                self._llm.ask(
                    "You are a technical documentation agent. Produce concise documentation follow-up guidance for the requested task.",
                    f"Task: {task}\nTarget path: {target_path}\nSignals: {signals.model_dump_json()}\nVersion: {version}",
                )
            )

        return AgentResult(
            agent=AgentName.DOCUMENTER,
            status="completed",
            summary=f"Documenter lane prepared documentation updates for {target_path}.",
            details=details,
        )
