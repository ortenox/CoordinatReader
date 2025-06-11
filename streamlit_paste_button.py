import streamlit.components.v1 as components
from PIL import Image
import io
import base64

def paste_image_button(label="Paste image"):
    components.html(
        f"""
        <script>
        const streamlitDoc = window.parent.document;

        function sendImageToStreamlit(imgBase64) {{
            const streamlitInput = streamlitDoc.querySelector('iframe[srcdoc]').contentWindow;
            streamlitInput.postMessage({{ type: "streamlit:setComponentValue", value: imgBase64 }}, "*");
        }}

        streamlitDoc.addEventListener("paste", function(event) {{
            const items = (event.clipboardData || event.originalEvent.clipboardData).items;
            for (const item of items) {{
                if (item.type.indexOf("image") === 0) {{
                    const blob = item.getAsFile();
                    const reader = new FileReader();
                    reader.onload = function(event) {{
                        sendImageToStreamlit(event.target.result);
                    }};
                    reader.readAsDataURL(blob);
                }}
            }}
        }});
        </script>
        <button onclick="alert('Silakan tekan Ctrl+V setelah menyalin gambar ke clipboard.')">{label}</button>
        """,
        height=50
    )

    # Streamlit component return handling
    image_data = components.declare_component("image_paste_button", default=None)()
    if image_data:
        header, encoded = image_data.split(",", 1)
        binary_data = base64.b64decode(encoded)
        return Image.open(io.BytesIO(binary_data))
    return None
