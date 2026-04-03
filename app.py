import streamlit as st
import pandas as pd
import os
from PIL import Image

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Montino Sewing Gallery",
    page_icon="🧵",
    layout="wide",
)

# Initialize session state for clicked images
if 'show_aux' not in st.session_state:
    st.session_state['show_aux'] = None

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300&family=DM+Sans:wght@300;400&display=swap');

/* Full page black background */
[data-testid="stAppViewContainer"], 
[data-testid="stSidebar"], 
[data-testid="stHeader"], 
[data-testid="stToolbar"] {
    background-color: #000000 !important;
    color: #ffffff;
}

/* Sidebar styling */
section[data-testid="stSidebar"] { background: #4a148c; }
section[data-testid="stSidebar"] * { color: #f48fb1 !important; }

/* Headings */
h1 { font-family: 'Cormorant Garamond', serif; font-size: 3rem; font-weight: 300; color: #9c27b0; }
h2 { font-family: 'Cormorant Garamond', serif; font-size: 2rem; font-weight: 300; color: #ba68c8; }

/* Captions */
.gallery-caption { font-family: 'DM Sans', sans-serif; font-size: 0.82rem; color: #f48fb1; margin-top: 0.4rem; }

/* Divider */
hr { border: none; border-top: 1px solid #9c27b0; margin: 2rem 0; }

/* About text */
.about-text { font-size: 1.05rem; line-height: 1.85; max-width: 680px; color: #f48fb1; }

/* Collection badges */
.collection-tag { display:inline-block; background:#6a0dad; color:#f48fb1; font-size:0.72rem; letter-spacing:0.12em; padding:2px 10px; border-radius:2px; margin-bottom:0.5rem; text-transform:uppercase; }

/* Dark overlay for auxiliary images */
.aux-overlay { background-color: rgba(20,20,20,0.95); padding: 20px; border-radius: 6px; margin-top:10px; }
</style>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
PHOTOS_DIR = "photos"

@st.cache_data
def load_data():
    exts = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
    if not os.path.exists(PHOTOS_DIR):
        os.makedirs(PHOTOS_DIR)
        return pd.DataFrame(columns=["filename","collection","is_main","caption"])
    
    files = [f for f in os.listdir(PHOTOS_DIR) if os.path.splitext(f)[1].lower() in exts]

    def extract_collection(filename):
        base = filename[len("mcs_"):]  # remove prefix
        piece = "_".join(base.split("_")[:-1])  # remove _1/_2 suffix
        return piece

    df = pd.DataFrame({"filename": files})
    df["collection"] = df["filename"].apply(extract_collection)
    df["is_main"] = df["filename"].str.endswith("_1.jpeg")
    df["caption"] = df["collection"].apply(lambda x: f"This is a stylish {x} from the Montino collection.")
    return df

df = load_data()

# ── Define collection sets ─────────────────────────────────────────────────────
collection_sets = {
    "Greek Myth": ["shoes", "scarf", "gloves"],
    "Japanese Myth": ["eyes", "mask", "beanie"],
    "Painted Pins": ["stripes", "mountains", "scroll", "pincollectionpainted"],
    "Misc": ["phone"],
    "General Pins": [c for c in df["collection"].unique() if c not in ["shoes","scarf","gloves","eyes","mask","beanie","stripes","mountains","scroll","pincollectionpainted","phone"]]
}

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🧵 Navigation")
    page = st.radio("", ["About Me", "Full Gallery", "Sets"], label_visibility="collapsed")

# ══════════ PAGE: ABOUT ME ══════════
if page == "About Me":
    st.markdown("<h1>About Me</h1>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    col1, col2 = st.columns([1,1.6], gap="large")
    with col1:
        portrait_path = os.path.join(PHOTOS_DIR,"portrait.jpg")
        if os.path.exists(portrait_path):
            st.image(portrait_path, width=300)
        else:
            st.info("Add a portrait.jpg in your photos folder to show it here.")
    with col2:
        st.markdown("<h2>Hello, I'm Montino</h2>", unsafe_allow_html=True)
        st.markdown("""
<div class="about-text">
I'm a student sewer and textile artist building my Montino brand. This gallery shows main photos first, with auxiliary images revealed by clicking the main image.
</div>
""", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f"**{len(df)} pieces** across **{len(df['collection'].unique())} collections**")

# ══════════ PAGE: FULL GALLERY ══════════
elif page == "Full Gallery":
    st.markdown("<h1>Full Gallery</h1>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    display_df = df[df['is_main']]
    if display_df.empty:
        st.warning("No main images found in 'photos/'")
    else:
        cols = st.columns(2, gap="large")
        for i, row in display_df.iterrows():
            img_path = os.path.join(PHOTOS_DIR,row["filename"])
            with cols[i%2]:
                if os.path.exists(img_path):
                    st.image(img_path, width=400)
                    st.markdown(f'<span class="collection-tag">{row["collection"]}</span>', unsafe_allow_html=True)

                    # Checkbox to expand
                    if st.checkbox("Enlarge / show auxiliary images", key=row['filename']):
                        st.image(img_path, width=600)
                        st.markdown(f"**{row['collection']}**: {row['caption']}", unsafe_allow_html=True)
                        aux_df = df[(df['collection']==row['collection']) & (~df['is_main'])]
                        if not aux_df.empty:
                            cols_aux = st.columns(len(aux_df))
                            for c, (_, aux_row) in zip(cols_aux, aux_df.iterrows()):
                                aux_path = os.path.join(PHOTOS_DIR, aux_row["filename"])
                                c.image(aux_path, width=200)

# ══════════ PAGE: SETS ══════════
elif page == "Sets":
    st.markdown("<h1>Sets</h1>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    # Select a set
    selected_set = st.selectbox("Choose a set:", list(collection_sets.keys()))
    set_collections = collection_sets[selected_set]

    display_df = df[df['is_main'] & df['collection'].isin(set_collections)]
    if display_df.empty:
        st.warning("No main images found in this set.")
    else:
        cols = st.columns(2, gap="large")
        for i, row in display_df.iterrows():
            img_path = os.path.join(PHOTOS_DIR,row["filename"])
            with cols[i%2]:
                if os.path.exists(img_path):
                    st.image(img_path, width=400)
                    st.markdown(f'<span class="collection-tag">{row["collection"]}</span>', unsafe_allow_html=True)

                    # Checkbox to expand
                    if st.checkbox("Enlarge / show auxiliary images", key="set_"+row['filename']):
                        st.image(img_path, width=600)
                        st.markdown(f"**{row['collection']}**: {row['caption']}", unsafe_allow_html=True)
                        aux_df = df[(df['collection']==row['collection']) & (~df['is_main'])]
                        if not aux_df.empty:
                            cols_aux = st.columns(len(aux_df))
                            for c, (_, aux_row) in zip(cols_aux, aux_df.iterrows()):
                                aux_path = os.path.join(PHOTOS_DIR, aux_row["filename"])
                                c.image(aux_path, width=200)