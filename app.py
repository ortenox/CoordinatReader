import streamlit as st
from PIL import Image
import easyocr
import numpy as np
import re

st.set_page_config(page_title="Deteksi Koordinat dari Screenshot", layout="centered")
st.title("📸 Deteksi Koordinat dari Screenshot")

st.markdown("""
### 📋 Cara Menggunakan:
1. Ambil screenshot (misalnya dengan Snipping Tool atau PrtSc)
2. Klik pada area upload di bawah
3. Tekan **Ctrl + V** untuk langsung menempelkan gambar
""")

# File uploader yang bisa menangkap paste Ctrl+V (tidak perlu simpan manual)
uploaded_img = st.file_uploader("📎 Tempel atau unggah gambar (png/jpg/jpeg)", type=["png", "jpg", "jpeg"])

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

if uploaded_img:
    image = Image.open(uploaded_img)
    st.image(image, caption="🖼️ Gambar berhasil diterima", use_column_width=True)

    with st.spinner("🔍 Memproses teks dari gambar..."):
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
    st.info("📝 Tempel atau unggah gambar screenshot untuk mulai.")
