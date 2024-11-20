import streamlit as st
import requests
from gtts import gTTS
import os
import base64
#from dotenv import load_dotenv

# Load environment variables from .env file
#load_dotenv()

# Set Cohere API key from environment variables
cohere_api_key = "3O2uRDDVta5S6yDmaYBCeEjVHc3ZAch6j7olGy9H"  # Replace with your actual Cohere API key

# Function to process text using Cohere (e.g., summarize or rephrase)
def cohere_process_text(prompt):
    url = "https://api.cohere.ai/generate"
    
    headers = {
        "Authorization": f"Bearer {cohere_api_key}",
        "Content-Type": "application/json"
    }
    
    # Prepare the data for the API request
    data = {
        "model": "command",  # Specify the Cohere model
        "prompt": prompt,
        "max_tokens": 100,  # Adjust based on your needs
        "temperature": 0.5  # Control creativity
    }
    
    try:
        # Send the request to Cohere's API
        response = requests.post(url, json=data, headers=headers)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Extract the response JSON
            response_data = response.json()
            
            # Check if 'text' is in the response
            if 'text' in response_data:
                return response_data['text'].strip()
            else:
                return f"Error: 'text' key not found in response. Response: {response_data}"
        else:
            return f"Error: {response.status_code} - {response.text}"
    
    except Exception as e:
        return f"Error: {str(e)}"

# Function to convert text to speech and save it as an MP3 file
def text_to_speech(text, lang="en"):
    try:
        # Generate speech
        tts = gTTS(text=text, lang=lang, slow=False)
        
        # Save audio to a temporary file
        audio_file = "output.mp3"
        tts.save(audio_file)
        return audio_file
    except Exception as e:
        return f"Error: {str(e)}"

# Function to generate a download link for the audio file
def generate_download_link(file_path):
    with open(file_path, "rb") as f:
        audio_bytes = f.read()
        b64 = base64.b64encode(audio_bytes).decode()
        href = f'<a href="data:audio/mp3;base64,{b64}" download="output.mp3">Download Speech</a>'
        return href

# Streamlit App Interface
st.set_page_config(page_title="Cohere Text-to-Speech App")
st.header("Cohere Text-to-Speech App")

# Input for text
input_text = st.text_area("Enter the text for processing and speech generation:", key="input")

# Dropdown to select language
language = st.selectbox("Select Language for Speech Output", options=["en", "es", "fr", "de", "hi"], index=0)

# Button to trigger text processing and TTS
submit = st.button("Process and Convert to Speech")

# If the button is clicked and the input text is not empty
if submit and input_text:
    # Use Cohere to process the text
    processed_text = input_text
    
    st.subheader("Processed Text:")
    st.write(processed_text)
    
    # Convert the processed text to speech
    audio_file_path = text_to_speech(processed_text, lang=language)
    
    if os.path.exists(audio_file_path):
        # Audio Player
        st.audio(audio_file_path, format="audio/mp3")
        
        # Download Link
        st.markdown(generate_download_link(audio_file_path), unsafe_allow_html=True)
        
        # Remove the temporary file
        os.remove(audio_file_path)
    else:
        st.error(audio_file_path)  # Display error message if TTS failed