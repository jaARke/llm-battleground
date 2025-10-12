from typing import List

from fastapi import APIRouter

from ...core.shared.models import AIModel

router = APIRouter(prefix="/api/py/game", tags=["game"])

AVAILABLE_MODELS = [
    # Anthropic Models
    AIModel(internal_name="anthropic/claude-sonnet-4.5", display_name="Claude Sonnet 4.5"),
    AIModel(internal_name="anthropic/claude-sonnet-4", display_name="Claude Sonnet 4"),
    AIModel(internal_name="anthropic/claude-opus-4.1", display_name="Claude Opus 4.1"),
    AIModel(internal_name="anthropic/claude-opus-4", display_name="Claude Opus 4"),
    # OpenAI Models
    AIModel(internal_name="openai/gpt-5", display_name="GPT-5"),
    AIModel(internal_name="openai/gpt-5-mini", display_name="GPT-5 Mini"),
    AIModel(internal_name="openai/gpt-5-nano", display_name="GPT-5 Nano"),
    AIModel(internal_name="openai/gpt-4.1", display_name="GPT-4.1"),
    AIModel(internal_name="openai/gpt-4.1-mini", display_name="GPT-4.1 Mini"),
    AIModel(internal_name="openai/gpt-4o", display_name="GPT-4o"),
    AIModel(internal_name="openai/gpt-4o-mini", display_name="GPT-4o Mini"),
    # Google Models
    AIModel(internal_name="google/gemini-2.5-pro", display_name="Gemini 2.5 Pro"),
    AIModel(internal_name="google/gemini-2.5-flash", display_name="Gemini 2.5 Flash"),
    AIModel(internal_name="google/gemini-2.5-flash-lite", display_name="Gemini 2.5 Flash Lite"),
    AIModel(internal_name="google/gemini-2.0-flash", display_name="Gemini 2.0 Flash"),
    AIModel(internal_name="google/gemini-2.0-flash-lite", display_name="Gemini 2.0 Flash Lite"),
    # XAI Models
    AIModel(internal_name="xai/grok-4", display_name="Grok 4"),
    AIModel(internal_name="xai/grok-4-fast-reasoning", display_name="Grok 4 Fast Reasoning"),
    AIModel(
        internal_name="xai/grok-4-fast-non-reasoning", display_name="Grok 4 Fast Non-Reasoning"
    ),
    AIModel(internal_name="xai/grok-3", display_name="Grok 3"),
    AIModel(internal_name="xai/grok-3-fast", display_name="Grok 3 Fast"),
    AIModel(internal_name="xai/grok-3-mini", display_name="Grok 3 Mini"),
    AIModel(internal_name="xai/grok-3-mini-fast", display_name="Grok 3 Mini Fast"),
]


@router.get("/available_models")
async def get_available_models() -> List[AIModel]:
    return AVAILABLE_MODELS
