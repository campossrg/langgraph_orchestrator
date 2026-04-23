from __future__ import annotations

from langgraph_orchestrator.application.ports import Publisher
from langgraph_orchestrator.domain.models import PublishDecision


def decide_publication(architect_status: str, architect_summary: str, publish_requested: bool) -> PublishDecision:
    if not publish_requested:
        return PublishDecision(approved=False, reason="Publish not requested.")
    if architect_status != "completed":
        return PublishDecision(approved=False, reason=architect_summary)
    return PublishDecision(approved=True, reason="Architect approved publication.")


def publish_if_approved(publisher: Publisher, target_path: str, decision: PublishDecision) -> str:
    if not decision.approved:
        return f"Publish skipped: {decision.reason}"
    return publisher.publish(target_path)
