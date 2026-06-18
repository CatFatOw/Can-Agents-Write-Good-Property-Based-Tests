"""Routes for choosing which model API/key provider the app should use."""

from __future__ import annotations

import os

from fastapi import APIRouter, HTTPException, status

from schemas import ModelProviderResponse, ModelProviderSelection

router = APIRouter(prefix="/model-api", tags=["model api"])
api_router = APIRouter(prefix="/api", tags=["legacy model api"])


PROVIDERS: dict[str, dict[str, object]] = {
    "openai": {
        "id": "openai",
        "label": "GPT / OpenAI",
        "key_label": "OpenAI key",
        "key_placeholder": "sk-...",
        "default_model": os.environ.get("OPENAI_MODEL", "gpt-5.5"),
        "key_url": None,
        "requires_base_url": False,
        "openai_compatible": True,
    },
    "claude": {
        "id": "claude",
        "label": "Claude / Anthropic",
        "key_label": "Anthropic key",
        "key_placeholder": "sk-ant-...",
        "default_model": os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-6"),
        "key_url": "https://console.anthropic.com/settings/keys",
        "requires_base_url": False,
        "openai_compatible": False,
    },
    "cmu_gateway": {
        "id": "cmu_gateway",
        "label": "CMU AI Gateway",
        "key_label": "Gateway key",
        "key_placeholder": "Paste gateway key",
        "default_model": os.environ.get("CMU_AI_GATEWAY_MODEL") or os.environ.get("OPENAI_MODEL", "gpt-5.5"),
        "key_url": "https://ai-gateway.andrew.cmu.edu/ui/?page=api-keys",
        # The key UI URL is known, but the API base URL can vary by gateway setup.
        # Set CMU_AI_GATEWAY_BASE_URL or pass base_url in requests when using it.
        "requires_base_url": True,
        "openai_compatible": True,
    },
}


def provider_response(provider: dict[str, object]) -> ModelProviderResponse:
    """Shape plain provider metadata through a Pydantic response model."""
    return ModelProviderResponse(**provider)


@router.get("/providers", response_model=list[ModelProviderResponse])
async def get_model_providers():
    """Return provider options for the frontend dropdown."""
    return [provider_response(provider) for provider in PROVIDERS.values()]


@router.post("/selection", response_model=ModelProviderResponse)
async def select_model_provider(selection: ModelProviderSelection):
    """Validate a user's provider choice before generation requests use it."""
    provider = PROVIDERS.get(selection.provider)
    if provider is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unknown model provider: {selection.provider}",
        )
    return provider_response(provider)


@api_router.get("/model-providers", response_model=list[ModelProviderResponse])
async def get_legacy_model_providers():
    """Frontend-friendly alias that sits beside the existing /api routes."""
    return await get_model_providers()


@api_router.post("/model-selection", response_model=ModelProviderResponse)
async def select_legacy_model_provider(selection: ModelProviderSelection):
    """Frontend-friendly alias for provider validation."""
    return await select_model_provider(selection)
