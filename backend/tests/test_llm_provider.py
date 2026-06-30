from app.services.llm_provider import (
    LocalTemplateProvider,
    get_llm_provider,
)


def test_local_template_provider_returns_prompt_unchanged() -> None:
    provider = LocalTemplateProvider()
    assert provider.provider_name == "local-template"
    assert provider.generate("hello world") == "hello world"


def test_get_llm_provider_defaults_to_local_template() -> None:
    provider = get_llm_provider()
    assert isinstance(provider, LocalTemplateProvider)
    assert provider.provider_name == "local-template"


def test_get_llm_provider_returns_local_template_for_unknown() -> None:
    provider = get_llm_provider(provider="unknown-provider")
    assert isinstance(provider, LocalTemplateProvider)


def test_get_llm_provider_falls_back_when_no_api_key() -> None:
    provider = get_llm_provider(provider="openai", openai_api_key=None)
    assert provider.provider_name == "openai/gpt-4o-mini"
    result = provider.generate("test")
    assert "[OpenAI unavailable" in result or "test" in result
