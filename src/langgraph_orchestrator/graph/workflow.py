from __future__ import annotations

from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from langgraph_orchestrator.adapters.filesystem import LocalWorkspaceInspector
from langgraph_orchestrator.adapters.git import GitPublisher
from langgraph_orchestrator.adapters.llm import LlmClient
from langgraph_orchestrator.agents.architect import ArchitectAgent
from langgraph_orchestrator.agents.developer import DeveloperAgent
from langgraph_orchestrator.agents.documenter import DocumenterAgent
from langgraph_orchestrator.application.services import decide_publication, publish_if_approved
from langgraph_orchestrator.application.workspace import TargetWorkspaceService
from langgraph_orchestrator.config.runtime import RuntimeConfig, load_runtime_config
from langgraph_orchestrator.domain.models import AgentName, AgentResult
from langgraph_orchestrator.domain.policies import select_agents


class WorkflowState(TypedDict, total=False):
    task: str
    target_path: str
    publish: bool
    requested_agents: list[str]
    signals: dict
    results: list[dict]
    publish_decision: dict
    publish_result: str


def build_workflow():
    config = load_runtime_config()
    inspector = LocalWorkspaceInspector()
    workspace = TargetWorkspaceService()
    llm = LlmClient(config)
    developer = DeveloperAgent(workspace=workspace, llm=llm)
    documenter = DocumenterAgent(workspace=workspace, llm=llm)
    architect = ArchitectAgent(workspace=workspace, llm=llm)
    publisher = GitPublisher()

    def intake(state: WorkflowState) -> WorkflowState:
        requested = [agent.value for agent in select_agents(state["task"])]
        signals = inspector.inspect(state["target_path"]).model_dump()
        return {**state, "requested_agents": requested, "signals": signals, "results": []}

    def run_developer(state: WorkflowState) -> WorkflowState:
        if AgentName.DEVELOPER.value not in state["requested_agents"]:
            return state
        result = developer.run(state["task"], state["target_path"], inspector.inspect(state["target_path"]))
        return {**state, "results": [*state.get("results", []), result.model_dump()]}

    def run_documenter(state: WorkflowState) -> WorkflowState:
        if AgentName.DOCUMENTER.value not in state["requested_agents"]:
            return state
        result = documenter.run(state["task"], state["target_path"], inspector.inspect(state["target_path"]))
        return {**state, "results": [*state.get("results", []), result.model_dump()]}

    def run_architect(state: WorkflowState) -> WorkflowState:
        result = architect.run(state["task"], state["target_path"], inspector.inspect(state["target_path"]))
        next_state = {**state, "results": [*state.get("results", []), result.model_dump()]}
        decision = decide_publication(result.status, result.summary, state.get("publish", False))
        next_state["publish_decision"] = decision.model_dump()
        return next_state

    def maybe_publish(state: WorkflowState) -> WorkflowState:
        decision = state.get("publish_decision", {})
        publish_result = publish_if_approved(
            publisher,
            state["target_path"],
            decide_publication(
                architect_status=_architect_result(state).status,
                architect_summary=_architect_result(state).summary,
                publish_requested=state.get("publish", False),
            ),
        )
        return {**state, "publish_decision": decision, "publish_result": publish_result}

    def should_publish(state: WorkflowState) -> str:
        decision = state.get("publish_decision", {})
        return "publish" if decision.get("approved") else "skip"

    graph = StateGraph(WorkflowState)
    graph.add_node("intake", intake)
    graph.add_node("developer", run_developer)
    graph.add_node("documenter", run_documenter)
    graph.add_node("architect", run_architect)
    graph.add_node("publish", maybe_publish)
    graph.add_edge(START, "intake")
    graph.add_edge("intake", "developer")
    graph.add_edge("developer", "documenter")
    graph.add_edge("documenter", "architect")
    graph.add_conditional_edges("architect", should_publish, {"publish": "publish", "skip": END})
    graph.add_edge("publish", END)
    return graph.compile()


def _architect_result(state: WorkflowState) -> AgentResult:
    for result in reversed(state.get("results", [])):
        if result["agent"] == AgentName.ARCHITECT.value:
            return AgentResult.model_validate(result)
    raise ValueError("Architect result missing from workflow state.")
