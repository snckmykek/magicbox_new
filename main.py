from kivy.config import Config
Config.set('graphics', 'resizable', '1')
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')

from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout

from db_requests import db


class MainScreen(MDBoxLayout):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)


class MainApp(MDApp):
    current_title = StringProperty("magicbox v.MEGAHOROSH")  # Динамически меняется заголовок
    waiting_message = StringProperty("")  # При длительных операциях, сообщение пользователю

    def build(self):
        self.theme_cls.theme_style = db.get_common_setting("theme_style")
        self.theme_cls.primary_palette = "Cyan"
        # self.theme_cls.primary_hue = "200"

        return MainScreen()

    def change_current_title(self, new_title):
        self.current_title = new_title


if __name__ == "__main__":
    MainApp().run()
