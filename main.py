import json
import os
import re
import shutil
import subprocess

while True:
    settings_path = os.path.join(os.path.dirname(__file__), "settings.json")
    if os.path.isfile(settings_path):
        with open("settings.json", 'r') as settings_file:
            config = json.load(settings_file)
    if not os.path.isfile(settings_path):
        print("Введите путь к папке модов")
        while True:
            mod_folder = input()
            if os.path.isdir(mod_folder):
                settings_mod_folder = os.path.normpath(mod_folder)
                break
            else:
                print("Неверный путь, попробуйте ещё раз")
        print("Введите путь к SteamCMD")
        while True:
            steamcmd_folder = input()
            if os.path.isdir(steamcmd_folder):
                settings_steam_folder = os.path.normpath(steamcmd_folder)
                break
            else:
                print("Неверный путь, попробуйте ещё раз")
        with open("settings.json", 'w') as settings_file:
            config = {"mod_folder": mod_folder, "steamcmd_folder": steamcmd_folder}
            json.dump(config, settings_file, indent=4)
        print("Всё настроено!")

    mod_folder = config.get("mod_folder").replace("\\", "/")
    steamcmd_folder = config.get("steamcmd_folder")
    steamcmd_folder_mods = steamcmd_folder.replace("\\", "/") + "/steamapps/workshop/content/294100/"
    command = ""
    download_one = False
    update_all = False
    del_all = False
    os.makedirs(mod_folder, exist_ok=True)
    os.makedirs(steamcmd_folder, exist_ok=True)
    modlist = os.listdir(mod_folder)
    modlist = [item for item in modlist if item.isdigit()]

    while True:
        print("Скачать один мод, обновить все или удалить все моды?(1 или 2 или 3)")
        answer = input()
        if answer == "1":
            download_one = True
            break
        if answer == "2":
            update_all = True
            break
        if answer == "3":
            del_all = True
            break

    if download_one:
        while True:
            print("Введите ссылку на мод")
            workshop_id = input()
            if "https://steamcommunity.com/sharedfiles/filedetails/?id=" in workshop_id or "https://steamcommunity.com/workshop/filedetails/?id=":
                pattern = r'id=(\d+)'
                match = re.search(pattern, workshop_id)
                if match:
                    workshop_id = match.group(1)
                steamcmd_download = steamcmd_folder + f"/steamcmd.exe +login anonymous +workshop_download_item 294100 {workshop_id} validate +quit"
                subprocess.call(steamcmd_download, shell=True)
                if workshop_id in modlist:
                    shutil.rmtree(mod_folder + "/" + workshop_id)
                shutil.copytree(steamcmd_folder_mods + workshop_id, mod_folder + "/" + workshop_id)
                print("Мод успешно установлен")
                break
            else:
                print("Неверное значение")

    if update_all:
        if not modlist:
            print("Модов нет")
        else:
            for index in modlist:
                command += " +workshop_download_item 294100 " + index + " validate"
            steamcmd_update = steamcmd_folder + f"/steamcmd.exe +login anonymous {command} +quit"
            subprocess.call(steamcmd_update, shell=True)

            print("Моды скачаны, идёт установка...")
            for item in modlist:
                item_path = mod_folder + "/" + item
                shutil.rmtree(item_path)

            if os.path.exists(steamcmd_folder_mods):
                for index in modlist:
                    source_path = os.path.join(steamcmd_folder_mods, index)
                    destination_path = os.path.join(mod_folder, index)
                    if os.path.isdir(source_path):
                        shutil.copytree(source_path, destination_path)
                    else:
                        shutil.copy2(source_path, destination_path)
            print("Моды обновлены")

    if del_all:
        for item in modlist:
            item_path = os.path.join(mod_folder, item)
            shutil.rmtree(item_path)
        print("Моды удалены")
