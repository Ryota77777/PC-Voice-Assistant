import pyttsx3
import pygame
import sys
import time
import webbrowser
import pyautogui
import requests
import sounddevice as sd
import soundfile as sf
import os
import tkinter as tk
from tkinter import messagebox
import threading

class CustomThread(threading.Thread):
  def run(self):
      # Создание главного окна

      root = tk.Tk()
      root.title("Простой интерфейс")

      # Создание метки
      label = tk.Label(root, text="Привет, мир!")
      label.pack()

      # Создание кнопки
      button = tk.Button(root, text="Нажми меня", command=on_button_click)
      button.pack()

      # Запуск основного цикла обработки событий
      root.mainloop()



def open_file(file_path):
    try:
        os.startfile(file_path)
        print(f"Файл {file_path} успешно открыт.")
    except Exception as e:
        print(f"Ошибка при открытии файла: {e}")

# Пример использования
def open_browser_with_actions(url):
    # Открываем браузер
    webbrowser.open(url)

    # Пауза, чтобы браузер успел открыться
    time.sleep(5)

    # Получаем размеры экрана
    screen_width, screen_height = pyautogui.size()

    # Перемещаем окно браузера в определенные координаты (например, в середину экрана)
    browser_width, browser_height = 800, 600
    x_position = (screen_width - browser_width) // 2
    y_position = (screen_height - browser_height) // 2

    pyautogui.moveTo(x_position, y_position, duration=1)
def on_button_click():
    messagebox.showinfo("Сообщение", "Вы нажали на кнопку")




def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def display_image(image_path, width, height):
    pygame.init()

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Отображение картинки")

    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, (width, height))

    running = True
    start_time = time.time()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(image, (0, 0))
        pygame.display.flip()

        # Добавляем тайм-дилей
        current_time = time.time()
        if current_time - start_time >= 8:  # Подождать 8 секунд
            running = False

    pygame.quit()

def set_shutdown_timer(seconds):
    command = f"shutdown -s -t {seconds}"
    os.system(command)

def cancel_shutdown_timer():
    os.system("shutdown /a")

def speaker(text: object) -> object:
    greeting = text
    print(greeting)
    speak(greeting)

def record_and_recognize_yandex(api_key, file_path, duration=3, sample_rate=16000):
    record_audio(file_path, duration, sample_rate)
    text = recognize_speech_yandex(api_key, file_path)
    return text

def record_audio(file_path, duration, sample_rate=16000):
    print("Идет запись голоса...")
    audio_data = sd.rec(int(sample_rate * duration), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    sf.write(file_path, audio_data, sample_rate)

def recognize_speech_yandex(api_key, audio_path):
    url = "https://stt.api.cloud.yandex.net/speech/v1/stt:recognize"

    with open(audio_path, "rb") as f:
        data = f.read()

    headers = {
        "Authorization": f"Api-Key {api_key}",
        "Content-Type": "audio/x-ogg",
    }

    params = {
        "topic": "general",
        "lang": "ru-RU",
    }

    response = requests.post(url, headers=headers, params=params, data=data)

    if response.status_code == 200:
        result = response.json()
        if "result" in result:
            print(f"Текст: {result['result']}")
            return result['result']
        else:
            print("Распознавание не удалось.")
            return None
    else:
        print(f"Ошибка {response.status_code}: {response.text}")
        return None

if __name__ == "__main__":
    thread_A = CustomThread()
    thread_A.start()
    yandex_api_key = "XXXXXXXXXXXXXXXXXXXXXX"
    audio_file_path = "C:/Users/Рёта/PycharmProjects/pythonProject1/output.ogg"
    listening = False  # Флаг, указывающий, что ассистент должен начать слушать речь

    while True:  # Бесконечный цикл для непрерывной работы ассистента
        if not listening:
            result_text = record_and_recognize_yandex(yandex_api_key, audio_file_path)  # Передаем audio_file_path

            if result_text == "Мера":  # Если ассистент услышал фразу "Мера", то начинаем слушать команды
                listening = True
                speaker("Слушаю вас!")

        else:
            # Слушаем команды
            result_text = record_and_recognize_yandex(yandex_api_key, audio_file_path)

            if result_text:
                if result_text == "Открой браузер":
                    speaker("Хорошо, надеюсь вы любите Яндекс!")
                    url_to_open = "https://ya.ru/"
                    open_browser_with_actions(url_to_open)
                elif result_text == "Открой google":
                    speaker("Ладно, у всех вкусы разные!")
                    url_to_open = "https://www.google.ru/"
                    open_browser_with_actions(url_to_open)
                elif result_text == "Запусти кс":
                    speaker("Зачем, вы все равно даже мышь держать не умеете!")
                    file_to_open = "steam://rungameid/730"
                    open_file(file_to_open)
                elif result_text == "Запусти фифу":
                    speaker("ССССУУУУУУУУУУУУУУ")
                    file_to_open = "steam://rungameid/1506830"
                    open_file(file_to_open)
                elif result_text == "Запусти нба":
                    speaker("Ты кроссовки купил, чтобы на компе играть?")
                    file_to_open = "steam://rungameid/1644960"
                    open_file(file_to_open)
                elif result_text == "Запусти гарика":
                    speaker("Вот же колдун!!!")
                    file_to_open = "C://Program Files (x86)//Hogwarts Legacy/HogwartsLegacy.exe"
                    open_file(file_to_open)
                elif result_text == "Поставь на таймер":
                    speaker("На сколько секунд поставить таймер?")
                    timer_duration = int(record_and_recognize_yandex(yandex_api_key,audio_file_path)) # Записываем продолжительность таймера, которую сказал пользователь
                    set_shutdown_timer(timer_duration)
                    speaker(f"Таймер на {timer_duration} секунд успешно установлен.")
                elif result_text == "Отмени таймер":
                    cancel_shutdown_timer()
                    speaker("Таймер выключения успешно отменен.")
                elif result_text == "Выход" or result_text == "Стоп":  # Предположим, что вы хотите выйти из цикла, когда услышите фразу "выход"
                        break  # Выходим из цикла

                # Здесь можно добавить другие команды

                listening = False  # После выполнения команды возвращаемся к прослушиванию фразы "Мера"


