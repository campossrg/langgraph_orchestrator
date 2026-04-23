from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class AgentName(str, Enum):
    DEVELOPER = "developer"
    DOCUMENTER = "documenter"
    ARCHITECT = "architect"


class AgentResult(BaseModel):
    agent: AgentName
    status: Literal["completed", "needs_changes", "skipped"]
    summary: str
    details: list[str] = Field(default_factory=list)


class PublishDecision(BaseModel):
    approved: bool = False
    reason: str = ""


class OrchestratorState(BaseModel):
    task: str
    target_path: str
    requested_agents: list[AgentName] = Field(default_factory=list)
    results: list[AgentResult] = Field(default_factory=list)
    publish: bool = False
    publish_decision: PublishDecision = Field(default_factory=PublishDecision)


class ProjectSignals(BaseModel):
    has_maven: bool = False
    has_gradle: bool = False
    has_jib: bool = False
    has_readme: bool = False
    has_changelog: bool = False
    has_obsidian_docs: bool = False
