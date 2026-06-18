from django.core.management.base import BaseCommand
from models import *
from utils import *
import platform, os, subprocess, speech_recognition as sr

from core.managment.commands.add_commands import add_new_command_voice

APP_CASH = {}
class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f"Assitant was launched.."))
        recognizer = sr.Recognizer() #розпознаватель
        micro = sr.Microphone() 

        with micro as source: # відкриваємо мікро для запису
            self.stdout.write(self.style.SUCCESS(f"Setting background noise "))
            recognizer.adjust_for_ambient_noise(source, 1) # щоб убрати шум, принима микро и прибира шум
            self.stdout.write(self.style.SUCCESS(f"You said: {command_text}"))
            self.process_command(command_text, source)

            while True:
                try:
                    audio = recognizer.listen(source, None, 5) #phrase_time_limit
                    command_text = recognizer.recognize_google(audio, language="uauk-UA")
                    self.stdout.write(self.style.SUCCESS(f"Listening... microfon activated"))
                    self.process_command(command_text, source)

                except sr.UnknownValueError as error:
                    print(error)
                except Exception as error:
                    self.stdout.write(self.style.ERROR(f"Error: {error}"))

    def process_command(self, text, source): # соурс за мікрофон
        text = text.lower().strip()# видалить усі пробіли

        if "додати команду" in text:
            add_new_command_voice()
            return

        if "відкрий" not in text:
            # перевіряем чи є цей текст, команда є в нашей моделе, если есть то озвучиваем ответ
            for resp in VoiceResponse.objects.all():
                if resp.keyword and resp.keyword.lower() in text:
                    speak_async(resp.response)
                    return 
            return
        
        found_app = None
        for app in AppCommand.objects.all():
            if app.keyword and app.keyword.lower() in text:
                found_app = app
                break

            if not found_app:
                speak_async("Я не знайшов такої програми")
                return
            
            if found_app.app_name in APP_CASH and os.path.exists(APP_CASH[found_app.app_name]):
                speak_async(f"Відкриваю {found_app.app_name}")
                self.launch_app(APP_CASH[found_app.app_name])
                return
            speak_async(f"Шукаю {found_app.app_name}")

        def find_and_launch():
            found_path = find_app_path(found_app.app_name)
            if found_path:
                APP_CASH[found_app.app_name] = found_path
                found_app.path = found_path # змінюємо шлях в бд
                found_app.save() # зберігати змінні в бд
                speak_async(f"Знайшов додаток за шляхом {found_path}")
                self.launch_app(found_path)
            else:
                speak_async(f"Я не зміг знайти шлях до програми....")

        threading.Thread(
            target = find_and_launch,
            daemon = True,
        ).start()
            

    def launch_app(self, path):
        try:
            system = platform.system()
            if system == "Windows":
                os.startfile(path)
            elif system == "Darwin":
                subprocess.Popen(["open", path]) # відкриває файл
            else:
                subprocess.Popen([path])
        except Exception as error:
            self.stdout.write(self.style.ERROR(f"Error: {error}"))