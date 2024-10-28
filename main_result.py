import flet as ft
import sys
import os
import pygame
import threading
import time
from transformers import pipeline
import fitz
from dialog.synthes import synth_dialogue

import dialog as oaid
from openai import OpenAI


# Загрузка звукового файла
pygame.init()
sound = pygame.mixer.Sound('synth_audio13.wav')

def main(page: ft.Page):
    page.title = "MIREA Result"
    page.fonts = {
        "Roboto": "https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap"
    }

    # Получаем данные из аргументов командной строки
    if len(sys.argv) > 1:
        data = sys.argv[1]
    else:
        data = "No data provided"
    # сбор текста в pdf
    def extract_text_from_pdf(pdf_path):
        try:
            # Открываем PDF-документ
            pdf_document = fitz.open(pdf_path)

            # Извлекаем текст из каждой страницы
            text = ""
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                text += page.get_text()

            return text

        except Exception as e:
            return [f"An error occurred: {str(e)}"]
    # сбор текста в txt
    def read_txt_file(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content

    if data.endswith('.pdf'):
        data = [extract_text_from_pdf(data)]
    elif data.endswith('.txt'):
        data = [read_txt_file(data)]
    else:
        data = [data]     # сбор текста интернет-ссылки на статью

    '''
    client = OpenAI(api_key=os.environ.get("OPENAI_AK"), base_url="https://api.proxyapi.ru/openai/v1")
    oai_inst = oaid.OpenAiDialog(client, data[0])
    dialog = oai_inst.simulate_dialog_once()
    '''
    dialog = ['Дочь: Привет, папа! Как зародилась жизнь на земле?', 
              'Отец: В начале было слово и слово было у Бога и слово было Бог.', 
              'Дочь: Ладно, пока!', 
              ]
    def show_data(e):
        # Удаляем контейнер с кнопкой
        page.controls.remove(button_container)

        image = ft.Container(
            ft.Image(
                src="https://samara.rybolov66.ru/wa-data/public/site/img/%D1%82-%D0%B1%D0%B0%D0%BD%D0%BA.png",
                width=350,
                height=250,
            ),
            margin=ft.margin.only(left=70, top=30),
        )

        # Создаем контейнер для изображения dad
        dad = ft.Container(
            ft.Image(
                src=f"dad.jpg",
                width=373,
                height=746,
            ),
            margin=ft.margin.only(left=150, top=355),
        )
        # Создаем контейнер для изображения girl
        global girl_container
        girl_container = ft.Container(
            ft.Image(
                src=f"girl.jpg",
                width=373,
                height=746,
            ),
            margin=ft.margin.only(left=550, top=355),
        )

        global dialog_container
        dialog_container = ft.Container(
            content=ft.Text("",
                            font_family="Roboto",
                            color="white",
                            size=20),
            width=500,
            height=100,
            bgcolor="#212121",
            border_radius=20,
            padding=ft.padding.all(10),
            margin=ft.margin.only(left=1000, top=540),
        )

        global dialog_container2
        dialog_container2 = ft.Container(
            content=ft.Text("",
                            font_family="Roboto",
                            color="white",
                            size=20),
            width=500,
            height=100,
            bgcolor="#212121",
            border_radius=20,
            padding=ft.padding.all(10),
            margin=ft.margin.only(left=600, top=630),
        )

        global dialog_container3
        dialog_container3 = ft.Container(
            content=ft.Text("",
                            font_family="Roboto",
                            color="white",
                            size=20),
            width=500,
            height=100,
            bgcolor="#212121",
            border_radius=20,
            padding=ft.padding.all(10),
            margin=ft.margin.only(left=1000, top=740),
        )

        # Основной контейнер с использованием Stack
        global main_container
        main_container = ft.Container(
            width=2120,
            height=1800,
            bgcolor="#ffdd30",  # задний фон
            margin=ft.margin.all(-100),
            content=ft.Stack(
                controls=[
                    image,
                    dad,
                    girl_container,
                ]
            ),
        )
                # Основной контейнер с использованием Stack
        global error_file
        error_file = ft.Container(
            content=ft.Text(
                "🚨ОШИБКА!\nФАЙЛ НЕ ПРОШЁЛ ВЕРИФИКАЦИЮ",
                size=50,
                color="white",
                font_family="Roboto",
                weight="bold",
                text_align=ft.TextAlign.CENTER,
            ),
            width=900,
            height=380,
            bgcolor="black",
            border_radius=20,
            padding=20,
            alignment=ft.alignment.center,
            margin=ft.margin.only(left=640, top=300),
        )
        # Добавляем основной контейнер на страницу
        page.add(main_container)
        # Обновляем страницу для отображения
        page.update()

        # Запускаем таймер для перемещения девочки вправо каждую секунду
        threading.Thread(target=start_moving_girl, daemon=True).start()

    # плавное перемещение девочки
    def start_moving_girl():
        while girl_container.margin.left < 1300:
            time.sleep(0.0000007)
            move_girl_right()

        while girl_container.margin.left < 1400:
            time.sleep(0.00001)
            move_girl_right()

        while girl_container.margin.left < 1550:
            time.sleep(0.0009)
            move_girl_right()

        # проверка обрезается т.к больше 512 нельзя
        check = data[0][:510]
        # предварительно обученная модель для задачи классификации текста, основанная на архитектуре DistilBERT
        classifier = pipeline('text-classification', model='distilbert-base-uncased-finetuned-sst-2-english')
        results = classifier(check)
        # проверка что данные не имеют бессвязного текста
        if results[0]['label'] == 'NEGATIVE' and results[0]['score'] > 0.97:
            main_container.content.controls.append(error_file)
            page.update()
        else:
            # synth_dialogue(dialog, "./synth/dialogue.wav")
            # После завершения движения девочки, добавляем диалоговый контейнер через 1 секунду

            add_dialog_container()

    # передвигаем по margin(положению)
    def move_girl_right():
        # Получаем текущие отступы контейнера с изображением девочки
        current_margin = girl_container.margin
        # Увеличиваем отступ слева на 1 пиксель
        new_margin = ft.margin.only(left=current_margin.left + 1, top=current_margin.top)
        # Обновляем отступы контейнера
        girl_container.margin = new_margin
        # Обновляем страницу для отображения изменений
        page.update()

    def add_dialog_container():
        # Запускаем диалог
        sound.play()
        threading.Thread(target=show_dialog, args=(dialog,), daemon=True).start()

    def adjust_dialog_container_size(text, x):
        # Пример функции для изменения размера контейнера в зависимости от длины текста
        text_length = len(text)
        if text_length > 200:
            x.width = 500
            x.height = 200
        elif text_length > 150:
            x.width = 500
            x.height = 170
        elif text_length > 100:
            x.width = 500
            x.height = 150
        elif text_length > 50:
            x.width = 500
            x.height = 80
        else:
            x.width = 500
            x.height = 60
        page.update()

    def show_dialog(dialog):
        for line in dialog:
            if dialog.index(line) == 0:
                main_container.content.controls.append(dialog_container)
                page.update()
                dialog_container.content.value = ""
                for char in line[6:]:
                    dialog_container.content.value += char
                    adjust_dialog_container_size(dialog_container.content.value, dialog_container)
                    page.update()
                    time.sleep(0.05)
        
                time.sleep(0.3)
            elif dialog.index(line) == 1:
                main_container.content.controls.append(dialog_container2)
                page.update()

                dialog_container2.content.value = ""
                for char in line[6:]:
                    dialog_container2.content.value += char
                    adjust_dialog_container_size(dialog_container2.content.value, dialog_container2)
                    page.update()
                    time.sleep(0.065)
        
                time.sleep(0.7)
            elif dialog.index(line) == 2:
                main_container.content.controls.append(dialog_container3)
                page.update()

                dialog_container3.content.value = ""
                for char in line[6:]:
                    dialog_container3.content.value += char
                    adjust_dialog_container_size(dialog_container3.content.value, dialog_container3)
                    page.update()
                    time.sleep(0.05)
        
                time.sleep(1)
        

    # Создаем кнопку
    button = ft.ElevatedButton(
        text="Показать окно",
        width=900,
        height=400,
        on_click=show_data,
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,  # Цвет текста
            bgcolor=ft.colors.BLACK,  # Фоновый цвет кнопки
            padding=ft.padding.all(10),  # Отступы вокруг текста
            side=ft.BorderSide(1, ft.colors.RED_800),  # Граница кнопки
            shape=ft.RoundedRectangleBorder(radius=10),  # Закругленные углы
            overlay_color=ft.colors.YELLOW,
            text_style=ft.TextStyle(size=70),
        ),
    )

    # Создаем контейнер для кнопки с отступами
    button_container = ft.Container(
        content=button,
        margin=ft.margin.only(left=500, top=300),  # Отступы вокруг контейнера
    )

    # Добавляем контейнер с кнопкой на страницу
    page.add(button_container)

    # Обновляем страницу для отображения
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
