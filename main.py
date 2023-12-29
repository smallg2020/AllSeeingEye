import streamlit as st
import openai
from PIL import Image
import os
from gtts import gTTS
import json
import base64

def main():
    def load_api_key():
        with open('config_encoded.txt', 'r') as encoded_file:
            encoded_string = encoded_file.read()
        decoded_bytes = base64.b64decode(encoded_string)
        config = json.loads(decoded_bytes)
        return config['openai_api_key']

    def encode_image(_file):
        # Convert the uploaded file to bytes, then encode it in base64
        file_bytes = _file.getvalue()
        return base64.b64encode(file_bytes).decode('utf-8')

    st.title("Image Upload and Analysis")

    # File uploader widget
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    openai.api_key = load_api_key()
    client = openai.OpenAI(api_key=openai.api_key)

    if uploaded_file is not None:
        base64_image = encode_image(uploaded_file)

        if base64_image:
            with_prompt = "describe the image as if i was blind, be brief but point out important objects"
            with st.spinner('Wait for it... generating response'):
                image = Image.open(uploaded_file)
                st.image(image, caption='Uploaded Image.', width=256)
                if os.path.exists("response.mp3"):
                    os.remove("response.mp3")
                try:
                    response = client.chat.completions.create(
                        model="gpt-4-vision-preview",
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": with_prompt},
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/jpeg;base64,{base64_image}",
                                        },
                                    },
                                ],
                            }
                        ],
                        max_tokens=100,
                    )

                    st.text("AI Response:")
                    # Correctly extracting the response text
                    response_text = response.choices[0].message.content
                    st.write(response_text)

                    tts = gTTS(text=response_text, lang='en')
                    tts_file = 'response.mp3'
                    tts.save(tts_file)
                    audio_file = open(tts_file, 'rb')
                    audio_bytes = audio_file.read()
                    st.audio(audio_bytes, format='audio/mp3', start_time=0)

                except Exception as e:
                    st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
