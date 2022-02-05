from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import MDList, OneLineIconListItem

from settings.common_settings import CommonSettingsForm

Builder.load_file(r"content_navigation_drawer.kv")


class ContentNavigationDrawer(MDBoxLayout):

    def __init__(self, **kwargs):
        super(ContentNavigationDrawer, self).__init__(**kwargs)

    def open_common_settings(self):
        settings = CommonSettingsForm()
        settings.owner = self
        settings.open()

    def after_dismiss_child(self, parameters):
        pass


class DrawerList(ThemableBehavior, MDList):
    pass


class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()
