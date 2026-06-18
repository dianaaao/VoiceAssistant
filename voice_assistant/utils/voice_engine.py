import edge_tts, time, asyncio, os, pygame, threading

pygame.mixer.init()
def speak_task(text):
    file_name = f"voice_{round(time.time())}.mp3"
    VOICE = "uk-UA-OstapNeural"

    try:   
        async def generate():
            communicate = edge_tts.Communicate( # створення обєкту що вдповідає за синтез мовлення
                text = text,
                voice = VOICE, # find all voice in teminal: edge-tts --list-voices
            )
            await communicate.save(file_name)

        loop = asyncio.new_event_loop() # створити новий цикл подій
        asyncio.set_event_loop(loop) #
        loop.run_until_complete(generate()) #
        loop.close() # закотває цикл подій, після завершення роботи

        if os.path.exists(file_name): # перевірка чи існує файл
            pygame.mixer.music.load(file_name)
            pygame.mixer.music.play
            while pygame.mixer.music.get_busy(): # чи програв наш файлик
                time.sleep(0.5)
            pygame.mixer.music.stop()

            pygame.mixer.music.unload() #відвантажити, очищаемо завантажений файл
            time.sleep(0.5)

            os.remove(file_name) #видалення файлу
            print(f"File {file_name} deleted!")
    except Exception as error:
        print(error)

def speak_async(text):
    threading.Thread( #создали новий потік, обгортку для спик таск
            target = speak_task,
            args = [text], # або (text,)
            daemon = True # автоматом завершиться коли завершиться виконання програма
        ).start()  # запуск
    
speak_task("Привіт це тест синхронного озвучування")
print("тест speak_task")

speak_async("Привіт це тест асинхронного озвучування")
print("тест speak_async")

time.sleep(5)
print("тест завершено")