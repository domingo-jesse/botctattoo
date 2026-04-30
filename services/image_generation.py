import base64
import logging
import os
from typing import Optional

from openai import OpenAI

logger = logging.getLogger(__name__)


class ImageGenerationError(Exception):
    """Raised when image generation cannot complete."""


def _build_prompt(style_name: str, abstract_context: str, image_prompt: str) -> str:
    return (
        "Create an original tattoo-ready illustration inspired by gothic social deduction themes. "
        "Use inspired motifs only; do not reproduce copyrighted logos, symbols, or exact Blood on the Clocktower artwork. "
        "Favor black ink line art and etching-style contrast unless style direction implies otherwise. "
        "Include atmospheric elements like gothic village silhouettes, clocktower forms, moon phases, ravens, demons, "
        "hidden identity symbolism, and circular tattoo composition where appropriate. "
        f"Tattoo style: {style_name}. "
        f"Abstract context: {abstract_context}. "
        f"Additional style direction: {image_prompt}."
    )


def generate_style_image(style_name: str, abstract_context: str, image_prompt: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ImageGenerationError("OPENAI_API_KEY is not configured.")

    prompt = _build_prompt(style_name, abstract_context, image_prompt)

    try:
        client = OpenAI(api_key=api_key)
        response = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024",
        )
        image_b64: Optional[str] = response.data[0].b64_json if response.data else None
        if not image_b64:
            raise ImageGenerationError("Image generation returned no image data.")
        return image_b64
    except ImageGenerationError:
        raise
    except Exception as exc:
        logger.exception("OpenAI image generation failed")
        raise ImageGenerationError(
            "We couldn't generate an image preview right now. Please try again."
        ) from exc


def b64_to_bytes(image_b64: str) -> bytes:
    return base64.b64decode(image_b64)
