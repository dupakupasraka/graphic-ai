import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import datetime
import random
from topics import get_random_prompt
from tags_generator import generate_tags

st.set_page_config(layout="centered")
st.title("Merch AI Generator – Auto Mode")

count = st.slider("Ile grafik wygenerować?", 1, 10, 100)
generate = st.button("Generuj teraz")

if generate:
    with st.spinner("Generowanie grafik..."):
        for i in range(count):
            prompt = get_random_prompt()
            url = f"https://image.pollinations.ai/prompt/{prompt}"
            try:
                response = requests.get(url)
                img = Image.open(BytesIO(response.content)).convert("RGB")
                img = img.resize((4500, 5400))
                today = datetime.date.today().isoformat()
                filename = f"{prompt.replace(' ', '_')}_{today}.png"
                img.save(file_name, dpi=(300, 300))

                st.image(img, caption=f"{prompt}")
                with open(file_name, "rb") as file:
                    st.download_button("Pobierz grafikę", file, file_name=file_name)

                title, description, tags = generate_tags(prompt)
                st.subheader("Tytuł i tagi")
                st.text(f"Title: {title}")
                st.text(f"Description: {description}")
                st.text(f"Tags: {', '.join(tags)}")
                st.markdown("---")

            except Exception as e:
                st.error(f"Błąd dla promptu '{prompt}': {e}")
