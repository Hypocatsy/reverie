from backend.config import settings
from backend.providers.base import LLMProvider, ImageProvider
from backend.providers.llm.openai_provider import OpenAIProvider
from backend.providers.llm.pollinations_provider import PollinationsLLMProvider
from backend.providers.image.openai_provider import OpenAIImageProvider
from backend.providers.image.pollinations_provider import PollinationsImageProvider
from backend.providers.image.gemini_provider import GeminiImageProvider

_llm_cache: dict[str, LLMProvider] = {}
_image_cache: dict[str, ImageProvider] = {}


def get_llm_provider() -> LLMProvider:
    """Return the active LLM provider based on config (cached)."""
    name = settings.llm_provider
    if name not in _llm_cache:
        factories: dict[str, type[LLMProvider]] = {
            "openai": OpenAIProvider,
            "pollinations": PollinationsLLMProvider,
        }
        if name not in factories:
            raise ValueError(f"Unknown LLM provider: {name}")
        _llm_cache[name] = factories[name]()
    return _llm_cache[name]


def get_image_provider() -> ImageProvider:
    """Return the active image provider based on config (cached)."""
    name = settings.image_provider
    if name not in _image_cache:
        factories: dict[str, type[ImageProvider]] = {
            "openai": OpenAIImageProvider,
            "pollinations": PollinationsImageProvider,
            "gemini": GeminiImageProvider,
        }
        if name not in factories:
            raise ValueError(f"Unknown image provider: {name}")
        _image_cache[name] = factories[name]()
    return _image_cache[name]
