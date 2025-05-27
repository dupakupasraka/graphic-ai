import streamlit as st
import requests
import base64
import datetime
import random
import csv
from PIL import Image
from io import BytesIO

# Konfiguracja
st.set_page_config(layout="centered")
st.title("🎨 Amazon T-Shirt Generator")

# Użytkownik podaje API key
api_key = st.text_input("🔑 Podaj swój Stability AI API Key", type="password")

# Liczba grafik
num_images = st.number_input("📦 Ile grafik wygenerować?", min_value=1, max_value=1000, value=5)

# Przycisk startu
if st.button("🚀 Generuj grafiki"):
    if not api_key:
        st.error()
    else:
        prompts = [
            "Minimalist cat with sunglasses",
            "Funny skeleton dancing with pizza",
            "Retro dog in sunglasses",
            "Inspirational quote in bold typography",
            "Cute ghost with coffee cup"
        ]
        today = datetime.datetime.now().strftime("%B %d")
        images = []
        metadata = []

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        for i in range(num_images):
            prompt = random.choice(prompts) + f", transparent background, holiday: {today}"
            data = {
                "cfg_scale": 7,
                "clip_guidance_preset": "FAST_BLUE",
                "height": 1024,
                "width": 1024,
                "samples": 1,
                "steps": 30,
                "style_preset": "digital-art",
                "text_prompts": [{"text": prompt, "weight": 1}]
            }

            response = requests.post(
                "https://api.stability.ai/v1/generation/stable-diffusion-v1-5/text-to-image",
                headers=headers,
                json=data,
            )

            if response.status_code != 200:
                st.error(f"❌ Błąd: {response.text}")
                break

            result = response.json()
            image_data = result["artifacts"][0]["base64"]
            image = Image.open(BytesIO(base64.b64decode(image_data))).convert("RGBA")
            filename = f"tshirt_{i+1}.png"
            image.save(filename)
            images.append((filename, image))
            metadata.append({
                "filename": filename,
                "title": prompt[:80],
                "tags": "tshirt, print, design, ai, " + today.lower(),
                "description": f"T-shirt design featuring: {prompt}"
            })

        # Wyświetl i pozwól pobrać obrazy
        for name, img in images:
            st.image(img, caption=name)
            with open(name, "rb") as f:
                btn = st.download_button(
                    label=f"⬇️ Pobierz {name}",
                    data=f,
                    file_name=name,
                    mime="image/png"
                )

        # Zapisz CSV
        csv_filename = "metadata.csv"
        with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["filename", "title", "tags", "description"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in metadata:
                writer.writerow(row)

        with open(csv_filename, "rb") as f:
            st.download_button("📄 Pobierz metadane CSV", f, file_name=csv_filename, mime="text/csv")
