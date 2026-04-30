import streamlit as st

st.set_page_config(page_title="BOTC Tattoo Mixer", page_icon="🩸", layout="wide")

st.title("🩸 BOTC Tattoo Mixer")
st.write(
    "Enter two roles (or one theme) and generate 5 tattoo-style concept ideas with descriptions and AI prompts."
)

styles = [
    {
        "name": "American Traditional",
        "descriptor": "bold black outlines, limited red/black palette, strong iconography",
    },
    {
        "name": "Blackwork / Dotwork",
        "descriptor": "heavy contrast black, geometric halos, stippled shading",
    },
    {
        "name": "Neo-Traditional",
        "descriptor": "ornamental framing, richer shadows, dramatic character focus",
    },
    {
        "name": "Fine Line",
        "descriptor": "clean thin lines, subtle symbols, elegant negative space",
    },
    {
        "name": "Dark Surrealism",
        "descriptor": "dreamlike symbolism, eerie composition, ritual atmosphere",
    },
]


def capitalize(text: str) -> str:
    return " ".join(word.capitalize() for word in text.split() if word)


def build_concept(a: str, b: str, style: dict[str, str]) -> dict[str, str]:
    core = f"{a} + {b}" if b else a
    if b:
        description = (
            f"A {style['name']} concept blending {a} and {b}: dual symbolism, mirrored "
            "elements, and a hidden BOTC clockface motif to represent deception vs truth."
        )
    else:
        description = (
            f"A {style['name']} concept inspired by {a}: a central emblem with BOTC motifs "
            "(grimoire sigils, moon phases, and the town square bell) to capture mystery "
            "and deduction."
        )

    ai_prompt = (
        f"Tattoo flash design, {style['name']}, {style['descriptor']}, Blood on the "
        f"Clocktower theme, {core}, high detail, stencil-ready composition, skin-safe "
        "spacing, dramatic contrast, no text"
    )

    return {"description": description, "ai_prompt": ai_prompt}


col1, col2 = st.columns(2)
with col1:
    role1 = st.text_input("Role / Theme 1", placeholder="e.g., Ravenkeeper")
with col2:
    role2 = st.text_input("Role / Theme 2 (optional)", placeholder="e.g., Scarlet Woman")

if st.button("Generate 5 Style Ideas", type="primary"):
    role1 = capitalize(role1.strip())
    role2 = capitalize(role2.strip())

    if not role1:
        st.warning("Please enter at least one role or theme.")
    else:
        cards = st.columns(2)
        for i, style in enumerate(styles):
            concept = build_concept(role1, role2, style)
            with cards[i % 2]:
                with st.container(border=True):
                    st.subheader(style["name"])
                    st.write(concept["description"])
                    st.caption("AI Prompt")
                    st.code(concept["ai_prompt"], language="text")
