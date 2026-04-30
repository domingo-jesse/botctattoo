import logging
import os

from openai import OpenAI

logger = logging.getLogger(__name__)


class ImageGenerationError(Exception):
    """Raised when image generation cannot complete."""


def generate_style_image(style_name: str, abstract_context: str, extra_prompt: str = "") -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ImageGenerationError("OPENAI_API_KEY is not configured")

    client = OpenAI(api_key=api_key)

    prompt = f"""
Tattoo design, black ink, high detail.
Style: {style_name}
Concept: {abstract_context}

Blood on the Clocktower inspired (DO NOT copy official art).
Use gothic horror, clocktower, moon, ravens, secrecy, social deduction.
Do not generate official logos or exact copyrighted icons.

Circular tattoo composition.
Clean linework, tattoo stencil ready.

{extra_prompt}
"""

    try:
        result = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024",
        )
        image_url = result.data[0].url if result.data else None
        if not image_url:
            raise ImageGenerationError("Image generation failed")
        return image_url
    except ImageGenerationError:
        raise
    except Exception as exc:
        logger.exception("Image generation failed")
        raise ImageGenerationError("Image generation failed") from exc
