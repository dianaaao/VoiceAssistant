import os, platform, subprocess, winreg
           # на якому девайсі 
                     # запускає команду
                                 # доступ до регистров виндовс

def find_in_path(app_name: str):
    try:
        cmd = ["where", app_name] if platform.system() == "Windows" else ["which", app_name]
                                     # визначає назву операційної системи
        result = subprocess.run( # запускає системну команду
            cmd, 
            capture_output = True,
            text = True
        )
        if result.returncode == 0:
            return result.stdout.splitlines()[0] 
                          # результата команди, (здорова строка з логами) 
                                 # розбивае на список рядків
    except Exception as error:
        print(error)

    return None


def find_in_registry(app_name: str):
    if platform.system() != "Windows":
        return None
    try:
        reg_path = [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\App paths", # путь до списку приложений
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\App paths"
        ]
        for reg in reg_path:
            try:
                key = winreg.OpenKey( #відкриває гілку для чтения, для прочтения инфи (без можливості зміни)
                    winreg.HKEY_LOCAL_MACHINE, # путь куди стучаться, базова гілка налаштувань компьютера
                    reg, # сам путь (якийсь з)
                )
                count = 0
                while True:
                    try:
                        # название нашого подключа
                        sub_key_name = winreg.EnumKey( # повертає по індексу регістра(ключу) назву підрозділу(підпапка)
                            key, 
                            count
                        ) 
                    except OSError:
                        break
                    if app_name.lower() in sub_key_name.lower():
                        sub_key = winreg.OpenKey(
                            key,
                            sub_key_name
                        )
                        # диструкторизация 
                        # значення, айди
                        value, _ = winreg.QueryValueEx( # повертає шлях по замовчуванню
                            sub_key, # ключ доступа
                            None # за замовчуванням (с розширением файлика)
                        )
                        return value
                    count += 1
                    
            except Exception as error:
                print(error)
    except Exception as error:
        print(error)


# знаходе ярлики на виндовс
def find_in_start_menu(app_name: str):
    if platform.system() != "Windows":
        return None
    
    start_paths = [
        os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs"), # подключає увесь шлях до ап дата (для конкретного юзера), треба доступ адміна
        os.path.expandvars(r"%PROGRAMDATA%\Microsoft\Windows\Start Menu\Programs") #(для інших любих юзерів)
    ]

    for base in start_paths:
        for root, _, files in os.walk(base):
            for file in files:
                if file.lower().startswith(app_name.lower()) and file.endswith(".lnk"):
                    return os.path.join(root, file)

# проверка спеціаних місць після скачування файлів
def find_in_common_dirs(app_name: str):
    system = platform.system()
    if system == "Windows":
        drives = []
        for code in range(65, 90):
            drive_letter = chr(code) #перероблює у букву
            path = f"{drive_letter}:\\"
            if os.path.exists(path):
                drives.append(path)

        base_dirs = [
            os.environ.get( # словарь, з усіма змінними середовища системи 
                "ProgramFiles", # ключ
                "" # значення, якщо немає ключа
            ), 
            os.environ.get( # словарь, з усіма змінними середовища системи 
                "ProgramFiles(x86)",
                ""
            ),
            os.path.expanduser( # підтягує шлях до апп дата, вже за юзером
                "~/AppData/Local"
            ),
            os.path.expanduser( # 
                "~/AppData/Roaming"
            )  
        ] + drives

        for base in base_dirs:
            if not os.path.exists(base):
                continue
            
            for root, _, files in os.walk(base):
                for file in files:
                    if file.lower() == app_name.lower() + ".exe":
                        return os.path.join(root, file)
                # заглушка щоб ограничить вході в папку  
                if root.count(os.sep) - base.count(os.sep) > 3:
                    drives[:] = []

    else:
        
        base_dirs = [
            "/usr/bin",
            "/usr/local/bin", 
            "/Applications", 
            "/System/Applications",
            os.path.expanduser("~/Applications")
        ]
        
        for base in base_dirs:
            if not os.path.exists(base):
                continue
            
            for item in os.listdir(base):
                if item.lower().startswith(app_name.lower()):
                    full_path = os.path.join(base, item)
                    
                if item.endswith(".app"):
                    exe_path = os.path.join(full_path, "Contents", "MacOS")
                    if os.path.exists(exe_path):
                        files = os.listdir(exe_path)
                        if files:
                            return os.path.join(exe_path, files[0])
                    return full_path
                
                if os.path.isfile(full_path):
                    return full_path


def find_app_path(app_name: str):
    app_name = app_name.lower().replace(".exe", "").replace(".app", "")

    path = find_in_path(app_name)
    if path:
        return path
    
    path = find_in_registry(app_name)
    if path:
        return path

    path = find_in_common_dirs(app_name)
    if path:
        return path

    path = find_in_start_menu(app_name)
    if path:
        return path
    
    return None


test_apps = [
    'word',
    'cmd',
    'steam',
    'discord',
    'chrome',
    'telegram'
]

for app in test_apps:
    result = find_app_path(app)
    print(app, ': ' , result)


# \\\\\\\\\\\\\\\\\\\\
# \\\\\\\\\\\\\\\\\\\\\\\