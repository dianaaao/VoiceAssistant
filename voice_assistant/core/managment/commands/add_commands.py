import time, speech_recognition as sr

from utils.voice_engine import speak_task
from voice_assistant.core.models import AppCommand

def get_voice_input():
    time.sleep(0.5)
    try:
        with sr.Microphone(device_index = 1) as source: #використовуємо миктофон
            print("Listening...")
            recognise = sr.Recognizer()
            recognise.adjust_for_ambient_noise(source, 1)
            audio = recognise.listen(source, None, phrase_time_limit = 5)
        print("Recognasing")
        text = recognise.recognize_google(audio, language="uauk-UA") # відправляє у гугл для обробки аудіо (на укр мові - спілкування) 
                                                                     # накопичені дані на сервер для обробки, де вони аналізуються нейромережами
        return text
    except Exception as error:
        print(error)
        # speak_async(f"Помилка  {error}")
        # return ""

def add_new_command_voice():
    speak_task("Щоб додати команду скажіть ключове слово")
    keyword = get_voice_input()

    if not keyword:
        speak_task("I don`t hear anything. Try again!")
        return
    
    # отримати підтвердження
    speak_task(f"Ваше слово {keyword}. Підтвердити?")
    confirm = get_voice_input()

    print(f"Assistant heard: {confirm}")
    if "підтвер" not in str(confirm):
        speak_task("The action canceled")
        return
    
    speak_task("Waiting for app name")
    app_name = get_voice_input()
    if not app_name:
        speak_task("I don`t hear anything. Try again!")
        return
    
    app_name = app_name.replace("крапка", ".").replace(" ", "")
    speak_task(f"Назва додатку {app_name}. Підтвердити?")

    confirm_app = get_voice_input()
    print(f"Асистент почув: {confirm_app}")

    if "підтвер" not in str(confirm_app):
        speak_task("Дію скасовано")
        return
    

    AppCommand.objects.create( #створює запис у базі даних 
        keyword = keyword,
        app_name = app_name,
    ) 
    speak_task(f"Ваша команда {keyword} успішно додана")
    print(f"Збережено: {keyword} - {app_name}")