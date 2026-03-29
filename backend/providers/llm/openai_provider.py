import logging
from openai import AsyncOpenAI
from backend.config import settings
from backend.models.schemas import SongInput
from backend.providers.base import LLMProvider, ProviderError
from backend.services.prompt_builder import SYSTEM_PROMPT, build_user_prompt

log = logging.getLogger("reverie.provider.openai_llm")


class OpenAIProvider(LLMProvider):
    """LLM provider backed by the OpenAI API."""

    def __init__(self) -> None:
        self._client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def generate_visual_prompt(self, song: SongInput) -> str:
        try:
            response = await self._client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": build_user_prompt(song)},
                ],
                max_tokens=120,
                temperature=0.6,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            log.error("OpenAI LLM error: %s", e)
            raise ProviderError("openai", str(e))
