import streamlit as st
import openai
import requests
from io import BytesIO

# Set your OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("🎨 Mandala Art Generator")

st.write("Enter a **single word** below. I will create a **black and white Mandala** inspired by it!")

# User input
word = st.text_input("Enter one word:", max_chars=20)

if st.button("Generate Mandala"):
    if not word.strip():
        st.error("Please enter a valid word.")
    else:
        with st.spinner("Creating your Mandala..."):
            prompt = f"Create a detailed, intricate black and white Mandala art inspired by the word '{word}'. The Mandala should be symmetric, highly artistic, and purely black and white, no colors."

            try:
                response = openai.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    n=1,
                    size="1024x1024",
                    quality="standard"
                )

                image_url = response.data[0].url

                # Get the image content
                image_response = requests.get(image_url)
                image_bytes = BytesIO(image_response.content)

                st.image(image_bytes, caption="Generated Mandala", use_container_width=True)

                # Download button
                st.download_button(
                    label="📥 Download Mandala",
                    data=image_bytes,
                    file_name=f"mandala_{word}.png",
                    mime="image/png"
                )

            except Exception as e:
                st.error(f"Error generating Mandala: {e}")
