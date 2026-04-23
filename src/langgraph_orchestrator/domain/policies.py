from __future__ import annotations

from langgraph_orchestrator.domain.models import AgentName


def select_agents(task: str) -> list[AgentName]:
    lowered = task.lower()
    agents = {AgentName.DEVELOPER, AgentName.ARCHITECT}

    if any(keyword in lowered for keyword in ["readme", "docs", "document", "changelog", "version"]):
        agents.add(AgentName.DOCUMENTER)

    return sorted(agents, key=lambda item: item.value)
