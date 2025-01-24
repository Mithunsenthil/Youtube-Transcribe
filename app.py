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
import whisper
from openai import OpenAI
import streamlit as st
from audio_recorder_streamlit import audio_recorder


def transcribe(audio_file_path):
    """
    Transcribe audio using Whisper.
    :param audio_file_path: Path to the audio file
    :return: Transcribed text
    """
    model = whisper.load_model("base")
    result = model.transcribe(audio_file_path)
    return result["text"]


def save_audio_file(audio_bytes, file_extension):
    """
    Save audio bytes to a file with the specified extension.
    :param audio_bytes: Audio data in bytes
    :param file_extension: The extension of the output audio file
    :return: The name of the saved audio file
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"audio_{timestamp}.{file_extension}"

    with open(file_name, "wb") as f:
        f.write(audio_bytes)

    return file_name


def main():
    """
    Main function to run the Whisper Transcription app.
    """
    st.title("Whisper Transcription")

    tab1, tab2 = st.tabs(["Record Audio", "Upload Audio"])

    audio_file_path = None

    # Record Audio tab
    with tab1:
        audio_bytes = audio_recorder()
        if audio_bytes:
            st.audio(audio_bytes, format="audio/wav")
            audio_file_path = save_audio_file(audio_bytes, "wav")

    # Upload Audio tab
    with tab2:
        audio_file = st.file_uploader("Upload Audio", type=["mp3", "wav", "m4a"])
        if audio_file:
            file_extension = audio_file.type.split('/')[1]
            audio_file_path = save_audio_file(audio_file.read(), file_extension)

    # Transcribe button action
    if audio_file_path and st.button("Transcribe"):
        try:
            transcript_text = transcribe(audio_file_path)

            # Display the transcript
            st.header("Transcript")
            st.write(transcript_text)

            # Save the transcript to a text file
            with open("transcript.txt", "w") as f:
                f.write(transcript_text)

            # Provide a download button for the transcript
            st.download_button("Download Transcript", transcript_text)

        except Exception as e:
            st.error(f"An error occurred during transcription: {str(e)}")


if __name__ == "__main__":
    # Set up the working directory
    working_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(working_dir)

    # Run the main function
    main()
