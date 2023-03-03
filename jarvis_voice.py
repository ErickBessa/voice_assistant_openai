import openai
import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # 0 is for the male voice
engine.setProperty('language', 'en-us')


engine.say('Hello, how are you?')
engine.runAndWait()

import speech_recognition as sr
import time

# Set your OpenAI API Key
openai.api_key = "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"

#Initialize the text-to-speech engine
engine = pyttsx3.init()

def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print("Skipping unknown error")
        
def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt = prompt,
        max_tokens = 1024,
        n = 1,
        stop = None,
        temperature = 0.5,
    )
    return response["choices"] [0] ["text"]
  
def speak_text(text):
    engine.say(text)
    engine.runAndWait()
    
def main():
    while True:
        # Wait for user to say "jarvis"
        print("Say 'Jarvis' to start recoding your question...")
        with sr.Microphone() as source:
              recognizer = sr.Recognizer()
              audio = recognizer.listen(source)
              try:
                  transcription = recognizer.recognize_google(audio)
                  if transcription.lower() == "jarvis":
                      # Record audio
                      filename = "input.wav"
                      print("Say your question...")
                      with sr.Microphone() as source:
                            recognizer = sr.Recognizer()
                            source.pause_threshold = 1
                            audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                            with open(filename, 'wb') as f:
                                f.write(audio.get_wav_data())
                      # Transcribe audio to text
                      text = transcribe_audio_to_text(filename)
                      if text:
                          print(f"Yosef: {text}")
                          
                          #Generate response using GPT-3
                          response = generate_response(text)
                          print(f"Jarvis says: {response}")
                          
                          # Read the response using text-to-speech
                          speak_text(response)
              except Exception as e:
                  print("An error occurred: {}".format(e))
                  
if __name__ == "__main__":
    main()
    