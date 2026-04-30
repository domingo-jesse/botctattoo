import logging
import streamlit as st

from services.image_generation import ImageGenerationError, generate_style_image
from services.tattoo_styles import load_styles, set_style_image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(page_title="BOTC Tattoo Mixer", page_icon="🩸", layout="wide")


if "generated_images" not in st.session_state:
    st.session_state.generated_images = {}

if "failed_images" not in st.session_state:
    st.session_state.failed_images = {}

st.title("🩸 BOTC Tattoo Mixer")
st.write(
    "Enter two roles (or one theme) and generate 5 tattoo-style concept ideas with descriptions and AI prompts."
)


def capitalize(text: str) -> str:
    return " ".join(word.capitalize() for word in text.split() if word)


def build_concept(a: str, b: str, style: dict[str, str]) -> dict[str, str]:
    core = f"{a} + {b}" if b else a
    if b:
        description = (
            f"A {style['style_name']} concept blending {a} and {b}: dual symbolism, mirrored "
            "elements, and a hidden BOTC-inspired clockface motif to represent deception vs truth."
        )
    else:
        description = (
            f"A {style['style_name']} concept inspired by {a}: a central emblem with gothic motifs "
            "(moon phases, village bell, and shadowed sigils) to capture mystery and deduction."
        )

    ai_prompt = (
        f"Tattoo flash design, {style['style_name']}, {style['image_prompt']}, gothic social deduction "
        f"theme, {core}, high detail, stencil-ready composition, skin-safe spacing, dramatic contrast, no text"
    )

    return {"description": description, "ai_prompt": ai_prompt}


styles = [s.to_dict() for s in load_styles()]

col1, col2 = st.columns(2)
with col1:
    role1 = st.text_input("Role / Theme 1", placeholder="e.g., Ravenkeeper")
with col2:
    role2 = st.text_input("Role / Theme 2 (optional)", placeholder="e.g., Scarlet Woman")

if st.button("Generate 5 Style Ideas", type="primary"):
    st.session_state.show_styles = True
    st.session_state.role1 = capitalize(role1.strip())
    st.session_state.role2 = capitalize(role2.strip())

if st.session_state.get("show_styles"):
    role1 = st.session_state.get("role1", "")
    role2 = st.session_state.get("role2", "")

    if not role1:
        st.warning("Please enter at least one role or theme.")
    else:
        cards = st.columns(2)
        for i, style in enumerate(styles):
            concept = build_concept(role1, role2, style)
            with cards[i % 2]:
                with st.container(border=True):
                    style_name = style["style_name"]
                    st.subheader(style_name)
                    st.write(style["description"])
                    st.markdown(f"**Abstract context:** {style['abstract_context']}")
                    st.caption("AI Prompt")
                    st.code(concept["ai_prompt"], language="text")

                    image_url = st.session_state.generated_images.get(style_name) or style.get("ai_image_url")

                    if image_url:
                        st.image(image_url, caption=f"{style_name} AI preview", use_container_width=True)
                        button_label = "Regenerate Image"
                    else:
                        button_label = "Generate Image"

                    if st.session_state.failed_images.get(style_name):
                        st.caption("Previous generation attempt failed. Click the button to retry.")

                    if st.button(button_label, key=f"gen-{style_name}"):
                        try:
                            with st.spinner("Generating tattoo preview..."):
                                image_url = generate_style_image(
                                    style_name=style_name,
                                    abstract_context=style["abstract_context"],
                                    extra_prompt=concept["ai_prompt"],
                                )
                                st.session_state.generated_images[style_name] = image_url
                                st.session_state.failed_images[style_name] = False
                                set_style_image(style_name, image_url)
                                st.rerun()
                        except ImageGenerationError as exc:
                            st.session_state.failed_images[style_name] = True
                            st.error(str(exc))
                            logger.exception("Image generation failed: %s", exc)
