from langgraph_orchestrator.domain.models import AgentName
from langgraph_orchestrator.domain.policies import select_agents


def test_select_agents_includes_documenter_for_docs_work() -> None:
    agents = select_agents("Update README and changelog")
    assert AgentName.DOCUMENTER in agents
    assert AgentName.ARCHITECT in agents
    assert AgentName.DEVELOPER in agents


def test_select_agents_defaults_to_developer_and_architect() -> None:
    agents = select_agents("Implement payment service")
    assert agents == [AgentName.ARCHITECT, AgentName.DEVELOPER]
