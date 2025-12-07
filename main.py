import threading
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList, OneLineListItem
from kivy.clock import Clock
from openai import OpenAI

class NikitaAI(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Dark"
        
        # --- НАСТРОЙКИ DEEPSEEK ---
        # Вставь свой ключ внутри кавычек ниже:
        self.api_key = "sk-138f247a94ea4c619d92559e4dbfb3d1" 
        self.base_url = "https://api.deepseek.com"
        
        # Инициализация клиента
        try:
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        except:
            self.client = None

        # Интерфейс
        screen = MDScreen()
        layout = MDBoxLayout(orientation='vertical', padding=10, spacing=10)

        # Список сообщений
        self.scroll = MDScrollView()
        self.list_view = MDList()
        self.scroll.add_widget(self.list_view)

        # Поле ввода
        input_layout = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        self.text_input = MDTextField(hint_text="Спроси Никиту...", mode="rectangle")
        send_btn = MDRaisedButton(text="Отправить", on_release=self.send_message)

        input_layout.add_widget(self.text_input)
        input_layout.add_widget(send_btn)

        layout.add_widget(MDLabel(text="Никита ИИ (DeepSeek)", halign="center", size_hint_y=None, height=40, font_style="H6"))
        layout.add_widget(self.scroll)
        layout.add_widget(input_layout)

        screen.add_widget(layout)
        return screen

    def send_message(self, instance):
        user_text = self.text_input.text
        if not user_text:
            return

        # 1. Показываем сообщение пользователя сразу
        self.list_view.add_widget(OneLineListItem(text=f"Вы: {user_text}", theme_text_color="Custom", text_color=(1, 1, 1, 1)))
        self.text_input.text = "" # Очистить поле
        
        # 2. Запускаем запрос к ИИ в отдельном потоке, чтобы приложение не зависло
        threading.Thread(target=self.get_ai_response_thread, args=(user_text,)).start()

    def get_ai_response_thread(self, text):
        try:
            # Запрос к DeepSeek
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "Ты полезный помощник по имени Никита."},
                    {"role": "user", "content": text},
                ],
                stream=False
            )
            answer = response.choices[0].message.content
        except Exception as e:
            answer = f"Ошибка связи: {str(e)}"

        # 3. Возвращаемся в главный поток, чтобы обновить экран
        Clock.schedule_once(lambda dt: self.update_chat(answer))

    def update_chat(self, text):
        # Добавляем ответ ИИ на экран
        self.list_view.add_widget(OneLineListItem(text=f"Никита: {text}", theme_text_color="Custom", text_color=(0.2, 0.8, 1, 1)))

if __name__ == '__main__':
    NikitaAI().run()
