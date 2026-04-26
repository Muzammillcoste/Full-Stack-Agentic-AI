import speech_recognition as sr
from dotenv import load_dotenv
from openai import OpenAI
import os
import base64
import io
import wave
import winsound
from google import genai
from google.genai import types

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
Google_client = genai.Client()

def SYSTEM_PROMPT():
    return """
    You are a helpful assistant that listens to the user's voice input and provides a response based on the content of the input. 
    Your responses should be concise and relevant to the user's query. 
    Always try to provide useful information or assistance based on what the user says.
    
    IMPORTNANT: you must provide responses in talking style,
    """

def main():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 2

        print("Listening...")
        audio = r.listen(source)    

        # recognize speech using Google Speech Recognition
        stt = r.recognize_google(audio)
        print("You said: " + stt) 

        response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT()},
            {"role": "user", "content": stt}
        ]
    )  
        
        ai_response = response.choices[0].message.content

        response = Google_client.models.generate_content(
        model="gemini-3.1-flash-tts-preview",
        contents=ai_response,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                    voice_name='Kore',
                    )
                )
            ),
        )
        )
        print("AI:", ai_response)

        part = response.candidates[0].content.parts[0]
        audio_data = part.inline_data.data

        if isinstance(audio_data, str):
            audio_data = base64.b64decode(audio_data)

        wav_buffer = io.BytesIO()
        with wave.open(wav_buffer, "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(24000)
            wav_file.writeframes(audio_data)

        winsound.PlaySound(wav_buffer.getvalue(), winsound.SND_MEMORY)

if __name__ == "__main__":    
    main()