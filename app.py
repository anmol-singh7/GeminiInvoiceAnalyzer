## Invoice Extractor
from  dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemino_response(input,image,prompt):
    ## loading the gemini model
    model= genai.GenerativeModel("gemini-pro-vision")
    response = model.generate_content([input,image[0],prompt])
    return response.text


def input_image_setup(uploaded_file):
     if uploaded_file is not None:
          byte_data = uploaded_file.getvalue()

          image_parts =[
               {
                    "mime_type":uploaded_file.type,
                    "data":byte_data
               }
          ]
          return image_parts
     else:
          raise FileNotFoundError("No file uploaded")