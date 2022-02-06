from kivy.lang.builder import Builder
from kivymd.uix.boxlayout import MDBoxLayout

from content.list.list_ef import ListElementForm


Builder.load_file(r"content/list/list_main_form.kv")


class ListMainForm(MDBoxLayout):

    def __init__(self, **kwargs):
        super(ListMainForm, self).__init__(**kwargs)

    def create_new_list(self):
        lef = ListElementForm()
        lef.owner = self
        lef.open()

    def after_dismiss_child(self, parameters):
        print(parameters)
