import streamlit as st
from PIL import Image
import easyocr
import numpy as np
import re

st.set_page_config(page_title="Deteksi Koordinat dari Screenshot", layout="centered")
st.title("📸 Deteksi Koordinat dari Screenshot")

uploaded_file = st.file_uploader(
    "📤 Klik di sini lalu tekan **Ctrl + V** untuk tempel screenshot (atau unggah manual)", 
    type=["png", "jpg", "jpeg"]
)

@st.cache_resource
def load_reader():
    return easyocr.Reader(['en'], gpu=False)

reader = load_reader()

def extract_latlong_from_text(text):
    matches = re.findall(r"[-+]?\d+\.\d+", text)
    if len(matches) >= 2:
        lat = float(matches[0])
        lon = float(matches[1])
        return f"{lat},{lon}"
    return None

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="🖼️ Gambar berhasil dimuat", use_column_width=True)

    with st.spinner("🔍 Memproses OCR..."):
        result = reader.readtext(np.array(image), detail=0)
        ocr_result = "\n".join(result)

    st.text_area("📄 Hasil OCR:", ocr_result, height=150)

    coords = extract_latlong_from_text(ocr_result)
    if coords:
        gmaps_url = f"https://www.google.com/maps/search/?api=1&query={coords}"
        st.success(f"✅ Koordinat ditemukan: {coords}")
        st.markdown(f"[🌍 Lihat di Google Maps]({gmaps_url})", unsafe_allow_html=True)
    else:
        st.error("❌ Koordinat tidak valid ditemukan.")
else:
    st.info("📝 Silakan unggah atau tempel screenshot koordinat.")
