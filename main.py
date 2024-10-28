import flet as ft
import os
import requests
from bs4 import BeautifulSoup
import subprocess

def main(page: ft.Page):

    python_executable = "venv/Scripts/python"
    # Название title
    page.title = "MIREA"
    # изменение стиля текста
    page.fonts = {
        "Roboto": "https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap"
    }
    # Создаем контейнер для изображения
    image = ft.Container(
        ft.Image(
            src="https://samara.rybolov66.ru/wa-data/public/site/img/%D1%82-%D0%B1%D0%B0%D0%BD%D0%BA.png",
            width=350,
            height=250,
        ),
        margin=ft.margin.only(left=70, top=30),
    )

    # Создаем контейнер для изображения dady
    dady = ft.Container(
        ft.Image(
            src=f"dady.png",
            width=900,
            height=1300,
        ),
        margin=ft.margin.only(left=70, top=50),
    )
    # Создаем контейнер для изображения dady
    maintext = ft.Container(
        content=ft.Text(
            "🌟 Представьте себе уютный вечер, когда отец и дочь-подросток сидят вместе, обсуждая новости и статьи. 📰\n\n"
            "Она задает вопросы, а он отвечает, превращая сложные темы в доступные и интересные истории. 🗣️\n\n"
            "Такие беседы помогают подросткам понять мир вокруг, делая обучение увлекательным и полезным. 🌍\n\n",
            size=30,
            color="white",
            font_family="Roboto",
            weight="bold",
        ),
        width=900,
        height=380,
        bgcolor="black",
        border_radius=20,
        padding=20,
        alignment=ft.alignment.center,
        margin=ft.margin.only(left=1000, top=70),
    )

    containerbutton = ft.Container(
        width=900,
        height=700,
        bgcolor="white",
        border_radius=20,
        padding=20,
        margin=ft.margin.only(left=1000, top=450),
    )

    # Функция для обработки выбранных файлов
    def on_file_picked(e: ft.FilePickerResultEvent):
        if e.files:
            file_path = e.files[0].path
            subprocess.run([python_executable, "main_result.py", file_path])

    # Компонент FilePicker
    file_picker = ft.FilePicker(on_result=on_file_picked)
    page.overlay.append(file_picker)

    # Функция для выбора только txt файлов
    def on_pick_file_txt(e):
        file_picker.pick_files(allow_multiple=False, allowed_extensions=["txt"])

    # Кнопка для выбора txt файлов
    pick_file_txt = ft.Container(
        ft.ElevatedButton(
            "Загрузить txt",
            on_click=on_pick_file_txt,
            width=250,
            height=90,
            color="white",
            bgcolor="black",
            style=ft.ButtonStyle(text_style=ft.TextStyle(size=30)),
        ),
        margin=ft.margin.only(left=1600, top=520),
    )

    # Функция для выбора только pdf файлов
    def on_pick_file_pdf(e):
        file_picker.pick_files(allow_multiple=False, allowed_extensions=["pdf"])

    # Кнопка для выбора pdf файлов
    pick_file_pdf = ft.Container(
        ft.ElevatedButton(
            "Загрузить pdf",
            on_click=on_pick_file_pdf,
            width=250,
            height=90,
            color="white",
            bgcolor="black",
            style=ft.ButtonStyle(text_style=ft.TextStyle(size=30)),
        ),
        margin=ft.margin.only(left=1600, top=720),
    )

    def on_button_click(e):
        url = input_field.content.value
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                # Извлекаем текст из всех элементов, которые обычно содержат текстовое содержимое
                text_elements = soup.find_all(
                    ["p", "div", "span", "h1", "h2", "h3", "h4", "h5", "h6"]
                )
                text = " ".join([element.get_text() for element in text_elements])
                subprocess.run([python_executable, "main_result.py", text])
            else:
                result_text.content.value = f"Error: {response.status_code}"
        except requests.exceptions.RequestException as e:
            result_text.content.value = f"Error: {e}"
        page.update()

    # Поле для ввода URL
    input_field = ft.Container(
        ft.TextField(label="Enter URL", width=300),
        margin=ft.margin.only(left=1570, top=900),
    )

    # Текст для отображения результата
    result_text = ft.Container(
        ft.Text(value="", selectable=True), margin=ft.margin.only(left=1200, top=1070)
    )

    # Кнопка для начала чтения контента
    button_url = ft.Container(
        ft.ElevatedButton(
            "Загрузить статью",
            on_click=on_button_click,
            width=300,
            height=90,
            color="white",
            bgcolor="black",
            style=ft.ButtonStyle(text_style=ft.TextStyle(size=30)),
        ),
        margin=ft.margin.only(left=1570, top=960),
    )

    mirea = ft.Container(
        ft.Text(
            value="MIREA team ❤️",
            size=60,
            color="#333332",
            font_family="Roboto",
            weight="bold",
        ),
        margin=ft.margin.only(left=500, top=108),
    )
    # линия разъединия
    line1 = ft.Container(
        width=900,
        height=2,
        bgcolor="#8c8c8c",
        margin=ft.margin.only(left=1000, top=670),
    )
    # линия разъединия
    line2 = ft.Container(
        width=900,
        height=2,
        bgcolor="#8c8c8c",
        margin=ft.margin.only(left=1000, top=870),
    )

    # правила для txt
    rule_txt = ft.Container(
        content=ft.Text(
            "Наша система — это как вечеринка 🥳, но только для файлов в формате TXT. Если у вас есть PDF, DOC или JPEG, они будут как те, кто пришел на вечеринку в костюме клоуна 🤡 — их просто не пустят.",
            size=20,
            color="black",
            font_family="Roboto",
            weight="bold",
        ),
        width=550,
        height=300,
        alignment=ft.alignment.center,
        margin=ft.margin.only(left=1010, top=400),
    )

    # правила для pdf
    rule_pdf = ft.Container(
        content=ft.Text(
            "Зачем пытаться загружать txt? 🤔\nНе получится! 🤣\nНормальные люди загружают pdf, Попробуешь?...",
            size=20,
            color="black",
            font_family="Roboto",
            weight="bold",
        ),
        width=550,
        height=300,
        alignment=ft.alignment.center,
        margin=ft.margin.only(left=990, top=620),
    )

    # правила для article
    rule_article = ft.Container(
        content=ft.Text(
            "Отец и дочь не любят когда им дают не рабочие url ссылки. Когда интернет-ссылка не существует, дочь начинает плакать 😭, а отец выписывает ошибку текстом ниже❗⚠️",
            size=20,
            color="black",
            font_family="Roboto",
            weight="bold",
        ),
        width=550,
        height=300,
        alignment=ft.alignment.center,
        margin=ft.margin.only(left=1010, top=820),
    )

    # Основной контейнер с использованием Stack
    main_container = ft.Container(
        width=2120,
        height=1800,
        bgcolor="#ffdd30",  # задний фон
        margin=ft.margin.all(-100),
        content=ft.Stack(
            controls=[
                image,
                dady,
                maintext,
                containerbutton,
                pick_file_txt,
                pick_file_pdf,
                input_field,
                button_url,
                result_text,
                mirea,
                line1,
                line2,
                rule_txt,
                rule_pdf,
                rule_article,
            ]
        ),
    )

    # Добавляем основной контейнер на страницу
    page.add(main_container)

    # Обновляем страницу для отображения
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
'''
браузер
if __name__ == "__main__":
    ft.app(target=main, port=8550, view=ft.AppView.WEB_BROWSER)
'''