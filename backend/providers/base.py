from abc import ABC, abstractmethod
from backend.models.schemas import SongInput


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    async def generate_visual_prompt(self, song: SongInput) -> str:
        """Generate an image generation prompt from song data.

        Args:
            song: Resolved song metadata and optional audio features.

        Returns:
            A descriptive visual prompt suitable for image generation.

        Raises:
            ProviderError: If the LLM call fails.
        """
        ...


class ImageProvider(ABC):
    """Abstract base class for image generation providers."""

    @abstractmethod
    async def generate_image(self, prompt: str) -> str:
        """Generate an image from a visual prompt.

        Args:
            prompt: Descriptive visual prompt from the LLM.

        Returns:
            A publicly accessible URL to the generated image.

        Raises:
            ProviderError: If image generation fails.
        """
        ...


class ProviderError(Exception):
    """Raised when a provider call fails."""

    def __init__(self, provider: str, message: str) -> None:
        self.provider = provider
        self.message = message
        super().__init__(f"[{provider}] {message}")
