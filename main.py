import speech_recognition as sr
from langdetect import detect
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
from playsound import playsound

# 🎯 Set target language (ISO 639-1 code: "hi", "fr", "es", etc.)
TARGET_LANG = "ja"  # Change to any language you want

recognizer = sr.Recognizer()

def speak(text, lang):
    """Speak the translated text using gTTS"""
    try:
        print(f"🔊 Speaking ({lang}): {text}")
        tts = gTTS(text=text, lang=lang)
        filename = "temp_audio.mp3"
        tts.save(filename)
        playsound(filename)
        os.remove(filename)
    except Exception as e:
        print(f"❌ TTS Error: {e}")

def translate_text(text, target_lang):
    """Detect the input language and translate"""
    try:
        source_lang = detect(text)
        print(f"🌍 Detected Language: {source_lang.upper()} ➡ {target_lang.upper()}")
        translated = GoogleTranslator(source=source_lang, target=target_lang).translate(text)
        return translated
    except Exception as e:
        print(f"❌ Translation error: {e}")
        return "Translation failed."

def main():
    print(f"\n🗣 Real-Time Multilingual Translator - Target: {TARGET_LANG.upper()}")
    print("🎤 Say something (say 'exit' to quit)...\n")

    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("🎧 Listening...")
                audio = recognizer.listen(source, timeout=5)

            print("🧠 Recognizing speech...")
            spoken_text = recognizer.recognize_google(audio)
            print(f"🗨 You said: {spoken_text}")

            if "exit" in spoken_text.lower():
                print("👋 Exiting translator.")
                speak("Goodbye!", TARGET_LANG)
                break

            translated_text = translate_text(spoken_text, TARGET_LANG)
            print(f"🌐 Translated: {translated_text}")
            speak(translated_text, TARGET_LANG)

        except sr.UnknownValueError:
            print("🤷 Could not understand audio.")
            speak("Sorry, I didn't catch that.", TARGET_LANG)
        except sr.RequestError as e:
            print(f"🔌 API error: {e}")
        except Exception as e:
            print(f"❗ Unexpected error: {e}")
            speak("Something went wrong.", TARGET_LANG)

if __name__ == "__main__":
    main()