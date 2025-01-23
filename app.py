from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()  # Load environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """You are YouTube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here:  """

# Function to extract transcript details
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        
        # Attempt to fetch the transcript
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Combine the transcript parts into a single string
        transcript = ""
        for item in transcript_text:
            transcript += " " + item["text"]
        
        return transcript

    except TranscriptsDisabled as e:
        # If transcripts are disabled, notify the user
        st.error("Sorry, this video does not have available captions.")
        return None
    except Exception as e:
        # Handle any other exceptions that may occur
        st.error(f"An error occurred: {str(e)}")
        return None

# Function to generate content using Google Gemini
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text

# Streamlit UI
st.title("YouTube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Detailed Notes"):
    transcript_text = extract_transcript_details(youtube_link)
    
    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)
