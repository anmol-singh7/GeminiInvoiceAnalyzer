## Invoice Extractor
from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
from io import BytesIO

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemino_response(image_data, mime_type, prompt):
   
    uploaded_image = genai.upload_file(image_data, mime_type=mime_type)
    
    # Load the Gemini model
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    # Generate content based on the uploaded image and prompt
    response = model.generate_content([uploaded_image, "\n\n", prompt])
    # The "\n\n" in [uploaded_image, "\n\n", prompt] serves as a separator between
    # the image and the text prompt. This is commonly used for readability or to 
    # distinguish sections when feeding multiple types of input into a model
   
    return response.text

st.set_page_config(page_title="Invoice Extractor")

st.header("Gemini Application")
input_prompt = st.text_input("Enter your question or prompt:", key="input")
uploaded_file = st.file_uploader("Choose an invoice image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

base_prompt = """
You are an expert in understanding invoices. 
You will receive an invoice image and will answer questions based on it.
"""


if st.button("Analyze Invoice"):
    if uploaded_file is not None:
        # Convert uploaded file to BytesIO to keep it in memory
        image_data = BytesIO(uploaded_file.getvalue())
        
        mime_type = uploaded_file.type
        
        response = get_gemino_response(image_data, mime_type, f"{base_prompt}\n{input_prompt}")
        
        st.subheader("Response from Gemini:")
        st.write(response)
    else:
        st.error("Please upload an invoice image.")
