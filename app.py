import streamlit as st
from PIL import Image
import easyocr
import numpy as np
import re
from streamlit_paste_button import paste_image_button

st.set_page_config(page_title="Deteksi Koordinat dari Screenshot", layout="centered")
st.title("📸 Deteksi Koordinat dari Screenshot")

# Komponen paste image dari clipboard
image = paste_image_button("📋 Klik tombol ini lalu tekan Ctrl+V untuk tempel screenshot dari clipboard")

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

if image:
    st.image(image, caption="🖼️ Gambar berhasil ditempel", use_column_width=True)

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
    st.info("📝 Tempel screenshot menggunakan Ctrl+V atau klik tombol paste di atas.")
