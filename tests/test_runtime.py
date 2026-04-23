from langgraph_orchestrator.config.runtime import load_runtime_config


def test_runtime_config_defaults(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ORCHESTRATOR_MODEL_PROVIDER", raising=False)
    monkeypatch.delenv("ORCHESTRATOR_MODEL_NAME", raising=False)

    config = load_runtime_config()

    assert config.model_provider == "openai"
    assert config.model_name == "gpt-4o-mini"
    assert config.openai_api_key is None
