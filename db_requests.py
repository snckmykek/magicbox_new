import sqlite3
from datetime import datetime

from kivy.clock import Clock


class Database(object):

    def __init__(self):
        self.con = sqlite3.connect('database_magicbox.db')
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()
        self.sqlite_create_db()
        self.initial_setup()

    def delayed_commit(self):
        Clock.schedule_once(lambda *args: self.con.commit())

    def commit(self):
        self.con.commit()

    def sqlite_create_db(self):
        # Для значений, который пользователь может выбирать из списка, но не создавать сам
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS limited_values(
                key TEXT NOT NULL,
                value NOT NULL,
                CONSTRAINT pk PRIMARY KEY (key, value)
            ) 
            """)

        # Синонимы для limited_values
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS limited_values_synonyms(
                lang TEXT NOT NULL,
                key TEXT NOT NULL,
                value NOT NULL,
                synonym TEXT NOT NULL,
                CONSTRAINT pk PRIMARY KEY (lang, key, value)
            ) 
            """)

        # В качестве ключа передается строка на русском, обратно возвращается в зависимости от языка,
        # Таблица для оформления интерфейса на разных языках, пользователь напрямую не работает с ней
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS multilang_interface(
                lang TEXT NOT NULL,
                key TEXT NOT NULL,
                text TEXT DEFAULT NULL,
                CONSTRAINT pk PRIMARY KEY (lang, key)
            ) 
            """)

        # Внутренние настройки приложения конкретного пользователя
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS common_settings(
                key TEXT PRIMARY KEY NOT NULL,
                value NOT NULL
            ) 
            """)

    def initial_setup(self):
        self.fill_limited_values()
        self.fill_multilang_interface()
        self.fill_common_settings()

        self.commit()

    def fill_limited_values(self):
        # Языки
        self.cur.execute(
            """
            INSERT OR IGNORE INTO
                limited_values
            VALUES
                ("lang", "ru"), 
                ("lang", "en")
            """)

        # Для всех языков синонимы в том же языке, чтобы можно было выбрать без знания других языков
        # Список выбора языка (на любом языке в настройках) будет одиноковый:
        # - Русский
        # - English
        # - и тд.
        self.cur.execute(
            """
            INSERT OR IGNORE INTO
                limited_values_synonyms
            VALUES
                ("ru", "lang", "ru", "Русский"), 
                ("ru", "lang", "en", "English"),
                ("en", "lang", "ru", "Русский"), 
                ("en", "lang", "en", "English")
            """)

        # Темы (темная, светлая)
        self.cur.execute(
            """
            INSERT OR IGNORE INTO
                limited_values
            VALUES
                ("theme_style", "Light"), 
                ("theme_style", "Dark")
            """)

        self.cur.execute(
            """
            INSERT OR IGNORE INTO
                limited_values_synonyms
            VALUES
                ("ru", "theme_style", "Light", "Светлый"), 
                ("ru", "theme_style", "Dark", "Темный"),
                ("en", "theme_style", "Light", "Light"), 
                ("en", "theme_style", "Dark", "Dark")
            """)

    def fill_multilang_interface(self):
        # main.kv
        self.cur.execute(
            """
            INSERT OR IGNORE INTO
                multilang_interface
            VALUES
                ("ru", "Бюджет", "Бюджет"), 
                ("en", "Бюджет", "Budget"),
                ("ru", "Планировщик", "Планировщик"), 
                ("en", "Планировщик", "Glider"),
                ("ru", "Списки продуктов", "Списки продуктов"), 
                ("en", "Списки продуктов", "Products lists"),
                ("ru", "Прогресс", "Прогресс"), 
                ("en", "Прогресс", "Progress"),
                ("ru", "Рецепты", "Рецепты"), 
                ("en", "Рецепты", "Recipes"),
                ("ru", "Настройки", "Настройки"), 
                ("en", "Настройки", "Settings")
            """)

    def fill_common_settings(self):
        # Дефолтные настройки пи первом запуске (или при возврате к настройкам по умолчанию)
        self.cur.execute(
            """
            INSERT OR IGNORE INTO
                common_settings
            VALUES
                ("theme_style", "Light"), 
                ("lang", "ru")
            """)

    def get_common_setting(self, key):
        """Возвращает настройку по ключу.
        Если настройка не найдена, возвращает None.
        """

        self.cur.execute(
            f"""
            SELECT
                value
            FROM
                common_settings
            WHERE
                key = "{key}"
            """)

        try:
            return self.cur.fetchone()["value"]
        except TypeError:
            return None

    def interface_lang(self, key):
        """Возвращает синоним для элемента интерфейса по ключу и языку из настроек."""

        self.cur.execute(
            f"""
            SELECT
                text
            FROM
                multilang_interface
                INNER JOIN (SELECT
                                common_settings.value
                            FROM
                                common_settings
                            WHERE
                                common_settings.key = "lang") as langs
                    ON multilang_interface.lang = langs.value
            WHERE
                multilang_interface.key = "{key}"
            """)

        try:
            return self.cur.fetchone()["text"]
        except TypeError:
            return ""


db = Database()
