import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Montino Sewing Gallery", page_icon="🧵", layout="wide")

PHOTOS_DIR = "photos"

# ══════════════════════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════════════════════
COLLECTION_SETS = {
    "Greek Myth":           ["gloves", "scarf", "shoes"],
    "Japanese Myth":        ["eyes", "mask", "beanie"],
    "Accessories":          ["phone"],
    "Pins — General":       ["butterfly", "lillypad", "sanddollar", "scarab", "snowflake", "ginko", "pincollection"],
    "Pins — Painted":       ["mountains", "pincollectionpainted", "stripes", "scroll"],
    "Pins — Stained Glass": ["koi", "hummingbird"],
}

CAPTIONS = {
    "beanie":               "Hear No Evil. A ribbed black beanie featuring a painted kanji patch with work and a rim of fabric Montino's Hearts.",
    "eyes":                 "See No Evil. A magenta eye mask with hand-painted leather Montino's Heart patches with Shide; Japanese mythological symbols. The design is complete with a branded kanji patch on the strap.",
    "mask":                 "Speak No Evil. A black fabric face mask adorned with a hand painted leather Montino's Heart motif and hand painted leather kanji label patches.",
    "gloves":               "The Midas Gloves — quilted dark fabric embroidered with the Greek words for Golden Ash and an abstract constellation pattern.",
    "scarf":                "The Icarus Scarf — black fleece scattered with painted stars and trimmed with purple feathers.",
    "shoes":                "The Achilles and Patroclus Converse — hand-embroidered fabric boots with painted leather Montino's Heart patches, hand painted moon emblems, painted stars and embroidered with Greek lettering.",
    "phone":                "The Be Not Afraid matching hand-painted phone case and AirPod case set, featuring a purple galaxy motif with butterflies and some religious references.",
    "butterfly":            "A small fabric Butterfly pin in navy blue Japanese indigo cotton with hand-stitched edges.",
    "lillypad":             "A Lily Pad pin cut from teal dotted fabric with embroidered french knots in variegated thread with hand-finished edges.",
    "sanddollar":           "A circular linen pin with a hand-embroidered Sand Dollar design on a striped fabric. Finished in gold thread.",
    "scarab":               "A round Scarab pin densely hand-embroidered in a purple and blue variegated thread.",
    "pincollection":        "The general pin collection displayed together.",
    "snowflake":            "A small Snowflake pin in pale blue fabric with geometric hand-stitched detail.",
    "ginko":                "A Ginkgo leaf pin — hand-sewn leaf veins on felt fabric with delicate detailing.",
    "scroll":               "A rectangular leather pin painted to resemble an ancient Scroll.",
    "mountains":            "A rectangular leather pin painted to resemble Mountain grey peaks against a pale sky.",
    "pincollectionpainted": "The painted pin collection displayed together.",
    "stripes":              "A rectangular striped leather pin painted with diagonal bands.",
    "koi":                  "A Koi Fish pin hand embroidered in a stained glass style.",
    "hummingbird":          "A Hummingbird pin hand embroidered in a stained glass style.",
}

SET_DESCRIPTIONS = {
    "Greek Myth":           "Pieces inspired by the myths of ancient Greece — Midas, Icarus, and the bond of Achilles and Patroclus. The set uses constellation imagery, greek lettering, and a consistent purple and black palette. These elements build a cohesive set design and visual messaging.",
    "Japanese Myth":        "A collection drawing from Japanese folklore, specifically the Three Wise Monkeys, from the Toshogu shrine. Each piece embodies a lesson about how to filter out the evils of the world from your life. They feature hand-painted kanji patches on leather, hand painted Japanese motifs; like the Shide zig zag symbol for warding off evil.",
    "Accessories":          "Hand-painted phone and AirPod cases featuring a purple galaxy and cherry blossom motif. The Be Not Afraid set references the creation myth and spiritual imagery.",
    "Pins — General":       "Hand-sewn fabric pins — Butterflies, Lily Pads, Sand Dollars, Scarabs, Snowflakes, and Ginkgo leaves. A vast collection of Nature inspired pins using creative embroidery techniques.",
    "Pins — Painted":       "Pins hand painted, featuring Mountains, Stripes, and Scrolls.",
    "Pins — Stained Glass": "Koi and Hummingbird pins hand embroidered with full fill technique in a vivid stained glass style.",
}

# ══════════════════════════════════════════════════════════════════════════════
# DATA LOADING
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data
def load_data():
    exts = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
    if not os.path.exists(PHOTOS_DIR):
        os.makedirs(PHOTOS_DIR)
        return pd.DataFrame(columns=["filename", "collection", "is_main"])
    files = sorted([f for f in os.listdir(PHOTOS_DIR) if os.path.splitext(f)[1].lower() in exts])
    def get_collection(fn):
        b = fn
        if b.startswith("mcs_"): b = b[4:]
        b = os.path.splitext(b)[0]
        return "_".join(b.split("_")[:-1])
    df = pd.DataFrame({"filename": files})
    df["collection"] = df["filename"].apply(get_collection)
    df["is_main"]    = df["filename"].apply(lambda f: f.split("_")[-1].split(".")[0] == "1")
    return df

df = load_data()

# ══════════════════════════════════════════════════════════════════════════════
# GRID RENDERER
# ══════════════════════════════════════════════════════════════════════════════
def render_grid(display_df):
    if display_df.empty:
        st.warning("No images found.")
        return
    cols = st.columns(2, gap="large")
    for i, (_, row) in enumerate(display_df.iterrows()):
        img_path = os.path.join(PHOTOS_DIR, row["filename"])
        if not os.path.exists(img_path):
            continue
        with cols[i % 2]:
            st.image(img_path, use_container_width=True)
            st.caption(f"✦ {row['collection']}")
            all_images = [
                os.path.join(PHOTOS_DIR, r["filename"])
                for _, r in df[df["collection"] == row["collection"]].iterrows()
                if os.path.exists(os.path.join(PHOTOS_DIR, r["filename"]))
            ]
            caption = CAPTIONS.get(row["collection"], "")
            with st.expander("View details"):
                for img in all_images:
                    st.image(img, use_container_width=True)
                if caption:
                    st.write(caption)

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.title("🧵 Montino")
    st.divider()
    page = st.radio(
        "Navigate",
        ["About Me", "Full Gallery", "Sets"],
        label_visibility="collapsed"
    )

# ══════════════════════════════════════════════════════════════════════════════
# PAGES
# ══════════════════════════════════════════════════════════════════════════════
if page == "About Me":
    st.title("About Me")
    st.divider()
    st.subheader("Hello, I'm Montino")
    st.write(
        "My name is Zirk Montino Weil. I'm a high school student and textile artist; "
        "passionate about wearable art inspired by mythology, storytelling, and textile craft. "
        "I enjoy painting, leatherwork, hard stitching and embroidery techniques. "
        "I like making wearable craft and have made these art collections with that in mind."
    )
    st.write(
        "Each collection visible here on this site represents a different chapter of my personal "
        "interests — from Greek and Japanese myths, spiritualism and cosmology. I have translated "
        "my love for these themes into hand-stitched pins and painted accessories. "
        "This gallery was built as part of my Computer Science project, merging two things I love: "
        "making things by hand and making things with code. I am excited to share these finished "
        "projects with the wider world and to gain feedback and inspiration."
    )
    st.divider()
    st.write(f"**{len(df[df['is_main']])} pieces** across **{len(COLLECTION_SETS)} collections**")

elif page == "Full Gallery":
    st.title("Full Gallery")
    st.divider()
    render_grid(df[df["is_main"]])

elif page == "Sets":
    st.title("Sets")
    st.divider()
    set_options = [
        f"{name} ({len(df[df['is_main'] & df['collection'].isin(members)])})"
        for name, members in COLLECTION_SETS.items()
    ]
    selected_label  = st.selectbox("Choose a collection:", set_options)
    selected_set    = selected_label.split(" (")[0]
    set_collections = COLLECTION_SETS[selected_set]
    st.subheader(selected_set)
    if selected_set in SET_DESCRIPTIONS:
        st.write(SET_DESCRIPTIONS[selected_set])
    st.divider()
    render_grid(
        df[df["is_main"] & df["collection"].isin(set_collections)]
    )