import httpx
from backend.models.schemas import SongInput
from backend.providers.base import LLMProvider, ProviderError
from backend.services.prompt_builder import SYSTEM_PROMPT, build_user_prompt

POLLINATIONS_TEXT_URL = "https://text.pollinations.ai/openai"


class PollinationsLLMProvider(LLMProvider):
    """LLM provider backed by the Pollinations text API (no key required)."""

    async def generate_visual_prompt(self, song: SongInput) -> str:
        payload = {
            "model": "openai",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": build_user_prompt(song)},
            ],
            "max_tokens": 120,
            "temperature": 0.9,
        }
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(POLLINATIONS_TEXT_URL, json=payload)
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"].strip()
        except Exception as e:
            raise ProviderError("pollinations_llm", str(e))
