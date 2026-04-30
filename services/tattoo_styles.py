from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any

STYLE_CACHE_PATH = Path("data/tattoo_styles_cache.json")


@dataclass
class TattooStyle:
    style_name: str
    description: str
    abstract_context: str
    image_prompt: str
    ai_image_url: str | None = None
    ai_image_base64: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    image_generated_at: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def default_styles() -> list[TattooStyle]:
    return [
        TattooStyle(
            style_name="American Traditional",
            description="Bold iconic shapes with heavy outlines and limited palette.",
            abstract_context="Uses ritual objects, mirrored masks, and a clock motif to express truth vs deception in a haunted village.",
            image_prompt="bold black outlines, limited red/black accents, strong iconography",
        ),
        TattooStyle(
            style_name="Blackwork / Dotwork",
            description="High-contrast black fields and stippled gradient depth.",
            abstract_context="Uses distorted clock imagery, hidden role symbolism, and gothic village motifs to represent deception, fate, and social deduction.",
            image_prompt="heavy contrast black, geometric halos, stippled shading",
        ),
        TattooStyle(
            style_name="Neo-Traditional",
            description="Ornamental framing with dramatic focal storytelling.",
            abstract_context="Combines moonlit architecture, ornate framing, and dual-character allegory to depict social bluffing and revelation.",
            image_prompt="ornamental framing, richer shadows, dramatic character focus",
        ),
        TattooStyle(
            style_name="Fine Line",
            description="Minimal elegant linework with symbolic negative space.",
            abstract_context="Focuses on subtle hidden identities using delicate sigils, moon phases, and restrained circular balance.",
            image_prompt="clean thin lines, subtle symbols, elegant negative space",
        ),
        TattooStyle(
            style_name="Dark Surrealism",
            description="Dreamlike, eerie storytelling with ritual atmosphere.",
            abstract_context="Blends fragmented faces, ravens, and impossible clocktower geometry to communicate paranoia and manipulated perception.",
            image_prompt="dreamlike symbolism, eerie composition, ritual atmosphere",
        ),
    ]


def load_styles() -> list[TattooStyle]:
    if not STYLE_CACHE_PATH.exists():
        styles = default_styles()
        save_styles(styles)
        return styles

    raw = json.loads(STYLE_CACHE_PATH.read_text())
    return [TattooStyle(**item) for item in raw]


def save_styles(styles: list[TattooStyle]) -> None:
    STYLE_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STYLE_CACHE_PATH.write_text(json.dumps([s.to_dict() for s in styles], indent=2))


def set_style_image(style_name: str, image_b64: str) -> None:
    styles = load_styles()
    now = _now_iso()
    for style in styles:
        if style.style_name == style_name:
            if not style.created_at:
                style.created_at = now
            style.updated_at = now
            style.image_generated_at = now
            style.ai_image_base64 = image_b64
            break
    save_styles(styles)
