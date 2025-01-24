# import yfinance as yf
# import streamlit as st

# st.write("""
# # Simple Stock Price App

# Shown are the stock **closing price** and ***volume*** of Google!

# """)

# # https://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75
# #define the ticker symbol
# tickerSymbol = 'GOOGL'
# #get data on this ticker
# tickerData = yf.Ticker(tickerSymbol)
# #get the historical prices for this ticker
# tickerDf = tickerData.history(period='1d', start='2010-5-31', end='2020-5-31')
# # Open	High	Low	Close	Volume	Dividends	Stock Splits

# st.write("""
# ## Closing Price
# """)
# st.line_chart(tickerDf.Close)
# st.write("""
# ## Volume Price
# """)
# st.line_chart(tickerDf.Volume)
import os
import sys
import datetime
import openai
import dotenv
import streamlit as st
import warnings

from audio_recorder_streamlit import audio_recorder

# Suppress specific warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# Import API key from .env file
dotenv.load_dotenv()
openai.api_key = "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"


def transcribe(audio_file):
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript


def save_audio_file(audio_bytes, file_extension):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"audio_{timestamp}.{file_extension}"
    with open(file_name, "wb") as f:
        f.write(audio_bytes)
    return file_name


def transcribe_audio(file_path):
    with open(file_path, "rb") as audio_file:
        transcript = transcribe(audio_file)
    return transcript["text"]


def main():
    st.title("Whisper Transcription on Streamlit")

    # Create tabs for recording or uploading audio
    tab1, tab2 = st.tabs(["Record Audio", "Upload Audio"])

    audio_bytes = None
    if "audio_files" not in os.listdir():
        os.makedirs("audio_files")

    with tab1:
        audio_bytes = audio_recorder()
        if audio_bytes:
            st.audio(audio_bytes, format="audio/wav")
            save_audio_file(audio_bytes, "mp3")

    with tab2:
        audio_file = st.file_uploader("Upload Audio", type=["mp3", "mp4", "wav", "m4a"])
        if audio_file:
            file_extension = audio_file.type.split('/')[1]
            save_audio_file(audio_file.read(), file_extension)

    # Transcription action
    if st.button("Transcribe"):
        try:
            # Check for audio files
            audio_files = [f for f in os.listdir("audio_files") if f.startswith("audio")]
            if not audio_files:
                st.error("No audio files found for transcription. Please record or upload an audio file.")
                return

            # Find the newest audio file
            audio_file_path = max(
                [os.path.join("audio_files", f) for f in audio_files],
                key=os.path.getctime,
            )

            # Transcribe the audio file
            transcript_text = transcribe_audio(audio_file_path)
            st.header("Transcript")
            st.write(transcript_text)

            # Save and allow downloading the transcript
            with open("transcript.txt", "w") as f:
                f.write(transcript_text)
            st.download_button("Download Transcript", transcript_text)

        except Exception as e:
            st.error(f"An error occurred during transcription: {e}")

if __name__ == "__main__":
    working_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(working_dir)
    main()

