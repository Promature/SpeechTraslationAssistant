from flask import Flask, render_template, request, redirect, url_for
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import playsound
import os

app = Flask(__name__)

# Define the absolute path to save the audio file
AUDIO_DIRECTORY = 'translatedAudio'
AUDIO_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),AUDIO_DIRECTORY, "hello.mp3")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Handle the POST request from the form
        input_language = request.form.get("input_language")
        output_language = request.form.get("output_language")

        recognizer = sr.Recognizer()

        with sr.Microphone() as source: #listen to audio
            print("Speak Now")
            recognizer.adjust_for_ambient_noise(source,duration=0.2)
            voice = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(voice, language=input_language)
            print("You said:", text)

            translator = Translator()
            translation = translator.translate(text, dest=output_language)#translated text
            print("Translation:", translation.text)
            # if(translation.text=="Marathi"):
            #     translation.text="This Translation is valid but for testing purpose this is done Urdu"

            converted_audio = gTTS(translation.text, lang=output_language)
            converted_audio.save(AUDIO_PATH)
            playsound.playsound(AUDIO_PATH)

            return render_template("new.html", translation=translation.text)

        except sr.UnknownValueError:
            error_message = "Google Speech Recognition could not understand audio"
            return render_template("new.html", error=error_message)

        except sr.RequestError as e:
            error_message = "Could not request results from Google Speech Recognition service; {0}".format(e)
            return render_template("new.html", error=error_message)

    return render_template("new.html")

if __name__ == "__main__":
    app.run(debug=True)
