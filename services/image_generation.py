import logging

import streamlit as st
from openai import OpenAI

logger = logging.getLogger(__name__)


class ImageGenerationError(Exception):
    """Raised when image generation cannot complete."""


def get_openai_client() -> OpenAI:
    api_key = st.secrets.get("OPENAI_API_KEY")

    if not api_key or not api_key.strip():
        raise ImageGenerationError("OPENAI_API_KEY is not configured.")

    return OpenAI(api_key=api_key)


def generate_style_image(style_name: str, abstract_context: str, extra_prompt: str = "") -> str:
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
        client = get_openai_client()
        result = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024",
        )

        if not result or not result.data or len(result.data) == 0:
            raise ImageGenerationError("No image returned from OpenAI")

        image_data = result.data[0]

        if hasattr(image_data, "url") and image_data.url:
            return image_data.url

        if hasattr(image_data, "b64_json") and image_data.b64_json:
            return f"data:image/png;base64,{image_data.b64_json}"

        raise ImageGenerationError("Image response missing url and base64 data")
    except ImageGenerationError:
        raise
    except Exception as exc:
        logger.exception("Image generation failed")
        message = str(exc)
        if "401" in message or "invalid_api_key" in message:
            raise ImageGenerationError(
                "OpenAI authentication failed. Check your API key in Streamlit secrets."
            ) from exc
        raise ImageGenerationError("Image generation failed") from exc
