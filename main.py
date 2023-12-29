import streamlit as st
from PIL import Image

def main():
    st.title("Image Upload Tutorial")

    # File uploader widget
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()

        # To convert to a PIL Image:
        image = Image.open(uploaded_file)

        st.image(image, caption='Uploaded Image.', use_column_width=True)

if __name__ == "__main__":
    main()
