from __future__ import annotations

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import SecretStr

from langgraph_orchestrator.config.runtime import RuntimeConfig


class LlmClient:
    def __init__(self, config: RuntimeConfig) -> None:
        self._config = config
        self._model = self._build_model(config)

    @property
    def enabled(self) -> bool:
        return self._model is not None

    def ask(self, system_prompt: str, user_prompt: str) -> str:
        if self._model is None:
            raise RuntimeError("LLM client is not configured.")

        response = self._model.invoke(
            [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt),
            ]
        )
        content = response.content
        if isinstance(content, str):
            return content
        return str(content)

    def _build_model(self, config: RuntimeConfig) -> BaseChatModel | None:
        provider = config.model_provider.lower()

        if provider == "openai" and config.openai_api_key:
            from langchain_openai import ChatOpenAI

            return ChatOpenAI(model=config.model_name, api_key=config.openai_api_key.get_secret_value(), temperature=0)

        if provider == "anthropic" and config.anthropic_api_key:
            from langchain_anthropic import ChatAnthropic

            return ChatAnthropic(model=config.model_name, api_key=config.anthropic_api_key.get_secret_value(), temperature=0)

        return None
