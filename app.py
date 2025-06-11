import streamlit as st
import pytesseract
from PIL import Image
import re
import io

st.title("🛰️ Deteksi Koordinat dari Screenshot")

uploaded_file = st.file_uploader("📤 Unggah gambar (screenshot koordinat)", type=["png", "jpg", "jpeg"])

def extract_latlong_from_text(text):
    matches = re.findall(r"[-+]?\d+\.\d+", text)
    if len(matches) >= 2:
        lat = float(matches[0])
        lon = float(matches[1])
        return f"{lat},{lon}"
    else:
        return None

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="🖼️ Gambar yang diunggah", use_column_width=True)

    ocr_result = pytesseract.image_to_string(image)
    st.text_area("📄 Hasil OCR", ocr_result, height=100)

    coords = extract_latlong_from_text(ocr_result)
    if coords:
        maps_url = f"https://www.google.com/maps/search/?api=1&query={coords}"
        st.success(f"✅ Koordinat Ditemukan: {coords}")
        st.markdown(f"[🌍 Buka di Google Maps]({maps_url})")
    else:
        st.error("❌ Tidak bisa mengenali koordinat.")
