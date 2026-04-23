from __future__ import annotations

import os

from dotenv import load_dotenv
from pydantic import BaseModel, SecretStr


class RuntimeConfig(BaseModel):
    model_provider: str = "openai"
    model_name: str = "provider-configured-model"
    max_review_loops: int = 1
    openai_api_key: SecretStr | None = None
    anthropic_api_key: SecretStr | None = None


def load_runtime_config() -> RuntimeConfig:
    load_dotenv()
    return RuntimeConfig(
        model_provider=os.getenv("ORCHESTRATOR_MODEL_PROVIDER", "openai"),
        model_name=os.getenv("ORCHESTRATOR_MODEL_NAME", "gpt-4o-mini"),
        max_review_loops=int(os.getenv("ORCHESTRATOR_MAX_REVIEW_LOOPS", "1")),
        openai_api_key=SecretStr(value) if (value := os.getenv("OPENAI_API_KEY")) else None,
        anthropic_api_key=SecretStr(value) if (value := os.getenv("ANTHROPIC_API_KEY")) else None,
    )
