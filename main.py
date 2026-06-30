import flet as ft
import urllib.request
import json
import os
import platform

def main(page: ft.Page):
    page.title = "Minecraft Bedrock Addon Manager"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 450
    page.window_height = 650
    
    JSON_URL = "https://raw.githubusercontent.com/HIKIDEMONMIF247/minecraft-addons/main/addons.json"
    ALL_ADDONS = []
    
    list_view = ft.ListView(expand=True, spacing=10)
    count_text = ft.Text(value="Загрузка...", size=14, color=ft.Colors.BLUE_GREY_300)

    def on_download_click(e):
        url = e.control.data
        if not url:
            return
            
        # Умный выбор папки Загрузок в зависимости от устройства
        if platform.system() == "Windows":
            save_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        else:
            # Для Android (работает в Termux при наличии прав на память)
            save_folder = "/sdcard/Download"
        
        try:
            if not os.path.exists(save_folder):
                os.makedirs(save_folder, exist_ok=True)
        except Exception:
            # Если на Android нет прав, сохраняем в локальную папку скрипта
            save_folder = "."
            
        file_name = url.split("/")[-1]
        full_path = os.path.join(save_folder, file_name)
        
        try:
            urllib.request.urlretrieve(url, full_path)
            
            # Старый надежный snack_bar для твоей версии Flet
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Скачано в: {save_folder}"),
                bgcolor=ft.Colors.GREEN_700
            )
        except Exception as ex:
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Ошибка скачивания: {ex}"),
                bgcolor=ft.Colors.RED_700
            )
            
        page.snack_bar.open = True
        page.update()

    def render_addons(search_text=""):
        list_view.controls.clear()
        visible_count = 0
        
        for item in ALL_ADDONS:
            title = item.get("title", "Без названия")
            desc = item.get("desc", "Нет описания")
            file_url = item.get("url", "") 
            
            if search_text.lower() in title.lower() or search_text.lower() in desc.lower():
                visible_count += 1
                
                list_view.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Text(title, size=20, weight="bold"),
                            ft.Text(desc, color=ft.Colors.BLUE_GREY_200),
                            ft.ElevatedButton(
                                "Скачать", 
                                data=file_url, 
                                on_click=on_download_click
                            )
                        ]),
                        padding=15,
                        bgcolor=ft.Colors.BLUE_GREY_900,
                        border_radius=10
                    )
                )
                
        count_text.value = f"Найдено дополнений: {visible_count}"
        page.update()

    def on_search_change(e):
        render_addons(search_field.value)

    search_field = ft.TextField(
        label="Поиск дополнений...",
        on_change=on_search_change,
        border_radius=10
    )

    try:
        req = urllib.request.Request(JSON_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as url:
            ALL_ADDONS = json.loads(url.read().decode('utf-8'))
    except Exception as ex:
        ALL_ADDONS = [{"title": "Ошибка сети", "desc": f"Не удалось загрузить: {ex}", "url": ""}]

    page.add(
        ft.Text("Каталог Bedrock", size=28, weight="bold"),
        count_text,
        search_field,
        ft.Divider(),
        list_view
    )
    
    render_addons()

ft.app(target=main)

