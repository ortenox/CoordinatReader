import streamlit as st
from PIL import Image
import easyocr
import numpy as np
import re
from openlocationcode import openlocationcode as olc

st.set_page_config(page_title="Deteksi Koordinat & Plus Code", layout="centered")
st.title("📸 Deteksi Koordinat & Plus Code dari Gambar")

st.markdown("""
### 📋 Cara Menggunakan:
1. Ambil screenshot koordinat (misalnya dari Google Maps)
2. Klik area upload di bawah, lalu tekan **Ctrl + V** untuk tempel gambar
3. Sistem akan mendeteksi koordinat & menampilkan Plus Code
""")

# Upload atau paste gambar
uploaded_img = st.file_uploader("📎 Tempel atau unggah gambar (png/jpg/jpeg)", type=["png", "jpg", "jpeg"])

@st.cache_resource
def load_reader():
    return easyocr.Reader(['en'], gpu=False)

reader = load_reader()

# Ekstrak koordinat dari teks
def extract_latlong_from_text(text):
    matches = re.findall(r"[-+]?\d+\.\d+", text)
    if len(matches) >= 2:
        lat = float(matches[0])
        lon = float(matches[1])
        return lat, lon
    return None, None

# Konversi lat/lon ke Plus Code lengkap & singkat
def latlon_to_plus_codes(lat, lon):
    full_code = olc.encode(lat, lon)
    try:
        short_code = olc.shorten(full_code, lat, lon)
    except:
        short_code = full_code  # fallback jika tidak bisa disingkat
    return full_code, short_code

if uploaded_img:
    image = Image.open(uploaded_img)
    st.image(image, caption="🖼️ Gambar diterima", use_column_width=True)

    with st.spinner("🔍 Memproses teks dari gambar..."):
        result = reader.readtext(np.array(image), detail=0)
        ocr_result = "\n".join(result)

    st.text_area("📄 Hasil OCR:", ocr_result, height=150)

    lat, lon = extract_latlong_from_text(ocr_result)
    if lat is not None and lon is not None:
        full_code, short_code = latlon_to_plus_codes(lat, lon)

        gmaps_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
        plus_code_url = f"https://www.google.com/maps/search/?api=1&query={short_code}"

        st.success(f"✅ Koordinat ditemukan: {lat}, {lon}")
        st.markdown(f"- [🌍 Lihat di Google Maps (Koordinat)]({gmaps_url})", unsafe_allow_html=True)
        st.markdown(f"- [🧭 Lihat di Google Maps (Plus Code: `{short_code}`)]({plus_code_url})", unsafe_allow_html=True)
        st.caption(f"Kode Plus Lengkap: `{full_code}`")
    else:
        st.error("❌ Koordinat tidak ditemukan dari gambar.")
else:
    st.info("📝 Tempel atau unggah screenshot yang mengandung koordinat.")
